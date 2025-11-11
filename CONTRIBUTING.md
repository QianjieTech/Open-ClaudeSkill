# Contributing to Open-ClaudeSkill

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Create and Share Skills

The most valuable contributions are high-quality skills that others can use.

**Requirements**:
- Follow the [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- Include clear description of when to use the skill
- Provide examples and best practices
- Test thoroughly before submitting

**Process**:
1. Create your skill in a local `.skill` directory
2. Test it with your agent
3. Submit a PR adding it to `examples/`
4. Include a description of the use case

### 2. Improve the Server

**Areas for improvement**:
- Performance optimization
- Better error handling
- Additional features
- Bug fixes

**Process**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and create a PR

### 3. Documentation

Help improve documentation:
- Fix typos and errors
- Add examples
- Clarify confusing sections
- Translate to other languages

### 4. Bug Reports

Found a bug? Please report it!

**Include**:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, agent)
- Relevant logs or error messages

### 5. Feature Requests

Have an idea? We'd love to hear it!

**Include**:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Alternatives considered

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/open-claudeskill.git
cd open-claudeskill
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install in Development Mode

```bash
pip install -e ".[dev]"
```

### 4. Run Tests

```bash
pytest
```

### 5. Code Style

We use:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

```bash
black src/
flake8 src/
mypy src/
```

## Skill Creation Guidelines

### Structure

```
skill-name/
├── SKILL.md          # Required: Main skill file
├── README.md         # Optional: Additional documentation
├── examples/         # Optional: Example files
│   └── example.py
└── templates/        # Optional: Template files
    └── template.txt
```

### SKILL.md Template

```markdown
---
name: skill-name
description: Clear, concise description of what the skill does and when to use it. Include keywords that match user queries.
license: MIT
---

# Skill Title

Brief overview of the skill.

## When to Use This Skill

Clear indicators of when this skill should be invoked.

## Capabilities

- Capability 1
- Capability 2

## Guidelines

### Section 1
Detailed instructions...

### Section 2
More instructions...

## Examples

### Example 1
```
User: [example request]
Agent: [example response]
```

## Best Practices

- Practice 1
- Practice 2

## Common Pitfalls

- Pitfall 1 and how to avoid it
- Pitfall 2 and how to avoid it
```

### Description Writing

The description is crucial for skill discovery. Make it:

1. **Specific**: Include concrete keywords
   - ❌ "Helps with code"
   - ✅ "Code review focusing on security, performance, and maintainability. Use for code audits, vulnerability scanning, or improvement suggestions."

2. **Action-oriented**: Use clear triggers
   - Include phrases like "Use when", "Use for"
   - List specific use cases

3. **Keyword-rich**: Think about user queries
   - What words would users use?
   - Include synonyms and related terms

4. **Concise but complete**: Balance brevity with clarity
   - Aim for 1-3 sentences
   - Cover the main use cases

### Content Guidelines

1. **Clear Structure**: Use headings and sections
2. **Actionable**: Provide specific instructions
3. **Examples**: Show, don't just tell
4. **Context**: Explain why, not just how
5. **Edge Cases**: Cover common issues
6. **Best Practices**: Share expert knowledge

### Testing Your Skill

Before submitting:

1. **Test invocation**: Does the agent recognize when to use it?
2. **Test instructions**: Can the agent follow them?
3. **Test edge cases**: Does it handle unusual inputs?
4. **Test clarity**: Is it easy to understand?

## Code Contribution Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Keep functions focused and small

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add hot-reload capability
fix: Handle missing SKILL.md gracefully
docs: Update configuration examples
test: Add tests for skill parsing
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

### Pull Requests

**Title**: Clear, descriptive summary

**Description should include**:
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes
- Related issues

**Example**:
```markdown
## Changes
- Added hot-reload capability using watchdog
- Refactored skill loader for better modularity

## Motivation
Users requested ability to update skills without restarting server

## Testing
1. Start server
2. Modify a SKILL.md file
3. Verify reload message appears
4. Invoke the skill to confirm changes

## Breaking Changes
None

## Related Issues
Closes #123
```

### Code Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer review required
3. Address all feedback
4. Squash commits if requested
5. Maintainer will merge when ready

## Skill Contribution Checklist

- [ ] Follows Agent Skills Spec format
- [ ] Clear, keyword-rich description
- [ ] Well-structured content
- [ ] Includes examples
- [ ] Tested with multiple agents
- [ ] No sensitive information
- [ ] License specified
- [ ] README.md if complex
- [ ] Attributed sources if applicable

## Community Guidelines

### Be Respectful

- Be kind and courteous
- Respect different opinions
- Provide constructive feedback
- Assume good intentions

### Be Collaborative

- Share knowledge
- Help others learn
- Credit contributions
- Celebrate successes

### Be Professional

- Stay on topic
- No spam or self-promotion
- Follow code of conduct
- Report inappropriate behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- **General questions**: GitHub Discussions
- **Bug reports**: GitHub Issues
- **Security issues**: Email security@example.com
- **Chat**: Discord community

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing to Open-ClaudeSkill! 🎉
