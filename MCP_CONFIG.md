# MCP Configuration Guide

This guide shows how to configure the `mcp-server-skill` for different MCP-compatible platforms.

## Installation

### Using uvx (Recommended for Kilo Code)

```bash
uvx mcp-server-skill
```

### Using pip

```bash
pip install mcp-server-skill
```

### From Source

```bash
git clone https://github.com/your-org/open-claudeskill.git
cd open-claudeskill
pip install -e .
```

---

## Configuration by Platform

### Kilo Code

Kilo Code only supports `uvx` command for MCP servers.

**Configuration File**: `mcp_settings.json`

**Location**:
- Windows: `%APPDATA%\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/kilocode.kilo-code/settings/mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/kilocode.kilo-code/settings/mcp_settings.json`

**Configuration**:

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

**With Custom Skills Directory**:

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill",
        "--skills-dir",
        "/path/to/your/skills"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

---

### Claude Desktop

**Configuration File**: `claude_desktop_config.json`

**Location**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration**:

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": ["mcp-server-skill"]
    }
  }
}
```

**Using Python directly**:

```json
{
  "mcpServers": {
    "skill": {
      "command": "python",
      "args": ["-m", "mcp_server_skill.server"]
    }
  }
}
```

---

### Cline (VSCode Extension)

**Configuration File**: VSCode settings or Cline MCP settings

**Method 1: VSCode settings.json**:

```json
{
  "cline.mcpServers": {
    "skill": {
      "command": "uvx",
      "args": ["mcp-server-skill"]
    }
  }
}
```

**Method 2: Cline Settings UI**:
1. Open Cline settings
2. Navigate to MCP Servers
3. Add new server:
   - Name: `skill`
   - Command: `uvx`
   - Args: `["mcp-server-skill"]`

---

### Continue.dev

**Configuration File**: `config.json` in Continue directory

**Location**:
- macOS/Linux: `~/.continue/config.json`
- Windows: `%USERPROFILE%\.continue\config.json`

**Configuration**:

```json
{
  "mcpServers": [
    {
      "name": "skill",
      "command": "uvx",
      "args": ["mcp-server-skill"]
    }
  ]
}
```

---

### Custom MCP Client

For custom implementations using the MCP SDK:

**Python**:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-skill"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()

            # Call tool
            result = await session.call_tool("load_skill", {"skill": "example"})
            print(result)
```

**TypeScript**:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "uvx",
  args: ["mcp-server-skill"],
});

const client = new Client({
  name: "skill-client",
  version: "1.0.0",
}, {
  capabilities: {}
});

await client.connect(transport);

// List tools
const tools = await client.listTools();

// Call tool
const result = await client.callTool({
  name: "load_skill",
  arguments: { skill: "example" }
});
```

---

## Configuration Options

### Command-Line Arguments

```bash
mcp-server-skill [OPTIONS]
```

**Options**:

- `--skills-dir PATH`: Directory containing skill folders
  - Default: `.skill` in current working directory
  - Example: `--skills-dir ~/my-skills`

### Environment Variables

You can also use environment variables:

```bash
export SKILLS_DIR=/path/to/skills
mcp-server-skill
```

---

## Skills Directory Setup

### Default Location

By default, the server looks for skills in `.skill/` in the current working directory.

**Example structure**:

```
your-project/
├── .skill/
│   ├── pdf-processor/
│   │   └── SKILL.md
│   ├── data-analyzer/
│   │   └── SKILL.md
│   └── code-reviewer/
│       └── SKILL.md
└── other-files...
```

### Custom Location

Specify a custom location:

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill",
        "--skills-dir",
        "~/Documents/my-skills"
      ]
    }
  }
}
```

### Multiple Skill Directories

To use multiple skill directories, you can run multiple instances:

```json
{
  "mcpServers": {
    "skill-work": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/work-skills"]
    },
    "skill-personal": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/personal-skills"]
    }
  }
}
```

---

## Troubleshooting

### Server Not Starting

1. **Check uvx installation**:
   ```bash
   uvx --version
   ```

2. **Test server manually**:
   ```bash
   uvx mcp-server-skill
   ```

3. **Check Python version** (requires Python 3.10+):
   ```bash
   python --version
   ```

### Skills Not Loading

1. **Verify skills directory exists**:
   ```bash
   ls .skill/
   ```

2. **Check SKILL.md format**:
   - Must start with `---`
   - Must have `name` and `description` in frontmatter
   - Name must match folder name

3. **Check server logs** for parsing errors

### Tool Not Appearing

1. **Restart your MCP client** (Kilo Code, Claude Desktop, etc.)
2. **Verify MCP server is enabled** (`disabled: false`)
3. **Check alwaysAllow** includes `load_skill`

### Hot-Reload Not Working

The server automatically watches for changes. If changes aren't detected:

1. **Check file permissions** on the skills directory
2. **Restart the MCP server**
3. **Verify file paths** are correct

---

## Advanced Configuration

### Auto-Approve Tool Calls

To avoid prompting for tool approval every time:

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": ["mcp-server-skill"],
      "alwaysAllow": ["load_skill"],
      "disabled": false
    }
  }
}
```

### Using with Docker

```dockerfile
FROM python:3.11-slim

RUN pip install mcp-server-skill

COPY .skill /app/.skill
WORKDIR /app

CMD ["mcp-server-skill"]
```

### Using with PM2 (for long-running servers)

```json
{
  "apps": [{
    "name": "mcp-skill-server",
    "script": "mcp-server-skill",
    "interpreter": "python",
    "env": {
      "SKILLS_DIR": "/path/to/skills"
    }
  }]
}
```

---

## Testing Your Configuration

1. **Start your MCP client** (Kilo Code, Claude Desktop, etc.)

2. **Check if tools are available**:
   - Ask: "What tools do you have access to?"
   - Should see `load_skill` tool

3. **List available skills**:
   - Ask: "What skills are available?"
   - Agent should list skills from your `.skill` directory

4. **Test loading a skill**:
   - Ask: "Load the [skill-name] skill"
   - Should see the full skill content

5. **Test hot-reload**:
   - Modify a SKILL.md file
   - Load the skill again
   - Changes should be reflected

---

## Getting Help

- **Documentation**: [GitHub README](https://github.com/your-org/open-claudeskill)
- **Issues**: [GitHub Issues](https://github.com/your-org/open-claudeskill/issues)
- **Examples**: See `examples/` directory in the repository
