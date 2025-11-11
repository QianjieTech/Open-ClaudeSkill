# Release Checklist

Use this checklist before publishing a new release.

## Pre-Release

### Code Quality
- [ ] All tests pass locally
- [ ] Code is formatted with `black`
- [ ] No linting errors from `flake8`
- [ ] Type hints checked with `mypy`
- [ ] No security vulnerabilities in dependencies

### Documentation
- [ ] README.md is up to date
- [ ] CHANGELOG.md updated with all changes
- [ ] Version number updated in `pyproject.toml`
- [ ] All documentation reviewed for accuracy
- [ ] Examples tested and working
- [ ] API documentation complete

### Testing
- [ ] Installation test passes (`python test_installation.py`)
- [ ] Skill discovery works with example skills
- [ ] Hot-reload functionality verified
- [ ] Tested on Windows
- [ ] Tested on macOS
- [ ] Tested on Linux
- [ ] Tested with Kilo Code
- [ ] Tested with Claude Desktop (if available)
- [ ] MCP protocol working correctly

### Legal & Compliance
- [ ] LICENSE file present and correct
- [ ] All dependencies have compatible licenses
- [ ] THIRD_PARTY_NOTICES updated if needed
- [ ] No proprietary or sensitive code included

## Release Process

### 1. Version Update
```bash
# Update version in pyproject.toml
# Update CHANGELOG.md with release date
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to X.Y.Z"
```

### 2. Create Tag
```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

### 3. Build Package
```bash
make clean
make build
```

### 4. Test Package
```bash
# Test in a clean environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install dist/mcp_server_skill-X.Y.Z-py3-none-any.whl
mcp-server-skill --help
python test_installation.py
deactivate
rm -rf test_env
```

### 5. Publish to PyPI
```bash
# Test PyPI first (optional)
python -m twine upload --repository testpypi dist/*

# Production PyPI
python -m twine upload dist/*
```

### 6. Create GitHub Release
- [ ] Go to GitHub Releases
- [ ] Create new release from tag
- [ ] Copy CHANGELOG entry to release notes
- [ ] Upload wheel and sdist files
- [ ] Mark as latest release
- [ ] Publish release

### 7. Verify Publication
- [ ] Package appears on PyPI: https://pypi.org/project/mcp-server-skill/
- [ ] Installation works: `pip install mcp-server-skill`
- [ ] uvx installation works: `uvx mcp-server-skill --help`
- [ ] Documentation links work
- [ ] GitHub release created

## Post-Release

### Announcements
- [ ] Update project README badges if needed
- [ ] Post announcement in GitHub Discussions
- [ ] Share on relevant communities
- [ ] Update documentation site (if exists)

### Monitoring
- [ ] Monitor GitHub Issues for bug reports
- [ ] Check PyPI download statistics
- [ ] Gather user feedback
- [ ] Plan next release based on feedback

## Rollback Plan

If critical issues are found after release:

1. **Yank release from PyPI** (if necessary):
   ```bash
   python -m twine upload --skip-existing --repository pypi dist/*
   # Contact PyPI support to yank version
   ```

2. **Create hotfix**:
   ```bash
   git checkout vX.Y.Z
   git checkout -b hotfix-X.Y.Z+1
   # Fix issue
   # Follow release process for X.Y.Z+1
   ```

3. **Communicate**:
   - Update GitHub release notes
   - Post issue explanation
   - Guide users to new version

## Version Numbering Guide

Following [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
  - Incompatible API changes
  - Skill format changes
  - MCP protocol changes

- **MINOR** (0.X.0): New features
  - New functionality
  - New configuration options
  - Performance improvements
  - Backwards compatible

- **PATCH** (0.0.X): Bug fixes
  - Bug fixes
  - Documentation updates
  - Security patches
  - Backwards compatible

## Emergency Hotfix Process

For critical security or data loss bugs:

1. Create hotfix branch from release tag
2. Fix issue with minimal changes
3. Fast-track testing (critical paths only)
4. Bump patch version
5. Release immediately
6. Backport to main/develop

## Notes

- Always test in clean environment before publishing
- Never delete published releases (yank if needed)
- Keep CHANGELOG.md accurate and up to date
- Communicate breaking changes clearly
- Maintain backwards compatibility when possible

---

**Last Updated**: 2025-01-11
