# 📚 Documentation Navigation

## 🎯 I Want To...

### Get Started
→ **[QUICKSTART.md](QUICKSTART.md)** - 5 minutes to get running
→ **[README.md](README.md)** - Full introduction (English)
→ **[README.zh-CN.md](README.zh-CN.md)** - 完整介绍（中文）

### Configure My Platform
→ **[MCP_CONFIG.md](MCP_CONFIG.md)** - All platforms (Claude Desktop, Cline, Continue.dev, etc.)
→ **[KILOCODE_SETUP.md](KILOCODE_SETUP.md)** - Kilo Code specific setup
→ **[AGENT_PROMPT.md](AGENT_PROMPT.md)** - System prompt template for agents

### Develop & Contribute
→ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design and implementation
→ **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute code or skills
→ **[examples/README.md](examples/README.md)** - Create your own skills

### Publish & Release
→ **[PUBLISH_GUIDE.md](PUBLISH_GUIDE.md)** - Publish to PyPI
→ **[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** - Release process
→ **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Manage Repository
→ **[GITHUB_DESCRIPTION.md](GITHUB_DESCRIPTION.md)** - Repository descriptions & marketing
→ **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project organization

---

## 📂 Directory Guide

```
📁 Root Level Documents
├── 👤 For Users
│   ├── README.md              Complete guide (English)
│   ├── README.zh-CN.md        完整指南（中文）
│   ├── QUICKSTART.md          5-minute setup
│   ├── MCP_CONFIG.md          Platform configuration
│   └── KILOCODE_SETUP.md      Kilo Code guide
│
├── 🛠️ For Developers
│   ├── ARCHITECTURE.md        Technical docs
│   ├── CONTRIBUTING.md        Contribution guide
│   ├── PUBLISH_GUIDE.md       Publishing guide
│   └── RELEASE_CHECKLIST.md   Release process
│
├── 📋 For Maintainers
│   ├── GITHUB_DESCRIPTION.md  Repository content
│   ├── PROJECT_STRUCTURE.md   File organization
│   ├── CHANGELOG.md           Version history
│   └── NAVIGATION.md          This file
│
└── 🔧 Configuration
    ├── AGENT_PROMPT.md        System prompt
    ├── mcp_settings.example.json
    └── pyproject.toml

📁 src/mcp_server_skill/
└── Python source code

📁 examples/
└── Example skills with README

📁 scripts/
└── Helper batch files

📁 .github/workflows/
└── CI/CD configuration

📁 docs/
└── Documentation portal

📁 archive/
└── Reference materials (not for distribution)
```

---

## 🎓 Learning Path

### Path 1: End User (Want to use skills)
1. Read [README.md](README.md) - Overview
2. Follow [QUICKSTART.md](QUICKSTART.md) - Setup
3. Check [MCP_CONFIG.md](MCP_CONFIG.md) - Configure your platform
4. Try example skills in `.skill/`

### Path 2: Skill Creator (Want to create skills)
1. Read [README.md](README.md) - Understand the system
2. Check [examples/README.md](examples/README.md) - Learn skill format
3. Read [CONTRIBUTING.md](CONTRIBUTING.md) - Best practices
4. Create and test your skill

### Path 3: Developer (Want to contribute code)
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) - Understand design
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) - Guidelines
3. Setup development environment
4. Submit improvements

### Path 4: Maintainer (Want to publish/release)
1. Read [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) - Publishing process
2. Follow [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Pre-release steps
3. Update [CHANGELOG.md](CHANGELOG.md) - Version notes
4. Use [GITHUB_DESCRIPTION.md](GITHUB_DESCRIPTION.md) - Marketing content

---

## 🔍 Quick Reference

| Task | Document |
|------|----------|
| Install | [README.md](README.md#quick-start) |
| Configure Kilo Code | [KILOCODE_SETUP.md](KILOCODE_SETUP.md) |
| Configure Other Platforms | [MCP_CONFIG.md](MCP_CONFIG.md) |
| Create Skill | [examples/README.md](examples/README.md) |
| Understand Design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Publish | [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) |
| Get System Prompt | [AGENT_PROMPT.md](AGENT_PROMPT.md) |

---

## 📦 What's Where?

### Documentation (13 files)
- Core: README.md, README.zh-CN.md, QUICKSTART.md
- Config: MCP_CONFIG.md, KILOCODE_SETUP.md, AGENT_PROMPT.md
- Developer: ARCHITECTURE.md, CONTRIBUTING.md
- Release: PUBLISH_GUIDE.md, RELEASE_CHECKLIST.md, CHANGELOG.md
- Meta: GITHUB_DESCRIPTION.md, PROJECT_STRUCTURE.md, NAVIGATION.md

### Source Code
- src/mcp_server_skill/*.py (3 files)

### Configuration
- pyproject.toml, setup.py, MANIFEST.in, Makefile
- mcp_settings.example.json
- .gitignore, LICENSE

### Examples
- .skill/example-calculator/, .skill/code-reviewer/
- examples/ (distributable versions)

### Scripts
- scripts/install_for_kilocode.bat
- scripts/run_skill_server.bat
- scripts/setup_local.bat

### Testing
- test_installation.py

### CI/CD
- .github/workflows/ci.yml
- .github/workflows/publish.yml

### Archive
- archive/ (reference materials, not for release)

---

## 🌟 Most Important Files

**Must Read:**
1. [README.md](README.md) - Start here!
2. [QUICKSTART.md](QUICKSTART.md) - Get running fast
3. [MCP_CONFIG.md](MCP_CONFIG.md) - Configure your platform

**For Development:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the system
2. [CONTRIBUTING.md](CONTRIBUTING.md) - Contribute properly

**For Publishing:**
1. [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) - Publish to PyPI
2. [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Don't forget anything

---

**Lost?** Start with [README.md](README.md) 📖
