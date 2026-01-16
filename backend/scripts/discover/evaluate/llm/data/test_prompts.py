# LLM 测试提示词 - 评估各 provider 的能力
from typing import Any

TEST_PROMPTS: list[dict[str, Any]] = [
    {
        "category": "coding",
        "prompt": "Write a Python function to check if a string is a palindrome. Return only the code.",
        "expected": "def",
    },
    {
        "category": "coding",
        "prompt": "What is the time complexity of binary search?",
        "expected": "O(log n)",
    },
    {
        "category": "reasoning",
        "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
        "expected": "no",
    },
    {
        "category": "knowledge",
        "prompt": "What is the capital of France?",
        "expected": "Paris",
    },
    {
        "category": "math",
        "prompt": "What is 15% of 80?",
        "expected": "12",
    },
    {
        "category": "coding",
        "prompt": "Explain what a closure is in JavaScript in one sentence.",
        "expected": "function",
    },
    {
        "category": "reasoning",
        "prompt": "A bat and ball cost $1.10. The bat costs $1 more than the ball. How much does the ball cost?",
        "expected": "0.05",
    },
    {
        "category": "knowledge",
        "prompt": "What programming language is PyTorch written in?",
        "expected": "Python",
    },
]
