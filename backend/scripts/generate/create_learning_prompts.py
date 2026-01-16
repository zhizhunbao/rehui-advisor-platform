# 创建学习辅助类 Prompts
from pathlib import Path
import json

PROMPTS_DIR = Path(__file__).parent.parent / "data" / "prompts"

LEARNING_PROMPTS = [
    {
        "category": "learning",
        "name": "explain_concept",
        "display_name": "概念解释器",
        "display_name_en": "Concept Explainer",
        "description": "用简单语言解释复杂概念",
        "description_en": "Explain complex concepts in simple terms",
    },
    {
        "category": "learning",
        "name": "create_analogy",
        "display_name": "类比生成器",
        "display_name_en": "Analogy Creator",
        "description": "用生活例子类比技术概念",
        "description_en": "Create real-world analogies for technical concepts",
    },
    {
        "category": "learning",
        "name": "generate_examples",
        "display_name": "示例生成器",
        "display_name_en": "Example Generator",
        "description": "生成具体示例帮助理解",
        "description_en": "Generate concrete examples to aid understanding",
    },
    {
        "category": "code",
        "name": "explain_code",
        "display_name": "代码解释器",
        "display_name_en": "Code Explainer",
        "description": "逐行解释代码逻辑",
        "description_en": "Explain code logic line by line",
    },
    {
        "category": "code",
        "name": "debug_helper",
        "display_name": "调试助手",
        "display_name_en": "Debug Helper",
        "description": "帮助找出代码问题",
        "description_en": "Help identify code issues",
    },
    {
        "category": "document",
        "name": "summarize_chapter",
        "display_name": "章节总结",
        "display_name_en": "Chapter Summarizer",
        "description": "总结章节重点内容",
        "description_en": "Summarize key points from chapters",
    },
    {
        "category": "test",
        "name": "generate_quiz",
        "display_name": "测验生成器",
        "display_name_en": "Quiz Generator",
        "description": "生成练习测验题",
        "description_en": "Generate practice quiz questions",
    },
]


def get_prompt_content(category: str, name: str) -> str:
    prompts = {
        "learning-explain_concept": """I want you to act as a concept explainer. I will provide you with {{concept}}, and you will:

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
- {{target_audience}}: Target audience level (beginner/intermediate/advanced)
- {{context}}: Optional context or specific aspect to focus on""",

        "learning-create_analogy": """I want you to act as an analogy creator. I will provide you with {{technical_concept}}, and you will:

1. Identify the core mechanism or principle of the concept
2. Find a relatable real-world scenario that shares similar structure
3. Map technical terms to everyday equivalents
4. Explain how the analogy works step-by-step
5. Clarify where the analogy breaks down (limitations)

## Constraints

- Use scenarios from {{domain}} (default: everyday life)
- Make analogies culturally neutral and universally understandable
- Ensure the analogy captures the essence
- Acknowledge limitations to prevent misconceptions

## Example

Input: "Create an analogy for neural network backpropagation"
Output:
**Analogy: Learning to Throw Darts**
You adjust your aim based on where the dart lands vs. the target.

## Variables

- {{technical_concept}}: The technical concept to analogize
- {{domain}}: Domain for analogy (everyday life, sports, cooking, etc.)""",

        "learning-generate_examples": """I want you to act as an example generator. I will provide you with {{concept}}, and you will:

1. Create {{num_examples}} concrete, worked examples (default: 3)
2. Start with the simplest case and gradually increase complexity
3. Show step-by-step solution process for each example
4. Highlight key decision points and reasoning
5. Explain what makes each example illustrative

## Constraints

- Examples should be self-contained and complete
- Use realistic scenarios relevant to {{application_domain}}
- Show both correct approach and common mistakes
- Include numerical values and specific details

## Variables

- {{concept}}: The concept to generate examples for
- {{num_examples}}: Number of examples to generate (default: 3)
- {{application_domain}}: Domain for examples
- {{complexity_level}}: Starting complexity (simple/medium/complex)""",

        "code-explain_code": """I want you to act as a code explainer. I will provide you with {{code}}, and you will:

1. Provide a high-level overview of what the code does
2. Explain the purpose and structure of key components
3. Walk through the execution flow step-by-step
4. Highlight important algorithmic decisions and why they matter
5. Point out potential edge cases or optimization opportunities

## Constraints

- Explain at {{detail_level}} level (high-level/detailed/line-by-line)
- Focus on the "why" behind design choices
- Use clear variable names in explanations
- Relate code back to underlying algorithm or concept

## Variables

- {{code}}: The code snippet to explain
- {{detail_level}}: Level of detail (default: detailed)
- {{focus_aspect}}: Specific aspect to emphasize""",

        "code-debug_helper": """I want you to act as a debug helper. I will provide you with {{code}} and {{error_description}}, and you will:

1. Analyze the code to identify potential issues
2. Explain what is likely causing the problem
3. Suggest specific fixes with code examples
4. Explain why the fix works
5. Recommend preventive measures to avoid similar issues

## Constraints

- Provide {{num_solutions}} alternative solutions if applicable (default: 2)
- Explain the root cause, not just symptoms
- Consider edge cases and potential side effects of fixes
- Suggest debugging strategies if the issue is unclear

## Variables

- {{code}}: The problematic code
- {{error_description}}: Description of the issue or error message
- {{num_solutions}}: Number of alternative solutions to provide""",

        "document-summarize_chapter": """I want you to act as a chapter summarizer. I will provide you with {{chapter_content}}, and you will:

1. Extract the main topic and learning objectives
2. List key concepts and definitions
3. Summarize important theorems, algorithms, or methods
4. Highlight critical insights and takeaways
5. Identify connections to previous/future topics

## Constraints

- Keep summary under {{max_length}} words (default: 500)
- Use bullet points for clarity
- Organize hierarchically (main points → sub-points)
- Include page/section references if available

## Variables

- {{chapter_content}}: The chapter text or topic to summarize
- {{max_length}}: Maximum summary length in words (default: 500)
- {{focus_areas}}: Specific aspects to emphasize""",

        "test-generate_quiz": """I want you to act as a quiz generator. I will provide you with {{topic}}, and you will:

1. Create {{num_questions}} questions of type {{question_type}} (default: 5, mixed)
2. Ensure questions test understanding, not just memorization
3. Provide correct answers with detailed explanations
4. Include common wrong answers with explanations of why they're incorrect
5. Indicate difficulty level for each question

## Constraints

- Question types: multiple-choice, true/false, short-answer, problem-solving
- Difficulty range: {{difficulty}} (easy/medium/hard/mixed)
- Cover different cognitive levels: recall, understanding, application, analysis
- Provide point values for each question

## Variables

- {{topic}}: The topic to generate questions about
- {{num_questions}}: Number of questions (default: 5)
- {{question_type}}: Type of questions (default: mixed)
- {{difficulty}}: Difficulty level (default: mixed)""",
    }
    
    return prompts.get(f"{category}-{name}", "")


def create_prompt(category: str, name: str, display_name: str, display_name_en: str, 
                 description: str, description_en: str):
    prompt_code = f"{category}-{name}"
    prompt_dir = PROMPTS_DIR / prompt_code
    prompt_dir.mkdir(parents=True, exist_ok=True)

    prompt_content = get_prompt_content(category, name)
    
    with open(prompt_dir / "PROMPT.md", "w", encoding="utf-8") as f:
        f.write(f"---\nname: {name}\ndescription: {description}\n---\n\n{prompt_content}\n")

    metadata = {
        "category": category,
        "name": name,
        "display_name": display_name,
        "display_name_en": display_name_en,
        "description": description,
        "description_en": description_en,
    }

    with open(prompt_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    readme = f"""# {display_name_en}

{description_en}

## 使用场景

配合任何 Skill 使用，特别适合学习类 Skills。

## 示例

见 PROMPT.md 中的详细示例。
"""

    with open(prompt_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✓ Created prompt: {prompt_code}")


def main():
    for prompt_data in LEARNING_PROMPTS:
        create_prompt(
            category=prompt_data["category"],
            name=prompt_data["name"],
            display_name=prompt_data["display_name"],
            display_name_en=prompt_data["display_name_en"],
            description=prompt_data["description"],
            description_en=prompt_data["description_en"],
        )
    
    print(f"\n✓ Successfully created {len(LEARNING_PROMPTS)} learning prompts")


if __name__ == "__main__":
    main()
