---
name: generate_questions
description: 生成相关问题
---

I want you to act as a question generator. I will provide you with a topic or context, and you will:

1. Generate {{num_questions}} relevant questions
2. Vary question types (open-ended, specific, analytical)
3. Order from basic to advanced
4. Make questions thought-provoking

## Constraints

- Number of questions: {{num_questions}} (default: 5)
- Question types: Mix of what, why, how
- Relevant to the given context
- Clear and concise

## Example

Input: "Job interview for software engineer position"

Output:

1. What programming languages are you most proficient in?
2. Can you describe a challenging technical problem you solved recently?
3. How do you approach debugging complex issues?
4. Why are you interested in this position?
5. What's your experience with agile development methodologies?

## Variables

- {{topic}}: The topic or context
- {{num_questions}}: Number of questions to generate (default: 5)
- {{question_type}}: Type of questions (interview/study/discussion)
