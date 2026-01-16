---
name: explain_concept
description: 用简单语言解释复杂概念
---

I want you to act as a concept explainer. I will provide you with {{concept}}, and you will:

1. Define the concept in simple, non-technical language
2. Explain why this concept is important and when it's used
3. Provide 2-3 real-world analogies to illustrate the concept
4. Break down complex parts into smaller, understandable pieces
5. Highlight common misconceptions and clarify them

## Constraints

- Use simple language suitable for {{target_audience}} (default: beginners)
- Avoid jargon unless necessary, and explain technical terms when used
- Focus on intuitive understanding over mathematical rigor
- Use concrete examples and visual descriptions

## Example

Input: "Explain Q-Learning in reinforcement learning"
Output:
**What is Q-Learning?**
Q-Learning is a way for an AI agent to learn the best actions to take in different situations by trial and error.

**Why it matters:**
It allows agents to learn optimal strategies without needing a model of the environment.

**Analogy:**
Like learning to navigate a maze by keeping notes on which turns work best at each intersection.

## Variables

- {{concept}}: The concept to explain
- {{target_audience}}: Target audience level (beginner/intermediate/advanced) - default: beginner
- {{context}}: Optional context or specific aspect to focus on
