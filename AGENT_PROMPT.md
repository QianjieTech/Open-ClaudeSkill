# System Prompt Template for Skill-Enabled Agents

Add this section to your agent's system prompt to enable skill support via MCP.

## Skill System Instructions

```xml
<skill_system>
You have access to a skill system that provides specialized capabilities and domain knowledge through progressive disclosure.

## How Skills Work

Skills are specialized capability modules that:
1. Are initially presented as brief descriptions in your tool list
2. Load full detailed instructions only when invoked
3. Provide domain-specific knowledge, workflows, and best practices

## When to Use Skills

When users ask you to perform tasks:
1. Check if any available skills (visible in the load_skill tool description) match the task
2. Look for keywords in skill descriptions that align with user requests
3. Proactively suggest relevant skills when appropriate

## How to Invoke Skills

Use the `load_skill` tool with the skill name:
- The tool description contains `<available_skills>` listing all skills
- Each skill has a `<name>` and `<description>`
- Pass only the skill name (no other arguments)
- After invocation, you'll receive the full skill instructions

## Examples

User: "Help me create a poster design"
→ Check available skills for design-related capabilities
→ If a design skill exists, invoke: load_skill(skill="canvas-design")
→ Follow the expanded instructions

User: "I need to analyze this spreadsheet"
→ Check for spreadsheet/data skills
→ Invoke the relevant skill if available
→ Apply the skill's specialized knowledge

## Important Rules

1. **Only use skills listed** in the load_skill tool's available_skills section
2. **Don't invoke twice**: If a skill is already loaded in the conversation, don't reload it
3. **Check descriptions carefully**: Match user intent to skill descriptions
4. **Progressive disclosure**: Skills save context by loading only when needed
5. **Be proactive**: Suggest relevant skills when they could help

## Skill Structure

Each skill provides:
- Specialized domain knowledge
- Step-by-step workflows
- Best practices and guidelines
- Tool usage recommendations
- Example patterns and templates

Skills enhance your capabilities without consuming context until actually needed.
</skill_system>
```

## Integration Notes

### For MCP-Compatible Agents

1. **Tool Registration**: The MCP server automatically provides a `load_skill` tool
2. **Tool Description**: Contains embedded `<available_skills>` XML with all skill metadata
3. **Progressive Disclosure**: Full skill content is only returned when the tool is called

### For Different Agent Platforms

#### Claude Code / Kilo Code
- Add the above prompt section to system instructions
- Configure MCP server in settings (see MCP_CONFIG.md)
- Skills will appear as MCP tools

#### Custom Agents
- Include the prompt template in your system prompt
- Ensure your agent supports MCP tool calls
- Parse the `<available_skills>` XML from tool descriptions

#### API-Based Agents
- Add to system message template
- Handle tool calls according to your framework
- Extract skill names from user requests

## Customization

You can customize the prompt based on your needs:

1. **Add domain-specific guidance**: Include examples relevant to your use case
2. **Adjust proactivity**: Control when the agent should suggest skills
3. **Modify language/tone**: Adapt to your agent's personality
4. **Add constraints**: Include any restrictions on skill usage

## Testing the Integration

1. Start your agent with the modified system prompt
2. Ask: "What skills are available?"
3. The agent should list skills from the MCP server
4. Test invoking a skill: "Use the [skill-name] skill"
5. Verify the full skill content is loaded and followed

## Example Integration (Kilo Code)

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

Then add the system prompt section above to your agent configuration.
