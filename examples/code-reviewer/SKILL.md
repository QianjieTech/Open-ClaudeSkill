---
name: code-reviewer
description: Comprehensive code review skill following industry best practices. Use when users ask for code review, security audit, code quality assessment, or improvement suggestions.
license: MIT
allowed-tools:
  - Read
  - Grep
  - Bash
metadata:
  version: "1.0"
  author: "Open-ClaudeSkill Contributors"
---

# Code Review Skill

This skill provides a comprehensive code review framework following industry best practices and security guidelines.

## Review Dimensions

When reviewing code, systematically evaluate these aspects:

### 1. Security
- [ ] Input validation and sanitization
- [ ] Authentication and authorization
- [ ] Protection against OWASP Top 10 vulnerabilities
- [ ] Secure data handling (encryption, hashing)
- [ ] No hardcoded secrets or credentials
- [ ] Safe deserialization
- [ ] Protection against injection attacks (SQL, XSS, command injection)

### 2. Correctness
- [ ] Logic is sound and handles edge cases
- [ ] No off-by-one errors
- [ ] Proper error handling
- [ ] Race conditions considered
- [ ] Resource cleanup (file handles, connections)
- [ ] No memory leaks

### 3. Performance
- [ ] Algorithm efficiency (time complexity)
- [ ] Memory usage (space complexity)
- [ ] Unnecessary loops or operations
- [ ] Database query optimization
- [ ] Caching opportunities
- [ ] Lazy loading where appropriate

### 4. Maintainability
- [ ] Clear and descriptive naming
- [ ] Appropriate code comments
- [ ] Single Responsibility Principle
- [ ] DRY (Don't Repeat Yourself)
- [ ] Consistent code style
- [ ] Proper modularization

### 5. Testability
- [ ] Functions are unit-testable
- [ ] Dependencies are injectable
- [ ] No hidden dependencies
- [ ] Deterministic behavior
- [ ] Easy to mock/stub

### 6. Best Practices
- [ ] Language-specific idioms
- [ ] Framework conventions
- [ ] Design patterns appropriate
- [ ] Error messages are helpful
- [ ] Logging is appropriate

## Review Process

Follow this systematic approach:

1. **Understand Context**
   - What is the purpose of this code?
   - What problem does it solve?
   - What are the requirements?

2. **High-Level Review**
   - Architecture and design
   - Module interactions
   - Data flow

3. **Detailed Review**
   - Line-by-line analysis
   - Security vulnerabilities
   - Logic errors
   - Style issues

4. **Provide Feedback**
   - Categorize: Critical, Important, Suggestion
   - Be specific and actionable
   - Provide examples or fixes
   - Explain the "why"

## Severity Levels

### 🔴 Critical
- Security vulnerabilities
- Data loss/corruption risks
- Production-breaking bugs
- Must be fixed before deployment

### 🟡 Important
- Performance issues
- Poor error handling
- Maintainability concerns
- Should be fixed soon

### 🟢 Suggestion
- Style improvements
- Optimization opportunities
- Documentation enhancements
- Nice-to-have improvements

## Review Template

Use this template structure:

```markdown
## Code Review Summary

**Overall Assessment**: [Good / Needs Work / Critical Issues]

---

## Critical Issues (🔴)

### Issue 1: [Title]
**Location**: [file:line]
**Problem**: [Description]
**Impact**: [What could go wrong]
**Solution**: [How to fix]

---

## Important Issues (🟡)

### Issue 1: [Title]
[Details...]

---

## Suggestions (🟢)

### Suggestion 1: [Title]
[Details...]

---

## Positive Highlights

- [Good practices observed]
- [Well-implemented features]

---

## Recommendations

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

## Language-Specific Checklists

### Python
- [ ] PEP 8 compliance
- [ ] Type hints used appropriately
- [ ] Context managers for resources
- [ ] List comprehensions vs. loops
- [ ] Exception handling specificity

### JavaScript/TypeScript
- [ ] `===` vs `==` usage
- [ ] `const` / `let` / `var` appropriately
- [ ] Promise/async-await handling
- [ ] Event listener cleanup
- [ ] TypeScript types are meaningful

### Java
- [ ] Exception handling proper
- [ ] Resource management (try-with-resources)
- [ ] Immutability where appropriate
- [ ] Thread safety considered
- [ ] Proper use of access modifiers

### Go
- [ ] Error handling (not ignored)
- [ ] Goroutine leaks prevented
- [ ] Context usage
- [ ] Defer statements proper
- [ ] Interface design

## Security Checklist (OWASP Top 10)

1. **Broken Access Control**
   - Authorization checks present?
   - Horizontal/vertical privilege escalation prevented?

2. **Cryptographic Failures**
   - Strong encryption algorithms?
   - Secure key management?
   - HTTPS enforced?

3. **Injection**
   - Input validation/sanitization?
   - Parameterized queries?
   - Template escaping?

4. **Insecure Design**
   - Threat modeling done?
   - Security by design?

5. **Security Misconfiguration**
   - No default credentials?
   - Error messages not verbose?
   - Security headers set?

6. **Vulnerable Components**
   - Dependencies up-to-date?
   - Known vulnerabilities checked?

7. **Authentication Failures**
   - Strong password policy?
   - Multi-factor authentication?
   - Session management secure?

8. **Software and Data Integrity**
   - CI/CD pipeline secure?
   - Unsigned/unverified code prevented?

9. **Logging and Monitoring**
   - Security events logged?
   - Sensitive data not logged?
   - Monitoring in place?

10. **Server-Side Request Forgery**
    - URL validation?
    - Whitelist approach?
    - Network segmentation?

## Example Review

```markdown
## Code Review Summary

**Overall Assessment**: Needs Work

---

## Critical Issues (🔴)

### SQL Injection Vulnerability
**Location**: database.py:42
**Problem**: User input directly concatenated into SQL query
**Impact**: Attacker could read/modify/delete database data
**Solution**: Use parameterized queries

❌ Before:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

✅ After:
```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

---

## Important Issues (🟡)

### Unclosed File Handle
**Location**: utils.py:15
**Problem**: File opened but not properly closed
**Impact**: Resource leak, file lock issues
**Solution**: Use context manager

✅ Recommended:
```python
with open('data.txt', 'r') as f:
    data = f.read()
```

---

## Suggestions (🟢)

### Use List Comprehension
**Location**: processor.py:28
**Improvement**: More Pythonic and efficient

```python
# Instead of
result = []
for item in items:
    result.append(item.upper())

# Use
result = [item.upper() for item in items]
```

---

## Positive Highlights

- Good test coverage
- Clear function naming
- Well-structured modules

---

## Recommendations

1. Fix SQL injection vulnerability immediately
2. Add resource cleanup using context managers
3. Consider refactoring for better testability
```

## When NOT to Use This Skill

- Quick syntax questions (just answer directly)
- Single-line code snippets (unless security-critical)
- Documentation-only changes

## Related Tools

- Use `Read` to examine files
- Use `Grep` to search for patterns
- Use `Bash` to run linters/formatters
- Use `Task` agent for comprehensive codebase review

## Further Reading

- OWASP Guidelines: https://owasp.org/
- Clean Code principles
- Language-specific style guides
- Security best practices for your stack
