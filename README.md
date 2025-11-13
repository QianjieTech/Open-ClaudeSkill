# AgentSkill MCP

**Bring Claude Agent Skills to ANY MCP-compatible Agent**

A universal MCP server that enables **any** Agent application with MCP support to use Anthropic's official [Claude Agent Skills](https://github.com/anthropics/skills) with **progressive disclosure** - reducing context overhead while maximizing capability.

**Package Name**: `agentskill-mcp` | **PyPI**: [agentskill-mcp](https://pypi.org/project/agentskill-mcp/)

English | [简体中文](README.zh-CN.md)

## Why AgentSkill MCP?

Claude Agent Skills are brilliantly designed but locked to Claude's ecosystem. This project breaks that limitation by:

- ✅ **Universal Compatibility**: Works with ANY MCP-compatible agent (Kilo Code, Cursor, Roo Code, Codex, and more)
- ✅ **100% Claude Skill Compatible**: Uses official Anthropic Skill format - no modifications needed
- ✅ **Progressive Disclosure**: Implements the same smart context loading as Claude Code
- ✅ **Zero Lock-in**: Standard MCP protocol means you're never tied to one platform

### The Problem Skills Solve

Traditional MCP tools load ALL documentation upfront, consuming massive amounts of tokens before you even start. With 15+ tools, your agent is context-starved before doing any real work.

**Skills fix this** through progressive disclosure: agents see a lightweight skill list initially, then load full details only when needed. This project brings that same efficiency to every MCP-compatible agent.

## Features

- 🚀 **One-Line Installation**: `pip install agentskill-mcp` or `uvx agentskill-mcp`
- 🔌 **Universal MCP Compatibility (gradual testing)**: Works with Kilo Code, Cursor, Roo Code, Codex, Cherry Studio, and any MCP-compatible agent
- 📦 **Official Skill Format**: Fully compatible with [Anthropic's Claude Skills](https://github.com/anthropics/skills)
- 🎯 **Progressive Disclosure**: Smart context loading - minimal overhead until skills are needed
- 🔄 **Hot Reload (not yet implemented)**: File changes detected and updated in real-time (where protocol supported)
- 🗂️ **Smart Path Discovery**: Auto-detects `.claude/skills/`, `.skill/`, or custom directories
- 🌍 **Environment Aware**: Project-level and global skill directories with automatic detection
- 🎨 **ClaudeCode Compatible**: Supports both `.claude/skills/` (ClaudeCode format) and `.skill/` (custom format for this project)

## Project Status

⚠️ **Early Development** - This project is in early stages. Currently tested on Windows only.

**Tested Platforms:**
- ✅ **Kilo Code** (AI coding assistant) - Windows
- ✅ **Roo Code** (AI coding assistant) - Windows
- ✅ **Cline** (AI coding assistant) - Windows

**Next Steps:**
- 🔄 Testing on more MCP-compatible agents (Codex, Cursor, QwenCode, etc.)
- 🔄 Cross-platform testing (macOS, Linux)
- 🔄 Broader compatibility verification
- 🔄 Hot reload feasibility testing (based on MCP's List Changed Notification) see:
https://modelcontextprotocol.io/specification/2025-06-18/server/tools#list-changed-notification

**In theory**: Any agent implementing the [Model Context Protocol](https://modelcontextprotocol.io) should work, but we're actively testing to confirm.

## Quick Start

### Configuration

⚠️ **Current Recommended Usage**: Specify skills directory via `--skills-dir` parameter

Add to your MCP client configuration file. Find the configuration location in your agent's documentation:
- **Kilo Code**: `.kilocode/mcp.json` in your workspace
- **Roo Code**: Check agent documentation
- **Cursor**: `.cursor/mcp.json` in your workspace
- **Other agents**: Refer to agent-specific MCP configuration guide

**Recommended Configuration (Windows):**

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\Users\\YourName\\path\\to\\skills"
      ]
    }
  }
}
```

**For macOS/Linux:**

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "/Users/YourName/path/to/skills"
      ]
    }
  }
}
```

**Using pip-installed version:**

Replace `"command": "uvx"` with `"command": "agentskill-mcp"` and remove it from args:

```json
{
  "mcpServers": {
    "skills": {
      "command": "agentskill-mcp",
      "args": [
        "--skills-dir",
        "C:\\Users\\YourName\\path\\to\\skills"
      ]
    }
  }
}
```

💡 **Tips**:
- Use absolute paths in `--skills-dir` to avoid ambiguity
- After configuration changes, restart your agent application or reload MCP servers
- Test with `examples/` directory first before creating custom skills

### Loading Skills

Create a skills directory and add skill packages:

**Format 1: ClaudeCode Format (Recommended for ClaudeCode users)**

```bash
# Create in current project (recommended)
Create .claude/skills/ in project root directory

# Or create globally
mkdir -p ~/.claude/skills    # Linux/Mac
mkdir C:\Users\YourName\.claude\skills  # Windows
```

**Format 2: Custom Format for This Project (Compatible with other agents)**

```bash
# Create in current project
Create .skill/ in project root directory

# Or create globally
mkdir ~/.skill         # Linux/Mac
mkdir C:\Users\YourName\.skill  # Windows
```

Then place your Skill packages in the skills directory. The `./examples` directory contains several official Anthropic Skill packages, which are sufficient for testing.

```bash
# Example of migrating skills (ClaudeCode format)
Copy examples/canvas-design -> .claude/skills/
Copy examples/brand-guidelines -> .claude/skills/

# Or (Custom format for this project)
Copy examples/canvas-design -> .skill/
Copy examples/brand-guidelines -> .skill/
```

The final structure should look like:
- ClaudeCode format: **`.claude/skills/canvas-design/`**
- Custom format for this project: **`.skill/canvas-design/`**

### Try It Out

Restart your Agent application and test with:

```
Create a 1920x1080 promotional poster using Anthropic brand style.
Theme: "AI belongs to the future? AI is just a means, not an end"
```

**What happens:**
1. Agent sees available skills in the `load_skill` tool description
2. Agent identifies relevant skills (`canvas-design`, `brand-guidelines`)
3. Agent calls `load_skill` to get full skill details
4. Agent follows skill instructions to create the poster

**Note**: The agent may call only one skill depending on how it interprets the task. This is normal - AI agents have some inherent randomness in tool selection.

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
# ClaudeCode format
.claude/skills/
├── algorithmic-art/
│   ├── SKILL.md
│   └── templates/
│       ├── viewer.html
│       └── generator.js

# Or legacy format
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

## How It Works

### Progressive Disclosure Implementation

**The Challenge**: How to implement progressive disclosure within the MCP framework?

**Official Claude Implementation** (inferred from behavior):
- Built-in Skill system integrated in agent's system prompt
- Initial display shows only `<available_skills>` list
- Special `load_skill` command triggers full content loading

**Our MCP Implementation**:

1. **Single MCP Tool: `load_skill`**
   - Embeds all available skill metadata in the tool's `description`
   - Agents see the skill list without loading full content

2. **Tool Description Structure**:
```xml
Tool(
    name="load_skill",
    description="""Execute a skill within the main conversation

<skills_instructions>
When users ask you to perform tasks, check if any of the
available skills below can help...
</skills_instructions>

<available_skills>
<skill>
  <name>code-reviewer</name>
  <description>Comprehensive code review framework...</description>
</skill>
<skill>
  <name>calculator</name>
  <description>Mathematical calculations...</description>
</skill>
</available_skills>
""",
    inputSchema={
        "type": "object",
        "properties": {
            "skill": {"type": "string"}
        }
    }
)
```

3. **On-Demand Loading**:
   - Agent matches task with skills from `<available_skills>`
   - Calls `load_skill(skill="code-reviewer")`
   - Server reads `.skill/code-reviewer/SKILL.md`
   - Returns full skill content

### Current Implementation Note

**Version 0.1.3** focuses on the most reliable usage pattern:

- ✅ **Recommended**: Specify skills directory via `--skills-dir` parameter
- ⚠️ **Experimental**: Dynamic `set_skills_directory` tool (currently disabled in production)

This approach ensures maximum compatibility across different agent implementations while we continue testing and refining more advanced features.

## Path Discovery

The server automatically finds skills using this priority:

1. **Command-line argument**: `--skills-dir /path/to/skills` ⭐ **Recommended**
2. **Environment variable**: `MCP_SKILLS_DIR=/path/to/skills`
3. **Project-level**: `.claude/skills/` or `.skill/` in project root (detects `.git`, `.claude/`, `package.json`, etc.)
4. **Global fallback**: `~/.skill`

**Note**: The project-level discovery prioritizes `.claude/skills/` (ClaudeCode format) over `.skill/` (custom format for this project) when both exist.

**Current Recommendation**: Always use `--skills-dir` parameter for best compatibility.

## Usage Examples

### Example 1: Using Absolute Path (Recommended)

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\userfolder\\DevFolder\\my-skills"
      ]
    }
  }
}
```

### Example 2: Using Project Examples

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\path\\to\\Open-ClaudeSkill\\examples"
      ]
    }
  }
}
```

## Tools Provided

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
agentskill-mcp --skills-dir /custom/path --log-level DEBUG
```

### Logging

Set log level for debugging:

```bash
agentskill-mcp --log-level DEBUG
```

Levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Examples

See the `examples/` directory for sample skills:

- **algorithmic-art**: Create generative art using p5.js
- **canvas-design**: Design visual art and posters
- **brand-guidelines**: Apply Anthropic brand styling
- **code-reviewer**: Comprehensive code review framework
- **calculator**: Mathematical calculations

### Installation

**Method 1: Using pip (Recommended)**

```bash
pip install agentskill-mcp
```

**Method 2: Using uvx (No installation needed for trial)**

```bash
# Run directly without installing
uvx agentskill-mcp --help
```

**Method 3: Using uv**

```bash
uv pip install agentskill-mcp
```

**Verify Installation:**

```bash
agentskill-mcp --help

# Expected output:
# usage: agentskill-mcp [-h] [--skills-dir SKILLS_DIR]
#                       [--log-level {DEBUG,INFO,WARNING,ERROR}]
#
# AgentSkill MCP - MCP Server for Claude Skills with progressive disclosure
```

**For Development** (if you want to modify the code):

```bash
git clone https://github.com/QianjieTech/Open-ClaudeSkill.git
cd Open-ClaudeSkill
pip install -e .
```

## Development

### Running from Source

```bash
# Install development dependencies
uv pip install -e .

# Run the server
uv run agentskill-mcp

# Run with debug logging
uv run agentskill-mcp --log-level DEBUG
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

**Note**: Hot reload functionality is implemented in the codebase but not yet verified to work reliably across all MCP-compatible agents in practice.

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Resources

- **Documentation**: [Official Docs](https://github.com/your-org/open-claudeskill)
- **Agent Skills Spec**: [Anthropic Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Issues**: [GitHub Issues](https://github.com/your-org/open-claudeskill/issues)

## Acknowledgments

This project is built upon the following open-source projects:

- [MCP (Model Context Protocol)](https://modelcontextprotocol.io) - Anthropic
- [Claude Skills](https://www.anthropic.com/news/claude-code-skills) - Anthropic
- [watchdog](https://github.com/gorakhargosh/watchdog) - File system monitoring
- [PyYAML](https://pyyaml.org/) - YAML parsing

## Contact

QQ Group: 1065081197

---

**Made with ❤️ by the Open-ClaudeSkill community**
