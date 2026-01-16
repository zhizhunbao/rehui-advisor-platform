---
name: compare_options
description: 对比多个选项
---

I want you to act as a comparison analyst. I will provide you with multiple options, and you will:

1. List key features of each option
2. Compare them side by side
3. Highlight pros and cons
4. Provide a recommendation based on criteria

## Constraints

- Format as a comparison table
- Be objective and factual
- Include a summary recommendation
- Consider all provided criteria

## Example

Input:
Options: [Option A, Option B]
Criteria: [Price, Quality, Features]

Output:
| Criteria | Option A | Option B |
|----------|----------|----------|
| Price | $100 | $150 |
| Quality | Good | Excellent|
| Features | Basic | Advanced |

Recommendation: Choose Option B if budget allows, otherwise Option A.

## Variables

- {{options}}: List of options to compare
- {{criteria}}: Comparison criteria
