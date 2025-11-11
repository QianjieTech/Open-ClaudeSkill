# Architecture Documentation

## Overview

Open-ClaudeSkill implements a progressive disclosure system for AI agent capabilities using the Model Context Protocol (MCP). This architecture enables any MCP-compatible agent to benefit from Claude's skill system design pattern.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User / Developer                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Natural Language Request
                         │
┌────────────────────────▼────────────────────────────────────┐
│               MCP-Compatible AI Agent                        │
│         (Kilo Code, Claude Desktop, Cline, etc.)             │
│                                                               │
│  System Prompt includes:                                     │
│  - Skill usage instructions                                  │
│  - How to recognize when to use skills                       │
│  - Progressive disclosure pattern                            │
│                                                               │
│  Agent sees load_skill tool with:                            │
│  - Tool description                                          │
│  - Embedded <available_skills> XML                          │
│  - Skill names and descriptions only                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ MCP Protocol (JSON-RPC over stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              MCP Server (This Project)                       │
│              mcp-server-skill                                │
│                                                               │
│  ┌───────────────────────────────────────────────┐          │
│  │         Tool Handler                           │          │
│  │  - load_skill tool registration               │          │
│  │  - Embeds available_skills XML                │          │
│  │  - Handles skill invocation                   │          │
│  └─────────────────┬─────────────────────────────┘          │
│                    │                                         │
│  ┌─────────────────▼─────────────────────────────┐          │
│  │         Skill Loader                           │          │
│  │  - Discovers skills in .skill/                │          │
│  │  - Parses SKILL.md files                      │          │
│  │  - Validates YAML frontmatter                 │          │
│  │  - Extracts name, description, content        │          │
│  │  - Caches parsed skills                       │          │
│  └─────────────────┬─────────────────────────────┘          │
│                    │                                         │
│  ┌─────────────────▼─────────────────────────────┐          │
│  │      File System Watcher                      │          │
│  │  - Monitors .skill/ directory                 │          │
│  │  - Detects SKILL.md changes                   │          │
│  │  - Triggers hot-reload                        │          │
│  │  - Updates skill cache                        │          │
│  └───────────────────────────────────────────────┘          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ File System Access
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  .skill/ Directory                           │
│                                                               │
│  skill-name-1/                                               │
│  ├── SKILL.md  ◄─── YAML frontmatter + Markdown             │
│  └── ...                                                     │
│                                                               │
│  skill-name-2/                                               │
│  ├── SKILL.md                                                │
│  ├── examples/                                               │
│  └── templates/                                              │
└──────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. MCP Server (`server.py`)

**Responsibilities**:
- Implements MCP protocol over stdio
- Registers `load_skill` tool
- Handles tool invocation requests
- Manages server lifecycle
- Coordinates hot-reload

**Key Classes**:
- `SkillMCPServer`: Main server class
- `SkillFileHandler`: File system event handler

**Protocol Flow**:
```
1. Client connects via stdio
2. Server sends initialization
3. Client requests tool list
4. Server responds with load_skill tool
5. Client calls load_skill(skill="name")
6. Server returns full skill content
```

### 2. Skill Loader (`skill_loader.py`)

**Responsibilities**:
- Scan `.skill/` directory for skill folders
- Parse `SKILL.md` files
- Validate YAML frontmatter
- Cache parsed skills
- Generate XML for tool description

**Key Classes**:
- `Skill`: Data class representing a parsed skill
- `SkillLoader`: Main loader with discovery and parsing logic

**Parsing Flow**:
```
1. Scan for directories in .skill/
2. Look for SKILL.md in each
3. Split frontmatter from body
4. Parse YAML frontmatter
5. Validate required fields
6. Create Skill object
7. Cache in memory
```

### 3. File System Watcher

**Responsibilities**:
- Monitor `.skill/` directory
- Detect file changes (create, modify, delete)
- Trigger skill reload
- Update agent's available skills

**Technologies**:
- `watchdog` library for cross-platform file monitoring
- Event-driven architecture
- Debouncing to avoid excessive reloads

## Progressive Disclosure Pattern

### Phase 1: Initial State (Minimal Context)

```xml
Agent's system prompt includes:
<available_skills>
  <skill>
    <name>code-reviewer</name>
    <description>Code review skill...</description>
    <location>local</location>
  </skill>
  <skill>
    <name>calculator</name>
    <description>Math calculation skill...</description>
    <location>local</location>
  </skill>
</available_skills>
```

**Context Usage**: ~100 tokens per skill (name + description only)

### Phase 2: Skill Invocation (Lazy Loading)

```
User: "Review this code for security issues"
Agent: [Recognizes code-reviewer skill matches]
Agent: [Calls load_skill("code-reviewer")]
Server: [Returns full SKILL.md content]
Agent: [Now has detailed instructions]
```

**Context Usage**: ~1000-5000 tokens (only for invoked skill)

### Phase 3: Execution (Full Capability)

```
Agent follows detailed instructions from skill:
- Security checklist
- Review dimensions
- Severity levels
- Output format
- Best practices
```

**Benefits**:
- Skills available but not loaded: ~100 tokens each
- Skills loaded on-demand: ~1000-5000 tokens
- Total context saved: Significant with many skills

## Data Flow

### Skill Discovery Flow

```
┌──────────────┐
│  Server      │
│  Starts      │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│  Scan .skill/       │
│  directory          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  For each folder:   │
│  - Find SKILL.md    │
│  - Parse YAML       │
│  - Extract content  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Create Skill       │
│  objects            │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Cache in memory    │
│  {name: Skill}      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Generate XML for   │
│  tool description   │
└─────────────────────┘
```

### Tool Invocation Flow

```
┌──────────────┐
│  Agent calls │
│  load_skill  │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│  MCP Server         │
│  receives call      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Extract skill      │
│  name from args     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Reload skills      │
│  (fresh data)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Lookup skill       │
│  in cache           │
└──────┬──────────────┘
       │
       ├── Found ─────┐
       │              │
       │              ▼
       │     ┌─────────────────────┐
       │     │  Format response:   │
       │     │  - Frontmatter      │
       │     │  - Full content     │
       │     └──────┬──────────────┘
       │            │
       │            ▼
       │     ┌─────────────────────┐
       │     │  Return to agent    │
       │     └─────────────────────┘
       │
       └── Not Found ┐
                     │
                     ▼
              ┌─────────────────────┐
              │  Return error with  │
              │  available skills   │
              └─────────────────────┘
```

### Hot-Reload Flow

```
┌──────────────┐
│  File change │
│  detected    │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│  Watchdog event     │
│  triggered          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Is SKILL.md?       │
└──────┬──────────────┘
       │
       ├── Yes ────────┐
       │               │
       │               ▼
       │        ┌─────────────────────┐
       │        │  Trigger reload     │
       │        │  callback           │
       │        └──────┬──────────────┘
       │               │
       │               ▼
       │        ┌─────────────────────┐
       │        │  Re-scan .skill/    │
       │        └──────┬──────────────┘
       │               │
       │               ▼
       │        ┌─────────────────────┐
       │        │  Update cache       │
       │        └──────┬──────────────┘
       │               │
       │               ▼
       │        ┌─────────────────────┐
       │        │  Log reload         │
       │        └─────────────────────┘
       │
       └── No ─────┐
                   │
                   ▼
              ┌─────────────────────┐
              │  Ignore event       │
              └─────────────────────┘
```

## Skill File Format

### SKILL.md Structure

```
┌─────────────────────────────────────┐
│  ---                                 │  ▲
│  name: skill-name                    │  │
│  description: When to use this...    │  │ YAML Frontmatter
│  license: MIT                        │  │ (Required section)
│  allowed-tools:                      │  │
│    - Read                            │  │
│  metadata:                           │  │
│    author: "Name"                    │  │
│  ---                                 │  ▼
├─────────────────────────────────────┤
│  # Skill Title                       │  ▲
│                                      │  │
│  ## Section 1                        │  │
│  Content...                          │  │
│                                      │  │ Markdown Body
│  ## Section 2                        │  │ (Instructions)
│  More content...                     │  │
│                                      │  │
│  ## Examples                         │  │
│  Examples...                         │  │
└─────────────────────────────────────┘  ▼
```

### Field Processing

```python
{
  "name": str,              # Required, must match folder
  "description": str,       # Required, for agent matching
  "license": str | None,    # Optional
  "allowed-tools": [str],   # Optional, for Claude Code
  "metadata": {             # Optional, custom fields
    str: str
  }
}
```

## Error Handling

### Parsing Errors

```python
try:
    skill = parse_skill_file(path)
except YAMLError:
    log_error("Invalid YAML")
    skip_skill()
except MissingFieldError:
    log_error("Missing required field")
    skip_skill()
except ValidationError:
    log_error("Validation failed")
    skip_skill()
```

### Runtime Errors

```python
try:
    skill = get_skill(name)
except KeyError:
    return error_response(
        available_skills=list_skill_names()
    )
```

### MCP Errors

```python
try:
    result = await call_tool(name, args)
except UnknownToolError:
    raise ValueError(f"Unknown tool: {name}")
except InvalidArgumentsError:
    raise ValueError("Invalid arguments")
```

## Security Considerations

### File System Access

- **Sandboxing**: Server only reads from configured directory
- **Path Validation**: Prevent directory traversal
- **Permissions**: Respect file system permissions

### Skill Content

- **No Execution**: Skills are text only, not executed
- **Agent Responsibility**: Agent interprets instructions
- **User Control**: Users control skill directory

### MCP Protocol

- **Stdio Only**: No network exposure by default
- **Local Communication**: Between agent and server
- **No Authentication**: Relies on process isolation

## Performance Considerations

### Caching Strategy

```python
# Parse once, cache in memory
skills: Dict[str, Skill] = {}

# Reload on changes
def on_file_change():
    skills = discover_skills()
```

### Lazy Loading

```python
# Don't load content until requested
def list_tools():
    return only_names_and_descriptions()

def call_tool(name):
    return full_skill_content(name)
```

### File Watching

```python
# Efficient event-driven reload
observer.schedule(handler, path, recursive=True)
# Only reload on SKILL.md changes
```

## Extensibility Points

### Custom Skill Locations

```python
# Support multiple directories
loader = SkillLoader(skills_dir=Path("/custom/path"))
```

### Custom Validation

```python
# Add custom validation logic
def validate_skill(skill: Skill) -> bool:
    # Custom rules
    return True
```

### Custom Tool Names

```python
# Use different tool name
server.register_tool("invoke_skill", handler)
```

### Skill Transformations

```python
# Pre-process skill content
def transform_skill(skill: Skill) -> Skill:
    skill.content = preprocess(skill.content)
    return skill
```

## Testing Strategy

### Unit Tests

```python
# Test skill parsing
def test_parse_valid_skill():
    skill = parse_skill_file("test.md")
    assert skill.name == "test"

# Test XML generation
def test_generate_xml():
    xml = skill.to_xml()
    assert "<name>test</name>" in xml
```

### Integration Tests

```python
# Test MCP protocol
async def test_tool_invocation():
    result = await client.call_tool("load_skill", {"skill": "test"})
    assert result.content[0].text.startswith("The \"test\" skill")
```

### End-to-End Tests

```python
# Test with real agent
def test_agent_workflow():
    # Start server
    # Configure agent
    # Invoke skill
    # Verify response
```

## Deployment

### Package Distribution

```bash
# PyPI package
pip install mcp-server-skill

# uvx (no install)
uvx mcp-server-skill

# From source
pip install -e .
```

### Configuration Management

```json
// Per-user config
~/.config/mcp/settings.json

// Per-project config
./.mcp/settings.json

// Environment variables
SKILLS_DIR=/path/to/skills
```

## Future Enhancements

### Planned Features

1. **Skill Dependencies**: Skills can reference other skills
2. **Skill Versioning**: Version control for skills
3. **Remote Repositories**: Download skills from GitHub/registries
4. **Skill Validation**: Automated quality checks
5. **Skill Analytics**: Usage tracking and metrics
6. **Web UI**: Browser-based skill management
7. **Skill Marketplace**: Share and discover skills

### Protocol Enhancements

1. **Resources**: Expose skill files as MCP resources
2. **Prompts**: Pre-configured prompts for skills
3. **Sampling**: Skill-specific LLM parameters
4. **Progress**: Streaming skill loading feedback

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- [Claude Code Skills](https://github.com/anthropics/skills)
- [Watchdog Documentation](https://python-watchdog.readthedocs.io/)

---

This architecture enables a universal skill system that works across any MCP-compatible agent while maintaining the progressive disclosure benefits of Claude's original design.
