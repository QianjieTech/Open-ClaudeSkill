"""MCP Server implementation for Claude Skills."""

import asyncio
import json
from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .skill_loader import SkillLoader


class SkillFileHandler(FileSystemEventHandler):
    """Watches for changes in the skills directory."""

    def __init__(self, skill_loader: SkillLoader, callback):
        self.skill_loader = skill_loader
        self.callback = callback

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('SKILL.md'):
            print(f"Skill file modified: {event.src_path}")
            self.callback()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('SKILL.md'):
            print(f"Skill file created: {event.src_path}")
            self.callback()

    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('SKILL.md'):
            print(f"Skill file deleted: {event.src_path}")
            self.callback()


class SkillMCPServer:
    """MCP Server that provides skill loading capabilities."""

    def __init__(self, skills_dir: Optional[Path] = None):
        self.server = Server("mcp-server-skill")
        self.skill_loader = SkillLoader(skills_dir)
        self.observer: Optional[Observer] = None

        # Setup handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP server request handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools (just the skill loader tool)."""
            return [
                Tool(
                    name="load_skill",
                    description="""Execute a skill within the main conversation

<skills_instructions>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke skills using this tool with the skill name only (no arguments)
- When you invoke a skill, you will see the message "The {name} skill is loading"
- The skill's prompt will expand and provide detailed instructions on how to complete the task
- Examples:
  - load_skill with name: "pdf" - invoke the pdf skill
  - load_skill with name: "xlsx" - invoke the xlsx skill

Important:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already running
</skills_instructions>

""" + self.skill_loader.generate_skills_xml(),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skill": {
                                "type": "string",
                                "description": "The skill name (no arguments). E.g., 'pdf' or 'xlsx'"
                            }
                        },
                        "required": ["skill"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            if name != "load_skill":
                raise ValueError(f"Unknown tool: {name}")

            skill_name = arguments.get("skill")
            if not skill_name:
                raise ValueError("Missing required argument: skill")

            # Reload skills to get latest changes
            self.skill_loader.discover_skills()

            skill = self.skill_loader.get_skill(skill_name)
            if not skill:
                available_skills = ", ".join(self.skill_loader.skills.keys())
                return [TextContent(
                    type="text",
                    text=f"Error: Skill '{skill_name}' not found.\n\nAvailable skills: {available_skills}"
                )]

            # Return the full skill content
            response = f"""The "{skill_name}" skill is loading...

---
name: {skill.name}
description: {skill.description}
"""
            if skill.license:
                response += f"license: {skill.license}\n"
            if skill.allowed_tools:
                response += f"allowed-tools: {json.dumps(skill.allowed_tools)}\n"
            if skill.metadata:
                response += f"metadata: {json.dumps(skill.metadata)}\n"

            response += "---\n\n" + skill.content

            return [TextContent(
                type="text",
                text=response
            )]

    def reload_skills(self):
        """Reload skills from the filesystem."""
        print("Reloading skills...")
        self.skill_loader.discover_skills()
        print(f"Loaded {len(self.skill_loader.skills)} skills")

    def start_watching(self):
        """Start watching the skills directory for changes."""
        if not self.skill_loader.skills_dir.exists():
            print(f"Skills directory does not exist: {self.skill_loader.skills_dir}")
            return

        self.observer = Observer()
        event_handler = SkillFileHandler(self.skill_loader, self.reload_skills)
        self.observer.schedule(
            event_handler,
            str(self.skill_loader.skills_dir),
            recursive=True
        )
        self.observer.start()
        print(f"Watching for skill changes in: {self.skill_loader.skills_dir}")

    def stop_watching(self):
        """Stop watching the skills directory."""
        if self.observer:
            self.observer.stop()
            self.observer.join()

    async def run(self):
        """Run the MCP server."""
        # Initial skill discovery
        self.reload_skills()

        # Start watching for changes
        self.start_watching()

        try:
            # Run the server
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        finally:
            self.stop_watching()


def main():
    """Main entry point for the MCP server."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="MCP Server for Claude Skills with progressive disclosure"
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help="Directory containing skill folders (default: .skill in current directory)"
    )

    args = parser.parse_args()

    # Create and run server
    server = SkillMCPServer(skills_dir=args.skills_dir)

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)


if __name__ == "__main__":
    main()
