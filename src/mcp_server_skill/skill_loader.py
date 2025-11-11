"""Skill loader module for discovering and parsing SKILL.md files."""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Skill:
    """Represents a parsed skill."""

    name: str
    description: str
    content: str  # Full markdown content after frontmatter
    license: Optional[str] = None
    allowed_tools: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None
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
        if not self.skills_dir.exists():
            print(f"Skills directory not found: {self.skills_dir}")
            return {}

        discovered_skills = {}

        # Iterate through all subdirectories
        for skill_folder in self.skills_dir.iterdir():
            if not skill_folder.is_dir():
                continue

            skill_file = skill_folder / "SKILL.md"
            if not skill_file.exists():
                continue

            try:
                skill = self._parse_skill_file(skill_file, skill_folder)
                if skill:
                    discovered_skills[skill.name] = skill
            except Exception as e:
                print(f"Error parsing skill {skill_folder.name}: {e}")

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
            print(f"Warning: {skill_file} doesn't start with YAML frontmatter")
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"Warning: {skill_file} has invalid frontmatter format")
            return None

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {skill_file}: {e}")
            return None

        # Extract markdown body
        markdown_body = parts[2].strip()

        # Validate required fields
        if 'name' not in frontmatter:
            print(f"Error: {skill_file} missing required 'name' field")
            return None
        if 'description' not in frontmatter:
            print(f"Error: {skill_file} missing required 'description' field")
            return None

        # Verify name matches folder name
        if frontmatter['name'] != folder_path.name:
            print(f"Warning: skill name '{frontmatter['name']}' doesn't match folder name '{folder_path.name}'")

        return Skill(
            name=frontmatter['name'],
            description=frontmatter['description'],
            content=markdown_body,
            license=frontmatter.get('license'),
            allowed_tools=frontmatter.get('allowed-tools'),
            metadata=frontmatter.get('metadata'),
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
