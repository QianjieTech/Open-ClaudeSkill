"""Skill loader module for discovering and parsing SKILL.md files."""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Skill:
    """Represents a parsed skill.

    Following official Claude Skill format:
    - name: Skill identifier (must match folder name)
    - description: Detailed description for agent matching
    - license: Optional license information
    - content: Full markdown content after frontmatter
    - folder_path: Path to skill folder (for resource resolution)
    """

    name: str
    description: str
    content: str  # Full markdown content after frontmatter
    license: Optional[str] = None
    location: str = "local"  # local or managed
    folder_path: Path = None

    def to_xml(self) -> str:
        """Convert skill metadata to XML format for agent system prompt."""
        xml = f"""<skill>
<name>{self.name}</name>
<description>{self.description}</description>
<location>{self.location}</location>
</skill>"""
        return xml


class SkillLoader:
    """Loads and manages skills from the filesystem."""

    def __init__(self, skills_dir: Optional[Path] = None):
        """
        Initialize the skill loader.

        Args:
            skills_dir: Directory containing skill folders.
                       Defaults to .skill in current working directory.
        """
        if skills_dir is None:
            # Default to .skill folder in current working directory
            self.skills_dir = Path.cwd() / ".skill"
        else:
            self.skills_dir = Path(skills_dir)

        self.skills: Dict[str, Skill] = {}

    def discover_skills(self) -> Dict[str, Skill]:
        """
        Discover all skills in the skills directory.

        Returns:
            Dictionary mapping skill names to Skill objects.
        """
        if not self.skills_dir:
            logger.debug("Skills directory not set")
            return {}

        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return {}

        discovered_skills = {}

        # Iterate through all subdirectories
        for skill_folder in self.skills_dir.iterdir():
            if not skill_folder.is_dir():
                continue

            # Skip hidden directories
            if skill_folder.name.startswith('.'):
                continue

            skill_file = skill_folder / "SKILL.md"
            if not skill_file.exists():
                logger.debug(f"Skipping {skill_folder.name}: no SKILL.md found")
                continue

            try:
                skill = self._parse_skill_file(skill_file, skill_folder)
                if skill:
                    discovered_skills[skill.name] = skill
                    logger.debug(f"Loaded skill: {skill.name}")
            except Exception as e:
                logger.error(f"Error parsing skill {skill_folder.name}: {e}", exc_info=True)

        self.skills = discovered_skills
        return discovered_skills

    def _parse_skill_file(self, skill_file: Path, folder_path: Path) -> Optional[Skill]:
        """
        Parse a SKILL.md file.

        Args:
            skill_file: Path to the SKILL.md file.
            folder_path: Path to the skill folder.

        Returns:
            Parsed Skill object or None if parsing fails.
        """
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split frontmatter and body
        if not content.startswith('---'):
            logger.warning(f"{skill_file} doesn't start with YAML frontmatter")
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            logger.warning(f"{skill_file} has invalid frontmatter format")
            return None

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in {skill_file}: {e}")
            return None

        # Extract markdown body
        markdown_body = parts[2].strip()

        # Validate required fields
        if 'name' not in frontmatter:
            logger.error(f"{skill_file} missing required 'name' field")
            return None
        if 'description' not in frontmatter:
            logger.error(f"{skill_file} missing required 'description' field")
            return None

        # Verify name matches folder name
        if frontmatter['name'] != folder_path.name:
            logger.warning(f"Skill name '{frontmatter['name']}' doesn't match folder name '{folder_path.name}'")

        # Note: Only official frontmatter fields are extracted
        # (name, description, license)
        # Non-standard fields like 'allowed-tools' and 'metadata' are ignored
        return Skill(
            name=frontmatter['name'],
            description=frontmatter['description'],
            content=markdown_body,
            license=frontmatter.get('license'),
            folder_path=folder_path
        )

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self.skills.get(name)

    def list_skills(self) -> List[Skill]:
        """Get list of all skills."""
        return list(self.skills.values())

    def generate_skills_xml(self) -> str:
        """
        Generate XML representation of all skills for agent system prompt.

        Returns:
            XML string with all available skills.
        """
        skills_xml = "<available_skills>\n"
        for skill in sorted(self.skills.values(), key=lambda s: s.name):
            skills_xml += skill.to_xml() + "\n"
        skills_xml += "</available_skills>"
        return skills_xml

    @staticmethod
    def resolve_skill_resource_path(skill: Skill, relative_path: str) -> Path:
        """
        Resolve a relative path to a skill resource file.

        This allows skills to reference auxiliary resources like templates,
        fonts, scripts, etc. using relative paths within their folder.

        Args:
            skill: The skill object
            relative_path: Relative path within the skill folder (e.g., "templates/viewer.html")

        Returns:
            Absolute path to the resource file

        Raises:
            ValueError: If path traversal is detected or path is outside skill directory
            FileNotFoundError: If the resource file doesn't exist

        Example:
            >>> skill = get_skill("algorithmic-art")
            >>> path = resolve_skill_resource_path(skill, "templates/viewer.html")
            >>> with open(path, 'r') as f:
            ...     content = f.read()
        """
        if not skill.folder_path:
            raise ValueError(f"Skill '{skill.name}' has no folder_path set")

        # Security: Prevent path traversal attacks
        if ".." in relative_path:
            raise ValueError(f"Path traversal not allowed: {relative_path}")

        # Construct full path
        full_path = skill.folder_path / relative_path

        # Security: Verify path is within skill directory
        try:
            resolved_path = full_path.resolve()
            skill_folder_resolved = skill.folder_path.resolve()

            if not str(resolved_path).startswith(str(skill_folder_resolved)):
                raise ValueError(f"Path outside skill directory: {relative_path}")
        except Exception as e:
            raise ValueError(f"Invalid path: {relative_path}") from e

        # Verify file exists
        if not resolved_path.exists():
            raise FileNotFoundError(f"Resource not found: {relative_path}")

        return resolved_path
