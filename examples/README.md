# Example Skills

This directory contains example skills to help you get started with Open-ClaudeSkill.

## Available Examples

### 1. Calculator (`calculator/`)

**Purpose**: Demonstrates a simple skill for mathematical calculations.

**Use Case**: When users ask for arithmetic operations, percentage calculations, or mathematical explanations.

**Key Features**:
- Clear instructions for showing work
- Guidelines for formatting
- Example interactions
- Best practices

**Try it**:
```
Copy to .skill directory:
cp -r examples/calculator .skill/

Ask your agent:
"What's 15% of 240?"
"Calculate 1234 times 5678"
```

---

### 2. Code Reviewer (`code-reviewer/`)

**Purpose**: Comprehensive code review framework with security focus.

**Use Case**: Code quality assessment, security audits, improvement suggestions.

**Key Features**:
- Multi-dimensional review (security, performance, maintainability)
- OWASP Top 10 security checklist
- Language-specific guidelines
- Severity categorization
- Detailed examples

**Try it**:
```
Copy to .skill directory:
cp -r examples/code-reviewer .skill/

Ask your agent:
"Review this code for security issues: [paste code]"
"What security vulnerabilities should I check for?"
```

---

## Using These Examples

### Quick Start

1. **Copy to your skills directory**:
   ```bash
   cp -r examples/calculator .skill/
   cp -r examples/code-reviewer .skill/
   ```

2. **Restart your agent** (or wait for hot-reload)

3. **Test the skills**:
   ```
   "What skills are available?"
   "Use the calculator skill"
   "Review my code"
   ```

### Customizing

These examples are templates. Feel free to:
- Modify descriptions to match your needs
- Add/remove sections
- Adjust guidelines
- Include your own best practices
- Add domain-specific knowledge

### Learning from Examples

Study these to understand:
- **Description writing**: How to write descriptions that trigger correctly
- **Structure**: How to organize skill content
- **Instructions**: How to provide clear, actionable guidance
- **Examples**: How to show rather than tell
- **Best practices**: What makes a skill effective

## More Examples

Want more? Check out:

### Official Claude Skills
- Repository: https://github.com/anthropics/skills
- Maintained by Anthropic
- Production-quality skills

```bash
cd .skill
git clone https://github.com/anthropics/skills.git temp-skills
cp -r temp-skills/mcp-builder ./
cp -r temp-skills/skill-creator ./
rm -rf temp-skills
```

### Community Skills
- Search GitHub for `claudeskill` or `mcp-skill`
- Check discussions in the community
- Browse shared skill collections

## Creating Your Own

1. **Start with a template**:
   ```bash
   cp -r examples/calculator .skill/my-new-skill
   ```

2. **Modify SKILL.md**:
   - Change name and description
   - Update instructions
   - Add your expertise

3. **Test thoroughly**:
   - Try different phrasings
   - Check edge cases
   - Verify hot-reload works

4. **Share with community**:
   - Submit a PR to add to examples/
   - Share in discussions
   - Get feedback

## Example Skill Ideas

### Development
- **api-designer**: REST API design best practices
- **test-writer**: Test generation guidelines
- **debug-helper**: Debugging strategies
- **git-helper**: Git workflow guidance

### Content
- **blog-writer**: Blog post structure and SEO
- **technical-docs**: Documentation standards
- **email-composer**: Professional email templates
- **presentation-builder**: Slide deck design

### Data & Analysis
- **sql-optimizer**: Database query optimization
- **data-visualizer**: Chart and graph best practices
- **stats-helper**: Statistical analysis guidance
- **data-cleaner**: Data cleaning workflows

### Domain-Specific
- **legal-drafter**: Legal document templates
- **medical-noter**: Medical note formatting
- **finance-analyzer**: Financial analysis frameworks
- **edu-planner**: Lesson planning assistance

## Contributing Examples

Have a great skill? Share it!

1. **Ensure quality**:
   - Well-tested
   - Clear documentation
   - Follows best practices

2. **Submit PR**:
   - Add to `examples/`
   - Include README entry
   - Provide use case

3. **Help others**:
   - Respond to questions
   - Update based on feedback
   - Maintain your contribution

## Troubleshooting Examples

### Example doesn't work
- Check YAML frontmatter format
- Verify name matches folder
- Look for parsing errors in logs

### Agent doesn't invoke skill
- Review description keywords
- Make description more specific
- Test with explicit request: "Use the [skill-name] skill"

### Instructions unclear
- Add more examples
- Break into smaller steps
- Include common pitfalls

## Resources

- **Documentation**: [Main README](../README.md)
- **Skill Format**: [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Configuration**: [MCP_CONFIG.md](../MCP_CONFIG.md)

---

**Happy skill building!** 🚀
