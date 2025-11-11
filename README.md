# Open-ClaudeSkill: Universal Skill System via MCP

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

**Open-ClaudeSkill** is an open-source implementation that brings Claude's powerful Skill system to any MCP-compatible AI agent. It enables **progressive disclosure** of specialized knowledge and capabilities, allowing agents to access domain expertise only when needed.

## 🎯 What is This?

Claude Code has a native "Skill" system that uses progressive disclosure:
- Skills are listed briefly in the system prompt (name + description)
- Full skill content loads only when invoked
- This saves tokens while providing specialized capabilities

**This project brings that capability to ANY agent** that supports MCP (Model Context Protocol), using a standard interface instead of proprietary function calls.

## ✨ Key Features

- **🔌 Universal Compatibility**: Works with any MCP-compatible agent (Kilo Code, Claude Desktop, Cline, Continue.dev, custom agents)
- **📁 Standard Format**: 100% compatible with official Claude Skill format
- **🔥 Hot-Reload**: Automatically detects changes to skills without restart
- **💾 Context-Efficient**: Progressive disclosure saves tokens by loading only when needed
- **🛠️ Easy Setup**: Works with `uvx` for zero-config deployment
- **🔒 Secure**: Skills run in your local environment

## 🚀 Quick Start

### For Kilo Code Users

1. **Install the MCP server** (one-time):
   ```bash
   pip install mcp-server-skill
   # or use uvx directly (no install needed)
   ```

2. **Configure MCP** in your `mcp_settings.json`:
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

3. **Create a skills directory**:
   ```bash
   mkdir -p .skill/my-first-skill
   ```

4. **Add a skill** (`.skill/my-first-skill/SKILL.md`):
   ```markdown
   ---
   name: my-first-skill
   description: A simple example skill for testing
   ---

   # My First Skill

   This skill demonstrates the system.

   ## Instructions
   When users ask about testing, explain this skill system!
   ```

5. **Test it**:
   - Restart Kilo Code
   - Ask: "What skills are available?"
   - Try: "Use the my-first-skill skill"

### For Other Platforms

See [MCP_CONFIG.md](MCP_CONFIG.md) for detailed setup instructions for:
- Claude Desktop
- Cline (VSCode)
- Continue.dev
- Custom MCP clients

## 📖 How It Works

### Architecture

```
┌─────────────────────────────────────────────────┐
│           MCP-Compatible Agent                   │
│         (Kilo Code, Claude Desktop, etc.)        │
└─────────────────┬───────────────────────────────┘
                  │ MCP Protocol
                  │
┌─────────────────▼───────────────────────────────┐
│         mcp-server-skill (This Project)          │
│  ┌────────────────────────────────────────┐     │
│  │  1. Scan .skill/ folder                │     │
│  │  2. Parse SKILL.md files               │     │
│  │  3. Generate available_skills XML      │     │
│  │  4. Watch for changes (hot-reload)     │     │
│  └────────────────────────────────────────┘     │
└─────────────────┬───────────────────────────────┘
                  │
                  │ File System Access
                  │
┌─────────────────▼───────────────────────────────┐
│              .skill/ Directory                   │
│  ├── calculator/                                 │
│  │   └── SKILL.md                               │
│  ├── code-reviewer/                              │
│  │   └── SKILL.md                               │
│  └── custom-skill/                               │
│      └── SKILL.md                                │
└──────────────────────────────────────────────────┘
```

### Progressive Disclosure Flow

1. **Initial State**: Agent sees only skill names and descriptions (embedded in tool description)
2. **User Request**: User asks for something that matches a skill description
3. **Agent Decision**: Agent recognizes the match and calls `load_skill` tool
4. **Content Loading**: Server returns full skill content (markdown instructions)
5. **Agent Execution**: Agent follows the detailed skill instructions

This saves context because full skill content is only loaded when needed!

## 📁 Skill Format

Skills follow the [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md):

```markdown
---
name: skill-name
description: Description of what the skill does and when to use it
license: MIT  # optional
allowed-tools:  # optional
  - Read
  - Write
metadata:  # optional
  author: "Your Name"
  version: "1.0"
---

# Skill Title

Your skill instructions in markdown...

## Sections

- Can include any markdown
- Code examples
- Best practices
- Workflows
```

### Required Fields
- `name`: Skill identifier (must match folder name)
- `description`: When/how the agent should use this skill

### Optional Fields
- `license`: License information
- `allowed-tools`: Pre-approved tools (for Claude Code)
- `metadata`: Custom key-value pairs

## 🎓 Creating Skills

### Simple Skill Example

```markdown
---
name: greeting-expert
description: Expert at crafting professional greetings in multiple languages. Use when users need formal or cultural greetings.
---

# Greeting Expert Skill

## Capabilities
- Formal business greetings
- Cultural sensitivity considerations
- Multi-language greetings
- Context-appropriate salutations

## Guidelines
1. Ask about context (business, casual, cultural background)
2. Provide 2-3 options
3. Explain cultural nuances
4. Include pronunciation if non-English
```

### Complex Skill Example

See [.skill/code-reviewer/SKILL.md](.skill/code-reviewer/SKILL.md) for a comprehensive example with:
- Security checklists
- Multi-dimensional review framework
- Language-specific guidelines
- Example outputs

### Tips for Good Skills

1. **Clear Description**: Make it easy for agents to know when to use the skill
2. **Structured Content**: Use headings, lists, and sections
3. **Actionable Instructions**: Be specific about what to do
4. **Examples**: Show don't just tell
5. **Edge Cases**: Cover common pitfalls
6. **Context**: Explain the "why" not just the "how"

## 🔧 Configuration

### Default Configuration

By default, skills are loaded from `.skill/` in the current working directory.

### Custom Skills Directory

```bash
mcp-server-skill --skills-dir /path/to/your/skills
```

In MCP config:
```json
{
  "command": "uvx",
  "args": ["mcp-server-skill", "--skills-dir", "/custom/path"]
}
```

### Multiple Skill Sources

Run multiple instances for different skill sets:

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

## 🧪 Testing

### Manual Testing

1. **Start the server**:
   ```bash
   mcp-server-skill
   ```

2. **Create a test skill** in `.skill/test/SKILL.md`

3. **Test discovery**: Server should log "Loaded X skills"

4. **Test hot-reload**: Modify the SKILL.md and watch for reload message

### Integration Testing

Use the provided examples:

```bash
# Create example skills
mkdir -p .skill
cp -r examples/calculator .skill/
cp -r examples/code-reviewer .skill/

# Test with your agent
# Ask: "What skills do you have?"
# Try: "Use the calculator skill to compute 123 * 456"
```

## 🎯 Use Cases

### Software Development
- **code-reviewer**: Comprehensive code review with security focus
- **test-generator**: Generate unit tests
- **documentation-writer**: Technical documentation best practices
- **refactoring-guide**: Code improvement strategies

### Content Creation
- **technical-writer**: Technical writing guidelines
- **blog-optimizer**: SEO and readability improvement
- **social-media**: Platform-specific content optimization

### Data & Analysis
- **data-analyst**: Statistical analysis workflows
- **visualization-expert**: Data visualization best practices
- **sql-optimizer**: Query optimization techniques

### Domain-Specific
- **legal-reviewer**: Legal document review checklist
- **medical-coder**: Medical coding assistance
- **financial-analyst**: Financial analysis frameworks

## 🤝 Contributing

We welcome contributions!

### Adding Your Skill

1. Create a skill following the format
2. Test it locally
3. Submit a PR with your skill in `examples/`

### Improving the Server

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a PR

### Skill Sharing

Share your skills with the community:
- Tag with `#open-claudeskill`
- Include use case and examples
- Document any special requirements

## 📚 Documentation

- **[MCP_CONFIG.md](MCP_CONFIG.md)**: Detailed configuration for all platforms
- **[AGENT_PROMPT.md](AGENT_PROMPT.md)**: System prompt template for agents
- **[Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)**: Official skill format specification

## 🔍 Troubleshooting

### Skills Not Loading

```bash
# Check directory
ls .skill/

# Check format
cat .skill/your-skill/SKILL.md

# Test server
mcp-server-skill --skills-dir .skill
```

### Tool Not Appearing in Agent

1. Restart your MCP client
2. Check `mcp_settings.json` syntax
3. Verify `disabled: false`
4. Check server logs

### Hot-Reload Not Working

- Verify file permissions
- Check if server is watching correct directory
- Restart MCP server if needed

## 🛣️ Roadmap

- [ ] Skill templates generator
- [ ] Skill validation tool
- [ ] Skill marketplace/registry
- [ ] Version management for skills
- [ ] Skill dependencies
- [ ] Remote skill repositories
- [ ] Skill analytics (usage tracking)
- [ ] Web UI for skill management

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Claude Code's Skill system](https://claude.ai/code)
- Built on [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Uses the [Agent Skills Spec](https://github.com/anthropics/skills)

## 🔗 Links

- **Documentation**: [Full docs](docs/)
- **Examples**: [Skill examples](examples/)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Official Skills**: [anthropics/skills](https://github.com/anthropics/skills)

## 💬 Community

- **Issues**: [GitHub Issues](https://github.com/your-org/open-claudeskill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/open-claudeskill/discussions)
- **Discord**: [Join our community](https://discord.gg/your-invite)

---

**Made with ❤️ by the Open-ClaudeSkill community**

If you find this useful, please ⭐ star the repo and share with others!
