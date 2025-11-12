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

> **⚠️ Current Status**: This project is not yet published to PyPI. You cannot use `uvx mcp-server-skill` directly at this time. We will publish to PyPI soon to enable simple one-line installation. For now, please follow the installation guide below.

**Project Repository**: https://github.com/QianjieTech/Open-ClaudeSkill

### Step 1: Clone the Repository

```bash
git clone https://github.com/QianjieTech/Open-ClaudeSkill.git
cd Open-ClaudeSkill
```

### Step 2: Installation

**Method A: Using System Python**

```bash
pip install -e .
```

This installs the `mcp-server-skill` command to your system Python's Scripts directory, which is usually in PATH.

**Method B: Using uv (Recommended for Developers)**

If using uv, the command won't be automatically added to PATH. You'll need to use `uv run`:

```bash
uv venv
uv pip install -e .
```

**Verify Installation:**

```bash
# After Method A installation
mcp-server-skill --help

# After Method B installation (requires uv run)
uv run mcp-server-skill --help

# If successful, you should see:
usage: mcp-server-skill [-h] [--skills-dir SKILLS_DIR] [--log-level {DEBUG,INFO,WARNING,ERROR}]

MCP Server for Claude Skills with progressive disclosure

options:
  -h, --help            show this help message and exit
  --skills-dir SKILLS_DIR
                        Directory containing skill folders (default: auto-detect)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level (default: INFO)
```

### Step 3: Configure MCP Client

Choose the configuration based on your Agent application and installation method:

#### Kilo Code (Recommended, Verified)

**If using Method A (System Python):**

```json
{
  "mcpServers": {
    "skills": {
      "command": "mcp-server-skill",
      "args": []
    }
  }
}
```

**If using Method B (uv):**

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

**When to specify `--skills-dir`:**

- MCP server starts in a directory other than the project directory

**If your agent supports project-level MCP configuration**, configuring this MCP tool at the project level will automatically load skills from `.skill/` in the current directory. Otherwise, you need to specify the skill directory via the `--skills-dir` parameter.

💡 **Tip**: If Kilo Code doesn't load skills after configuring project-level MCP, manually click the "Refresh MCP Server" button or restart VSCode.

#### QwenCode

Edit config file: `C:\Users\YourUserName\.qwen\settings.json` (Windows)

Add the following (QwenCode seems to only support global MCP settings, so you need to manually specify the skill directory):

**System Python Installation:**

```json
{
  "mcpServers": {
    "skills": {
      "command": "mcp-server-skill",
      "args": ["--skills-dir", "C:\\Users\\YourName\\.skill"]
    }
  }
}
```

### Step 4: Load Skills

Create a `.skill` folder in your project root or global directory:

```bash
# Create in current project (recommended)
Create .skill/ in project root directory

# Or create globally
mkdir ~/.skill         # Linux/Mac
mkdir C:\Users\YourName\.skill  # Windows
```

Then place your Skill packages in this directory - simply copy Skill folders into the `.skill/` folder. The `./examples` directory contains several official Anthropic Skill packages, which are sufficient for Step 5 testing.

```bash
# Example of migrating skills
Copy examples/canvas-design -> .skill/
Copy examples/brand-guidelines -> .skill/
```

The final structure should look like: **`.skill/canvas-design/`**

### Step 5: Test the Experience

Restart your Agent application, then enter in the conversation:

```
Create a 1920*1080 promotional poster using Anthropic brand style. Theme: "AI belongs to the future?\nAI is just a means, not an end"
```

If everything works correctly, the Agent will:
1. Recognize that you have `canvas-design` and `brand-guidelines` skills
2. Automatically call the `load_skill` tool
3. Create a poster following the guidance in the Skills

*Note: It might only call one of these skills, depending on the model's understanding of the task. This has some randomness. In my tests, at least one of these 2 skills is called.*

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
