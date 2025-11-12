# Open-ClaudeSkill

**MCP Server for Claude Skills with Progressive Disclosure**

Turn any MCP-compatible Agent into a Claude Skills powerhouse. This server enables environment-aware, hot-reloadable skill management across all MCP clients.

English | [简体中文](README.zh-CN.md)

## Features

- **Zero-Configuration Experience**: Skill files become services, automatically discovered and loaded
- **Real-Time Hot Reload**: File changes take effect immediately (depends on protocol features)
- **Environment Awareness**: Auto-detects project environments, supports global/project-level configs
- **Cross-Platform Compatible**: Standard MCP protocol, works with all Agent applications
- **Graceful Degradation**: Adapts to client capabilities automatically

## Quick Start

### Installation

```bash
# Install via uv (recommended)
uv pip install mcp-server-skill

# Or install from source
git clone https://github.com/your-org/open-claudeskill
cd open-claudeskill
uv pip install -e .
```

### Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uv",
      "args": ["run", "mcp-server-skill"]
    }
  }
}
```

### Creating Skills

1. Create a `.skill` directory in your project
2. Add skill folders with `SKILL.md` files:

```
.skill/
├── my-skill/
│   ├── SKILL.md          # Skill definition
│   └── templates/        # Optional resources
```

3. Define your skill in `SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does and when to use it
license: MIT
---

# Skill Instructions

Detailed instructions for the agent...
```

## Skill Format

Skills follow the official Claude Skill format:

### Frontmatter (YAML)

```yaml
---
name: skill-name          # Required: matches folder name
description: |            # Required: detailed description for agent matching
  What this skill does and when to use it.
  Include keywords that agents should match on.
license: MIT              # Optional: license information
---
```

### Skill Content

After the frontmatter, provide detailed Markdown instructions:

- Clear, actionable guidance
- Examples and best practices
- References to auxiliary resources

### Auxiliary Resources

Skills can include resources like templates, fonts, scripts:

```
.skill/
├── algorithmic-art/
│   ├── SKILL.md
│   └── templates/
│       ├── viewer.html
│       └── generator.js
```

Reference resources in your skill:

```markdown
Read `templates/viewer.html` using the Read tool
```

## Path Discovery

The server automatically finds skills using this priority:

1. **Command-line argument**: `--skills-dir /path/to/.skill`
2. **Environment variable**: `MCP_SKILLS_DIR=/path/to/.skill`
3. **Dynamic setting**: Via `set_skills_directory` tool
4. **Project-level**: `.skill/` in project root (detects `.git`, `package.json`, etc.)
5. **Global fallback**: `~/.skill`

## Usage

### For Type B Clients (with local agent capability)

Agents can set the skills directory dynamically:

```
Agent detects: User is in /path/to/project
Agent calls: set_skills_directory(path="/path/to/project")
Server responds: Discovered 5 skills: code-reviewer, calculator, ...
```

### For Type A Clients (without local agent capability)

Use global configuration:

```bash
mkdir ~/.skill
cp -r examples/code-reviewer ~/.skill/
```

## Tools Provided

### `set_skills_directory`

Set the skills directory for the current session.

**Parameters:**
- `path` (string): Absolute or relative path to project or `.skill` directory

**Example:**
```python
set_skills_directory(path="/path/to/project")
```

### `load_skill`

Load and activate a skill by name.

**Parameters:**
- `skill` (string): Name of the skill to load

**Example:**
```python
load_skill(skill="code-reviewer")
```

## Advanced Configuration

### Environment Variables

- `MCP_SKILLS_DIR`: Override default skills directory

### Command-Line Arguments

```bash
mcp-server-skill --skills-dir /custom/path --log-level DEBUG
```

### Logging

Set log level for debugging:

```bash
mcp-server-skill --log-level DEBUG
```

Levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Examples

See the `examples/` directory for sample skills:

- **algorithmic-art**: Create generative art using p5.js
- **canvas-design**: Design visual art and posters
- **brand-guidelines**: Apply Anthropic brand styling
- **code-reviewer**: Comprehensive code review framework
- **calculator**: Mathematical calculations

## Development

### Running from Source

```bash
# Install development dependencies
uv pip install -e .

# Run the server
uv run mcp-server-skill

# Run with debug logging
uv run mcp-server-skill --log-level DEBUG
```

### Creating Custom Skills

1. Copy an example skill as a template
2. Modify the frontmatter (name, description)
3. Update the instructions
4. Add any auxiliary resources
5. Test with your agent

## Architecture

### Core Components

- **ServerState**: Manages runtime state and path discovery
- **SkillLoader**: Discovers and parses skill files
- **SkillFileHandler**: Monitors file changes with debouncing
- **SkillMCPServer**: Main MCP server implementation

### Progressive Disclosure

Skills are exposed via a single `load_skill` tool that lists all available skills in its description. This minimizes initial token usage while providing full discovery.

### Hot Reload

File changes are detected via watchdog and trigger skill reloading. Changes take effect immediately for the next agent request.

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Resources

- **Documentation**: [Official Docs](https://github.com/your-org/open-claudeskill)
- **Agent Skills Spec**: [Anthropic Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)

---

**Made with ❤️ by the Open-ClaudeSkill community**
