# Quick Start Guide

Get up and running with Open-ClaudeSkill in 5 minutes!

## Step 1: Install (30 seconds)

### Option A: Using uvx (Recommended for Kilo Code)

No installation needed! Kilo Code will automatically download and run via uvx.

### Option B: Using pip

```bash
pip install mcp-server-skill
```

### Option C: From source

```bash
git clone https://github.com/your-org/open-claudeskill.git
cd open-claudeskill
pip install -e .
```

## Step 2: Configure Your Agent (1 minute)

### For Kilo Code

1. **Find your MCP settings file**:
   - Windows: `%APPDATA%\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json`
   - macOS: `~/Library/Application Support/Code/User/globalStorage/kilocode.kilo-code/settings/mcp_settings.json`
   - Linux: `~/.config/Code/User/globalStorage/kilocode.kilo-code/settings/mcp_settings.json`

2. **Add this configuration**:
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

3. **Restart Kilo Code**

### For Claude Desktop

Edit `claude_desktop_config.json`:

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

### For Other Agents

See [MCP_CONFIG.md](MCP_CONFIG.md) for platform-specific instructions.

## Step 3: Create Your First Skill (2 minutes)

1. **Create the skills directory**:
   ```bash
   mkdir -p .skill/hello-world
   ```

2. **Create a skill file** (`.skill/hello-world/SKILL.md`):
   ```markdown
   ---
   name: hello-world
   description: A friendly greeting skill. Use when users ask for greetings or want to test the skill system.
   ---

   # Hello World Skill

   This is your first skill!

   ## Instructions

   When invoked:
   1. Greet the user warmly
   2. Explain that this is a test skill
   3. Suggest they create their own skills
   4. Provide a link to the documentation

   ## Example

   "Hello! 👋 This is the Hello World skill. You've successfully set up the Open-ClaudeSkill system!

   This skill was loaded using progressive disclosure - I only saw its name and description until you triggered it. Now I have access to these detailed instructions.

   Ready to create your own skills? Check out the examples in the .skill directory or visit the documentation!"
   ```

## Step 4: Test It! (1 minute)

1. **Restart your agent** (if needed)

2. **Ask your agent**:
   ```
   What skills are available?
   ```

   You should see the hello-world skill listed.

3. **Invoke the skill**:
   ```
   Use the hello-world skill
   ```

   Your agent should greet you warmly!

## Step 5: Try a Real Skill (1 minute)

Let's add a useful skill from the examples:

1. **Copy an example skill**:
   ```bash
   cp -r examples/code-reviewer .skill/
   ```

   Or on Windows:
   ```cmd
   xcopy examples\code-reviewer .skill\code-reviewer\ /E /I
   ```

2. **Ask your agent**:
   ```
   Review this code for security issues:

   def login(username, password):
       query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
       return database.execute(query)
   ```

3. **Watch the magic happen!** Your agent will:
   - Recognize this is a code review task
   - Load the code-reviewer skill
   - Apply its comprehensive review framework
   - Identify the SQL injection vulnerability
   - Provide detailed fix recommendations

## What's Next?

### Create Your Own Skills

1. **Identify a repetitive task** you want to improve
2. **Create a skill directory**:
   ```bash
   mkdir -p .skill/my-skill
   ```
3. **Write the SKILL.md** following the template
4. **Test and iterate**

### Explore Examples

Check out the example skills:
- `examples/calculator/` - Simple calculation skill
- `examples/code-reviewer/` - Comprehensive code review
- Browse the official skills at [anthropics/skills](https://github.com/anthropics/skills)

### Import Official Skills

Download skills from the official repository:

```bash
cd .skill
git clone https://github.com/anthropics/skills.git
# Copy the skills you want
cp -r skills/mcp-builder ./
cp -r skills/skill-creator ./
```

### Join the Community

- **Share your skills**: Submit PRs with your creations
- **Get help**: GitHub Discussions
- **Report issues**: GitHub Issues
- **Chat**: Join our Discord

## Troubleshooting

### "No tools available"

- Verify MCP config syntax (use a JSON validator)
- Check `disabled: false`
- Restart your agent

### "Skill not found"

- Check skill folder name matches skill name in YAML
- Verify SKILL.md exists and is properly formatted
- Check server logs for parsing errors

### "Changes not reflected"

- Wait a moment for hot-reload (1-2 seconds)
- If it doesn't reload, restart the MCP server
- Check file permissions

### Server won't start

- Verify Python 3.10+ is installed
- Try running manually: `mcp-server-skill`
- Check for error messages

## Tips & Tricks

### Development Workflow

1. Create skill in `.skill/test/`
2. Test quickly by asking agent to use it
3. Iterate on SKILL.md
4. Hot-reload automatically updates it
5. Move to permanent location when ready

### Skill Organization

```
.skill/
├── work/
│   ├── code-reviewer/
│   ├── doc-writer/
│   └── meeting-notes/
├── personal/
│   ├── fitness-coach/
│   └── recipe-helper/
└── experiments/
    └── test-skill/
```

### Multiple Projects

Use different skill directories per project:

```json
{
  "mcpServers": {
    "skill-project-a": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/projects/a/.skill"]
    },
    "skill-project-b": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/projects/b/.skill"]
    }
  }
}
```

### Version Control

Add to `.gitignore`:
```
.skill/experiments/
.skill/personal/
```

Commit shared skills:
```
.skill/team/
```

## Success Checklist

- [ ] MCP server configured in agent
- [ ] Agent can list skills
- [ ] Successfully invoked hello-world skill
- [ ] Tested a real skill (like code-reviewer)
- [ ] Created your own custom skill
- [ ] Verified hot-reload works

## Get Help

- **Documentation**: [Full README](README.md)
- **Configuration**: [MCP_CONFIG.md](MCP_CONFIG.md)
- **Creating Skills**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/open-claudeskill/issues)

---

**Congratulations!** 🎉 You're now using the Open-ClaudeSkill system. Start creating skills and supercharge your AI agent!
