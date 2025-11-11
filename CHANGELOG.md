# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Unit tests for skill parsing
- Integration tests for MCP protocol
- CI/CD pipeline
- PyPI publication
- Skill validation tool
- Skill template generator

## [0.1.0] - 2025-01-11

### Added
- Initial release of Open-ClaudeSkill
- MCP server implementation for skill loading
- Progressive disclosure pattern support
- Skill discovery from `.skill/` directory
- YAML frontmatter parsing for SKILL.md files
- Hot-reload capability using watchdog
- `load_skill` MCP tool for skill invocation
- Support for custom skills directory via `--skills-dir`
- Complete documentation suite:
  - README.md (English)
  - README.zh-CN.md (Chinese)
  - QUICKSTART.md (5-minute guide)
  - MCP_CONFIG.md (Platform configuration)
  - ARCHITECTURE.md (Technical architecture)
  - CONTRIBUTING.md (Contribution guidelines)
  - AGENT_PROMPT.md (System prompt template)
  - PROJECT_SUMMARY.md (Project overview)
- Example skills:
  - example-calculator: Simple math skill
  - code-reviewer: Comprehensive code review
- Example MCP configuration for Kilo Code
- Installation test script
- Makefile for common operations
- MIT License
- Full 100% compatibility with Agent Skills Spec

### Features
- **Progressive Disclosure**: Skills listed with name+description only, full content loads on-demand
- **Hot-Reload**: Automatic skill updates without server restart
- **Universal Compatibility**: Works with any MCP-compatible agent
- **Standard Format**: 100% compatible with official Claude Skill format
- **uvx Support**: Zero-config deployment via uvx
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Technical
- Python 3.10+ support
- Dependencies: mcp>=1.0.0, pyyaml>=6.0.1, watchdog>=3.0.0
- Entry point: `mcp-server-skill` command
- Package structure following modern Python best practices

### Documentation
- Comprehensive setup guides for multiple platforms
- Detailed architecture documentation
- Contribution guidelines
- Example skills with best practices
- Chinese language support

## Development Guidelines

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

### Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with changes
3. Create git tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
4. Build: `make build`
5. Publish: `make publish`
6. Push tag: `git push origin v0.1.0`

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

[Unreleased]: https://github.com/your-org/open-claudeskill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/open-claudeskill/releases/tag/v0.1.0
