# Project Structure

## 📁 Directory Layout

```
Open-ClaudeSkill/
│
├── 📄 Core Documentation
│   ├── README.md                   Main documentation (English)
│   ├── README.zh-CN.md             Main documentation (Chinese)
│   ├── QUICKSTART.md               5-minute quick start
│   ├── LICENSE                     MIT License
│   └── CHANGELOG.md                Version history
│
├── ⚙️ Configuration Guides
│   ├── MCP_CONFIG.md               All platforms configuration
│   ├── KILOCODE_SETUP.md           Kilo Code specific setup
│   ├── mcp_settings.example.json   Example MCP configuration
│   └── AGENT_PROMPT.md             System prompt template
│
├── 🏗️ Developer Documentation
│   ├── ARCHITECTURE.md             Technical architecture
│   ├── CONTRIBUTING.md             Contribution guidelines
│   ├── PUBLISH_GUIDE.md            Publishing to PyPI
│   ├── RELEASE_CHECKLIST.md        Release process
│   └── GITHUB_DESCRIPTION.md       Repository descriptions
│
├── 💻 Source Code
│   └── src/mcp_server_skill/
│       ├── __init__.py             Package initialization
│       ├── server.py               MCP server implementation
│       └── skill_loader.py         Skill discovery & parsing
│
├── 🎓 Example Skills
│   ├── .skill/                     Default skills directory
│   │   ├── example-calculator/
│   │   └── code-reviewer/
│   └── examples/                   Distributable examples
│       ├── calculator/
│       ├── code-reviewer/
│       └── README.md
│
├── 🔧 Configuration Files
│   ├── pyproject.toml              Python package config
│   ├── setup.py                    Setup script
│   ├── MANIFEST.in                 Package manifest
│   ├── Makefile                    Development commands
│   └── .gitignore                  Git ignore rules
│
├── 🧪 Testing & Scripts
│   ├── test_installation.py        Installation test
│   └── scripts/
│       ├── install_for_kilocode.bat
│       ├── run_skill_server.bat
│       └── setup_local.bat
│
├── 🔄 CI/CD
│   └── .github/workflows/
│       ├── ci.yml                  Continuous integration
│       └── publish.yml             Auto-publish to PyPI
│
├── 📚 Documentation Portal
│   └── docs/
│       └── README.md               Documentation index
│
└── 📦 Archive
    └── archive/                    Old/reference documents
        ├── SKILL_DES.md
        ├── SKILL_hu.md
        ├── PROJECT_SUMMARY.md
        ├── PROJECT_OVERVIEW.md
        ├── DELIVERY.md
        ├── CURRENT_STATUS.md
        ├── LOCAL_TESTING.md
        ├── KILOCODE_LOCAL_CONFIG.md
        └── START_HERE.md
```

---

## 📖 Quick Reference

### For Users

| Need | Document |
|------|----------|
| Get started | [QUICKSTART.md](QUICKSTART.md) |
| Full guide | [README.md](README.md) or [README.zh-CN.md](README.zh-CN.md) |
| Configure agent | [MCP_CONFIG.md](MCP_CONFIG.md) |
| Kilo Code setup | [KILOCODE_SETUP.md](KILOCODE_SETUP.md) |
| System prompt | [AGENT_PROMPT.md](AGENT_PROMPT.md) |

### For Developers

| Need | Document |
|------|----------|
| Understand design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Contribute code | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Create skills | [examples/README.md](examples/README.md) |
| Publish package | [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) |
| Release process | [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) |

### For Repository Managers

| Need | Document |
|------|----------|
| GitHub descriptions | [GITHUB_DESCRIPTION.md](GITHUB_DESCRIPTION.md) |
| Version history | [CHANGELOG.md](CHANGELOG.md) |
| Project structure | This file |

---

## 🗂️ File Categories

### Essential (Must Keep)

**User Documentation:**
- README.md
- README.zh-CN.md
- QUICKSTART.md
- MCP_CONFIG.md
- KILOCODE_SETUP.md

**Source Code:**
- src/mcp_server_skill/*
- pyproject.toml
- LICENSE

**Examples:**
- .skill/
- examples/

### Important (Should Keep)

**Developer Docs:**
- ARCHITECTURE.md
- CONTRIBUTING.md
- PUBLISH_GUIDE.md
- AGENT_PROMPT.md

**Configuration:**
- mcp_settings.example.json
- Makefile
- .gitignore

**Testing:**
- test_installation.py
- scripts/

**CI/CD:**
- .github/workflows/

### Reference (Archived)

**Internal Docs:**
- archive/SKILL_DES.md (设计参考)
- archive/PROJECT_SUMMARY.md (项目总结)
- archive/DELIVERY.md (交付文档)

**Testing Docs:**
- archive/LOCAL_TESTING.md (本地测试)
- archive/START_HERE.md (快速开始)

---

## 🧹 Cleanup Summary

### Moved to Archive
- Internal design documents
- Project delivery documents
- Temporary testing guides
- Duplicate quick start docs

### Moved to Scripts
- Batch files for local testing
- Installation scripts

### Removed
- Duplicate configuration files
- Temporary test files

### Kept in Root
- Core user documentation
- Essential developer guides
- Configuration examples
- Source code
- Examples

---

## 📦 What Gets Published

When publishing to PyPI, only these are included:

```
Package Contents:
├── src/mcp_server_skill/      (source code)
├── README.md                   (package description)
├── LICENSE                     (license)
├── QUICKSTART.md              (quick start)
├── MCP_CONFIG.md              (configuration)
├── examples/                   (example skills)
└── pyproject.toml             (package metadata)
```

Excluded from package:
- Archive documents
- Testing scripts
- GitHub-specific files
- Development documentation

---

## 🎯 Navigation Tips

**New users?**
Start with [README.md](README.md) → [QUICKSTART.md](QUICKSTART.md)

**Want to configure?**
Check [MCP_CONFIG.md](MCP_CONFIG.md) for your platform

**Creating skills?**
See [examples/README.md](examples/README.md) and [CONTRIBUTING.md](CONTRIBUTING.md)

**Publishing?**
Follow [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md)

**Understanding internals?**
Read [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Last Updated:** 2025-01-11
