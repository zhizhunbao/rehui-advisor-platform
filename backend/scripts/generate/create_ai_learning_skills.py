# 为 ai_learning 分类生成 Skills（每个 domain 一个 skill）
import os
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "data" / "skills"

AI_LEARNING_DOMAINS = [
    {
        "code": "rl",
        "name": "Reinforcement Learning Assistant",
        "name_cn": "强化学习助手",
        "description": "Comprehensive RL learning assistant. Use when studying Q-Learning, Policy Gradient, Actor-Critic, MDP, or any RL concepts. Helps with concept explanation, code analysis, homework guidance, lab experiments, quiz generation, knowledge summarization, project advice, and paper reading.",
    },
    {
        "code": "ml",
        "name": "Machine Learning Assistant",
        "name_cn": "机器学习助手",
        "description": "Comprehensive ML learning assistant. Use when studying supervised learning, unsupervised learning, regression, classification, clustering, or any ML concepts. Helps with algorithm understanding, implementation guidance, model evaluation, and practical applications.",
    },
    {
        "code": "dl",
        "name": "Deep Learning Assistant",
        "name_cn": "深度学习助手",
        "description": "Comprehensive DL learning assistant. Use when studying neural networks, CNN, RNN, LSTM, Transformer, or any DL architectures. Helps with network design, training strategies, debugging, and optimization techniques.",
    },
    {
        "code": "nlp",
        "name": "NLP Learning Assistant",
        "name_cn": "自然语言处理助手",
        "description": "Comprehensive NLP learning assistant. Use when studying tokenization, embeddings, language models, text classification, or any NLP tasks. Helps with concept understanding, implementation, and practical applications.",
    },
    {
        "code": "cv",
        "name": "Computer Vision Assistant",
        "name_cn": "计算机视觉助手",
        "description": "Comprehensive CV learning assistant. Use when studying image processing, object detection, segmentation, or any CV tasks. Helps with algorithm understanding, implementation, and model optimization.",
    },
    {
        "code": "llm",
        "name": "LLM Learning Assistant",
        "name_cn": "大语言模型助手",
        "description": "Comprehensive LLM learning assistant. Use when studying transformer architecture, attention mechanisms, pre-training, fine-tuning, or prompt engineering. Helps with understanding LLM principles and practical applications.",
    },
]


def create_skill(category_code: str, domain_code: str, name: str, name_cn: str, description: str):
    skill_code = f"{category_code}-{domain_code}"
    skill_dir = SKILLS_DIR / skill_code
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = f"""---
name: {name}
description: {description}
---

# {name}

## Capabilities

### 1. Concept Explanation
Explain complex concepts in simple terms with real-world analogies and visual descriptions.

### 2. Code Analysis
Analyze and explain algorithm implementations, trace execution flow, and identify key components.

### 3. Homework Guidance
Help understand assignment requirements and develop solution approaches without providing direct answers.

### 4. Lab Experiments
Guide through hands-on experiments with step-by-step instructions and result interpretation.

### 5. Quiz Generation
Create practice questions and exercises with detailed explanations to test understanding.

### 6. Knowledge Summarization
Generate concise summaries, flashcards, and knowledge maps for efficient review.

### 7. Project Advisory
Provide guidance on project selection, design, implementation, and optimization.

### 8. Paper Reading
Help understand research papers by extracting key insights and explaining complex formulations.

## TODO: Complete this skill

Add specific content for each capability:

1. **Detailed Instructions**: Step-by-step guides for each capability
2. **Examples**: Concrete usage scenarios
3. **Best Practices**: Tips and recommendations
4. **Common Pitfalls**: What to avoid
5. **Resources**: Links to course materials and references

## References

See `references/` directory for detailed documentation and examples.
"""

    with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_md)

    references_dir = skill_dir / "references"
    references_dir.mkdir(exist_ok=True)

    readme_content = f"""# {name} - References

This directory contains detailed documentation and reference materials.

## Structure

- `concepts/` - Core concept explanations
- `examples/` - Code examples and implementations
- `exercises/` - Practice problems and solutions
- `papers/` - Key research papers and summaries
- `resources/` - Additional learning materials
"""

    with open(references_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    metadata = {
        "domain_code": domain_code,
        "category_code": category_code,
        "keywords": [domain_code, "learning", "education", "ai", "course", "study"],
    }

    import json
    with open(skill_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✓ Created skill: {skill_code}")


def main():
    category_code = "ai_learning"
    
    for domain in AI_LEARNING_DOMAINS:
        create_skill(
            category_code=category_code,
            domain_code=domain["code"],
            name=domain["name"],
            name_cn=domain["name_cn"],
            description=domain["description"],
        )
    
    print(f"\n✓ Successfully created {len(AI_LEARNING_DOMAINS)} skills")


if __name__ == "__main__":
    main()
