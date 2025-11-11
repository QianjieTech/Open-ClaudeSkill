---
name: example-calculator
description: A simple calculator skill that demonstrates the skill system. Use this when users ask for mathematical calculations, arithmetic operations, or number crunching.
license: MIT
---

# Calculator Skill

This skill helps you perform mathematical calculations accurately and explain the steps.

## Capabilities

You can help with:
- Basic arithmetic (addition, subtraction, multiplication, division)
- Order of operations
- Percentage calculations
- Unit conversions
- Explaining mathematical concepts

## Guidelines

1. **Show Your Work**: Always explain the steps in calculations
2. **Use Proper Notation**: Use clear mathematical notation
3. **Verify Results**: Double-check your calculations
4. **Handle Edge Cases**: Watch for division by zero, overflow, etc.

## Example Interactions

### Basic Calculation
```
User: What's 1234 × 5678?
Assistant: Let me calculate 1234 × 5678:

1234 × 5678 = 7,006,652

Breaking it down:
- 1234 × 5000 = 6,170,000
- 1234 × 600 = 740,400
- 1234 × 70 = 86,380
- 1234 × 8 = 9,872
- Total: 7,006,652
```

### Percentage
```
User: What's 15% of 240?
Assistant: To find 15% of 240:

15% = 15/100 = 0.15
0.15 × 240 = 36

So 15% of 240 is 36.
```

## Best Practices

- Always verify calculations using the Bash tool if needed
- Format large numbers with commas for readability
- Provide context and explanations, not just answers
- Use proper mathematical terminology
