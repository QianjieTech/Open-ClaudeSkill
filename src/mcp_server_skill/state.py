"""Server state management for MCP Skill Server."""

import os
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass, field

from .skill_loader import Skill


@dataclass
class ServerState:
    """
    Manages the runtime state of the MCP Skill Server.

    This includes:
    - Skills directory path (can be set dynamically)
    - Loaded skills cache
    - Client capability flags
    - Environment variables
    """

    # Skills directory (can be None initially, set later via tool)
    skills_directory: Optional[Path] = None

    # Currently loaded skills
    current_skills: Dict[str, Skill] = field(default_factory=dict)

    # Client capabilities detected during initialization
    supports_list_changed: bool = False

    # Environment variable override
    env_skills_dir: Optional[str] = field(default=None)

    # Command-line argument override
    cli_skills_dir: Optional[Path] = None

    def __post_init__(self):
        """Initialize environment variable."""
        self.env_skills_dir = os.getenv('MCP_SKILLS_DIR')

    def get_effective_skills_directory(self) -> Optional[Path]:
        """
        Get the effective skills directory based on priority order.

        Priority (highest to lowest):
        1. Command-line argument (--skills-dir)
        2. Environment variable (MCP_SKILLS_DIR)
        3. Dynamically set path (via set_skills_directory tool)
        4. Project-level discovery (.claude/skills/ or .skill/ in project root)
        5. Global fallback (~/.skill)

        Returns:
            Path to skills directory or None if not found
        """
        # Priority 1: CLI argument (with smart subdirectory detection)
        if self.cli_skills_dir is not None:
            resolved_path = self._resolve_skills_path(self.cli_skills_dir)
            if resolved_path:
                return resolved_path

        # Priority 2: Environment variable (with smart subdirectory detection)
        if self.env_skills_dir:
            env_path = Path(self.env_skills_dir)
            resolved_path = self._resolve_skills_path(env_path)
            if resolved_path:
                return resolved_path

        # Priority 3: Dynamically set directory
        if self.skills_directory is not None:
            if self.skills_directory.exists():
                return self.skills_directory

        # Priority 4: Project-level discovery
        project_skill_dir = self._find_project_skill_dir()
        if project_skill_dir is not None:
            return project_skill_dir

        # Priority 5: Global fallback
        global_skill_dir = Path.home() / ".skill"
        if global_skill_dir.exists():
            return global_skill_dir

        return None

    def _resolve_skills_path(self, path: Path) -> Optional[Path]:
        """
        Resolve a path to a skills directory with smart subdirectory detection.

        If the path points to a project root, automatically detect .claude/skills/ or .skill/.
        If the path is already a skills directory, use it directly.

        Args:
            path: Path to resolve

        Returns:
            Resolved skills directory path, or None if not found
        """
        if not path.exists():
            return None

        if not path.is_dir():
            return None

        # If path is already a skills directory, use it directly
        if path.name in [".skill", "skills"]:
            return path

        # Otherwise, look for skills subdirectories
        # Check both potential directories and prefer non-empty ones
        claude_skills_dir = path / ".claude" / "skills"
        skill_dir = path / ".skill"

        claude_exists = claude_skills_dir.is_dir()
        skill_exists = skill_dir.is_dir()

        # If both exist, check which one has skills (non-empty with SKILL.md files)
        if claude_exists and skill_exists:
            claude_has_skills = self._directory_has_skills(claude_skills_dir)
            skill_has_skills = self._directory_has_skills(skill_dir)

            # Priority 1: .claude/skills/ if it has skills
            if claude_has_skills:
                return claude_skills_dir
            # Priority 2: .skill/ if it has skills
            if skill_has_skills:
                return skill_dir
            # If both are empty, prefer .claude/skills/ (ClaudeCode format)
            return claude_skills_dir

        # Only .claude/skills/ exists
        if claude_exists:
            return claude_skills_dir

        # Only .skill/ exists
        if skill_exists:
            return skill_dir

        # If no subdirectories found, try using the path as-is
        # (in case it's a custom skills directory structure)
        return path

    def _directory_has_skills(self, directory: Path) -> bool:
        """
        Check if a directory contains any skills (subdirectories with SKILL.md).

        Args:
            directory: Directory to check

        Returns:
            True if directory contains at least one valid skill
        """
        if not directory.exists() or not directory.is_dir():
            return False

        # Check for any subdirectory containing SKILL.md
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / "SKILL.md").exists():
                    return True

        return False

    def _find_project_skill_dir(self) -> Optional[Path]:
        """
        Find project-level skills directory by traversing up from current directory.

        Looks for project root markers:
        - .git/
        - .claude/
        - .skill/
        - package.json
        - pyproject.toml, setup.py
        - Cargo.toml
        - go.mod

        Priority: .claude/skills/ (ClaudeCode format) > .skill/ (legacy format)

        Returns:
            Path to skills directory in project root, or None if not found
        """
        current = Path.cwd()

        # Traverse up the directory tree
        while current != current.parent:
            # Check if this is a project root
            is_project_root = any([
                (current / ".git").is_dir(),
                (current / ".claude").is_dir(),
                (current / ".skill").is_dir(),
                (current / "package.json").is_file(),
                (current / "pyproject.toml").is_file(),
                (current / "setup.py").is_file(),
                (current / "Cargo.toml").is_file(),
                (current / "go.mod").is_file(),
            ])

            if is_project_root:
                # Check both potential directories
                claude_skills_dir = current / ".claude" / "skills"
                skill_dir = current / ".skill"

                claude_exists = claude_skills_dir.is_dir()
                skill_exists = skill_dir.is_dir()

                # If both exist, prefer the non-empty one
                if claude_exists and skill_exists:
                    claude_has_skills = self._directory_has_skills(claude_skills_dir)
                    skill_has_skills = self._directory_has_skills(skill_dir)

                    if claude_has_skills:
                        return claude_skills_dir
                    if skill_has_skills:
                        return skill_dir
                    # If both empty, prefer .claude/skills/
                    return claude_skills_dir

                # Priority 1: .claude/skills/ (ClaudeCode format)
                if claude_exists:
                    return claude_skills_dir

                # Priority 2: .skill/ (legacy format)
                if skill_exists:
                    return skill_dir

            current = current.parent

        return None

    def set_skills_directory(self, path: str) -> tuple[bool, str]:
        """
        Set the skills directory dynamically.

        Args:
            path: Absolute or relative path to project root, .claude/skills/, or .skill/ directory

        Returns:
            Tuple of (success: bool, message: str)
        """
        skills_path = Path(path).resolve()

        # Validate path exists
        if not skills_path.exists():
            return False, f"Path does not exist: {skills_path}"

        # Validate it's a directory
        if not skills_path.is_dir():
            return False, f"Path is not a directory: {skills_path}"

        # Smart detection: if path is not already a skills directory, look for subdirectories
        if skills_path.name not in [".skill", "skills"]:
            claude_skills_dir = skills_path / ".claude" / "skills"
            skill_dir = skills_path / ".skill"

            claude_exists = claude_skills_dir.is_dir()
            skill_exists = skill_dir.is_dir()

            # If both exist, prefer the non-empty one
            if claude_exists and skill_exists:
                claude_has_skills = self._directory_has_skills(claude_skills_dir)
                skill_has_skills = self._directory_has_skills(skill_dir)

                if claude_has_skills:
                    skills_path = claude_skills_dir
                elif skill_has_skills:
                    skills_path = skill_dir
                else:
                    # Both empty, prefer .claude/skills/
                    skills_path = claude_skills_dir
            # Priority 1: .claude/skills/ (ClaudeCode format)
            elif claude_exists:
                skills_path = claude_skills_dir
            # Priority 2: .skill/ (legacy format)
            elif skill_exists:
                skills_path = skill_dir

        self.skills_directory = skills_path
        return True, f"Skills directory set to: {skills_path}"

    def update_skills(self, skills: Dict[str, Skill]):
        """Update the current skills cache."""
        self.current_skills = skills

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name from cache."""
        return self.current_skills.get(name)
