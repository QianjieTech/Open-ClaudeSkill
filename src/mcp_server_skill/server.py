"""MCP Server implementation for Claude Skills."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .skill_loader import SkillLoader
from .state import ServerState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SkillFileHandler(FileSystemEventHandler):
    """Watches for changes in the skills directory with debouncing."""

    def __init__(self, skill_loader: SkillLoader, callback):
        self.skill_loader = skill_loader
        self.callback = callback
        self._pending_reload = False
        self._debounce_timer = None
        self._debounce_delay = 0.3  # 300ms debounce window

    def _should_process(self, event) -> bool:
        """Check if event should trigger a reload."""
        if event.is_directory:
            return False

        # Only process SKILL.md files
        if not event.src_path.endswith('SKILL.md'):
            return False

        # Ignore temporary files
        path = Path(event.src_path)
        if path.name.startswith('.') or path.name.endswith(('.swp', '.tmp', '~')):
            return False

        return True

    def _schedule_reload(self, event_type: str, path: str):
        """Schedule a debounced reload."""
        if self._debounce_timer:
            self._debounce_timer.cancel()

        def do_reload():
            logger.info(f"Skill file {event_type}: {path}")
            self.callback()
            self._pending_reload = False

        self._pending_reload = True
        import threading
        self._debounce_timer = threading.Timer(self._debounce_delay, do_reload)
        self._debounce_timer.start()

    def on_modified(self, event):
        if self._should_process(event):
            self._schedule_reload("modified", event.src_path)

    def on_created(self, event):
        if self._should_process(event):
            self._schedule_reload("created", event.src_path)

    def on_deleted(self, event):
        if self._should_process(event):
            self._schedule_reload("deleted", event.src_path)


class SkillMCPServer:
    """MCP Server that provides skill loading capabilities."""

    def __init__(self, skills_dir: Optional[Path] = None):
        self.server = Server("agentskill-mcp")

        # Initialize server state
        self.state = ServerState(cli_skills_dir=skills_dir)

        # Initialize skill loader (will use state to find directory)
        effective_dir = self.state.get_effective_skills_directory()

        # Log path resolution details
        logger.info(f"Current working directory: {Path.cwd()}")
        if skills_dir:
            logger.info(f"CLI skills_dir argument: {skills_dir}")
        logger.info(f"Resolved skills directory: {effective_dir}")

        self.skill_loader = SkillLoader(effective_dir)

        # Discover skills immediately so they're available when list_tools() is called
        if effective_dir:
            self.skill_loader.discover_skills()
            self.state.update_skills(self.skill_loader.skills)
            logger.info(f"Discovered {len(self.skill_loader.skills)} skills: {list(self.skill_loader.skills.keys())}")
        else:
            logger.warning("No skills directory found - skills will not be available")

        self.observer: Optional[Observer] = None

        # Setup handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP server request handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            tools = []

#             # Tool 1: Set skills directory (environment awareness)
#             tools.append(Tool(
#                 name="set_skills_directory",
#                 description="""Set the skills directory for the current session.

# This tool allows you to specify which .skill directory to use for loading skills.
# Use this at the beginning of a conversation if you have access to the user's current
# working directory or project path.

# Usage:
# - Call this once at the start of the conversation
# - Provide the path to the project directory (it will look for .skill subdirectory)
# - Or provide the direct path to a .skill directory
# - Supports both absolute and relative paths

# Example:
# If user is working in /path/to/project and it has /path/to/project/.skill:
#   set_skills_directory(path="/path/to/project")

# If you discover the current directory through context or pwd command:
#   set_skills_directory(path=<current_directory>)
# """,
#                 inputSchema={
#                     "type": "object",
#                     "properties": {
#                         "path": {
#                             "type": "string",
#                             "description": "Absolute or relative path to the project directory or .skill directory"
#                         }
#                     },
#                     "required": ["path"]
#                 }
#             ))

            # Tool 2: Load skill (progressive disclosure)
            tools.append(Tool(
                name="load_skill",
                description="""Execute a skill within the main conversation

<skills_instructions>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke skills using this tool with the skill name only (no arguments)
- When you invoke a skill, you will see the message "The {name} skill is loading"
- The skill's prompt will expand and provide detailed instructions on how to complete the task
- Examples:
  - load_skill with skill: "code-reviewer"
  - load_skill with skill: "calculator"

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
                            "description": "The skill name (no arguments). E.g., 'code-reviewer' or 'calculator'"
                        }
                    },
                    "required": ["skill"]
                }
            ))

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""

            # Handle set_skills_directory tool
            if name == "set_skills_directory":
                path = arguments.get("path")
                if not path:
                    return [TextContent(
                        type="text",
                        text="Error: Missing required argument: path"
                    )]

                success, message = self.state.set_skills_directory(path)

                if success:
                    # Reload skill loader with new directory
                    effective_dir = self.state.get_effective_skills_directory()
                    self.skill_loader = SkillLoader(effective_dir)
                    self.reload_skills()

                    # Restart file watching with new directory
                    self.stop_watching()
                    self.start_watching()

                    return [TextContent(
                        type="text",
                        text=f"✓ {message}\n\nDiscovered {len(self.skill_loader.skills)} skills: {', '.join(self.skill_loader.skills.keys())}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"✗ {message}"
                    )]

            # Handle load_skill tool
            elif name == "load_skill":
                skill_name = arguments.get("skill")
                if not skill_name:
                    raise ValueError("Missing required argument: skill")

                # Reload skills to get latest changes
                self.skill_loader.discover_skills()
                self.state.update_skills(self.skill_loader.skills)

                skill = self.skill_loader.get_skill(skill_name)
                if not skill:
                    available_skills = ", ".join(self.skill_loader.skills.keys())
                    return [TextContent(
                        type="text",
                        text=f"Error: Skill '{skill_name}' not found.\n\nAvailable skills: {available_skills}"
                    )]

                # Return the full skill content (following official format)
                response = f"""The "{skill_name}" skill is loading...

---
name: {skill.name}
description: {skill.description}
"""
                if skill.license:
                    response += f"license: {skill.license}\n"

                response += "---\n\n" + skill.content

                return [TextContent(
                    type="text",
                    text=response
                )]

            else:
                raise ValueError(f"Unknown tool: {name}")

    def reload_skills(self):
        """Reload skills from the filesystem."""
        logger.info("Reloading skills...")
        try:
            self.skill_loader.discover_skills()
            self.state.update_skills(self.skill_loader.skills)
            logger.info(f"Loaded {len(self.skill_loader.skills)} skills: {', '.join(self.skill_loader.skills.keys())}")
        except Exception as e:
            logger.error(f"Error reloading skills: {e}", exc_info=True)

    def start_watching(self):
        """Start watching the skills directory for changes."""
        if not self.skill_loader.skills_dir:
            logger.warning("Skills directory not set, file watching disabled")
            return

        if not self.skill_loader.skills_dir.exists():
            logger.warning(f"Skills directory does not exist: {self.skill_loader.skills_dir}")
            return

        try:
            self.observer = Observer()
            event_handler = SkillFileHandler(self.skill_loader, self.reload_skills)
            self.observer.schedule(
                event_handler,
                str(self.skill_loader.skills_dir),
                recursive=True
            )
            self.observer.start()
            logger.info(f"Watching for skill changes in: {self.skill_loader.skills_dir}")
        except Exception as e:
            logger.error(f"Failed to start file watching: {e}", exc_info=True)

    def stop_watching(self):
        """Stop watching the skills directory."""
        if self.observer:
            self.observer.stop()
            self.observer.join()

    async def run(self):
        """Run the MCP server."""
        # Log effective skills directory
        effective_dir = self.state.get_effective_skills_directory()
        if effective_dir:
            logger.info(f"Using skills directory: {effective_dir}")
        else:
            logger.warning("No skills directory found. Use set_skills_directory tool to configure.")

        # Initial skill discovery
        if effective_dir:
            self.reload_skills()
        else:
            logger.info("Waiting for skills directory to be set via set_skills_directory tool")

        # Start watching for changes
        self.start_watching()

        try:
            # Run the server
            logger.info("Starting MCP server...")
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise
        finally:
            self.stop_watching()
            logger.info("MCP server stopped")


def main():
    """Main entry point for the MCP server."""
    import sys
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="MCP Server for Claude Skills with progressive disclosure"
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help="Directory containing skill folders (default: auto-detect)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Configure logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Log startup information
    logger.info("="*60)
    logger.info("MCP Server for Claude Skills")
    logger.info("="*60)

    # Log configuration
    if args.skills_dir:
        logger.info(f"CLI skills directory: {args.skills_dir}")
    if os.getenv('MCP_SKILLS_DIR'):
        logger.info(f"ENV skills directory: {os.getenv('MCP_SKILLS_DIR')}")

    # Create and run server
    server = SkillMCPServer(skills_dir=args.skills_dir)

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
