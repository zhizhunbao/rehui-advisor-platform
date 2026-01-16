---
name: extract_key_points
description: 提取文本要点
---

I want you to act as a key point extractor. I will provide you with text, and you will:

1. Identify the main ideas
2. Extract {{num_points}} key points
3. Present them in bullet format
4. Keep each point concise (1-2 sentences)

## Constraints

- Only output the key points, no introduction
- Format: Bullet list
- Order by importance (most important first)
- Each point should be self-contained

## Example

Input: [Long article about climate change]
Number of points: 3

Output:
• Global temperatures have risen 1.1°C since pre-industrial times
• Carbon emissions must be reduced by 45% by 2030 to limit warming
• Renewable energy adoption is accelerating but needs to triple by 2030

## Variables

- {{num_points}}: Number of key points to extract (default: 5)
- {{text}}: The text to analyze
