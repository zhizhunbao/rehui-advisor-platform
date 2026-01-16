# RAG 评测基类 - 定义统一接口，各框架实现相同功能
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import time


@dataclass
class RAGResult:
    """RAG 查询结果"""
    answer: str
    sources: list[str]
    latency_ms: float
    tokens_used: int


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    framework: str
    accuracy: float
    avg_latency_ms: float
    total_tokens: int
    details: list[dict[str, Any]]


class RAGFramework(ABC):
    """RAG 框架抽象基类 - 所有框架实现相同接口"""

    NAME: str = ""

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        self.docs_dir = Path(docs_dir)
        self.index = None

    @abstractmethod
    def build_index(self, docs: list[str]) -> None:
        """构建索引"""
        pass

    @abstractmethod
    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """查询"""
        pass

    def benchmark(self, questions: list[dict[str, str]]) -> BenchmarkResult:
        """运行基准测试"""
        details = []
        total_latency = 0.0
        total_tokens = 0
        correct = 0

        for q in questions:
            start = time.time()
            result = self.query(q["question"])
            latency = (time.time() - start) * 1000

            is_correct = self._check_answer(result.answer, q.get("expected", ""))
            if is_correct:
                correct += 1

            details.append({
                "question": q["question"],
                "answer": result.answer,
                "expected": q.get("expected", ""),
                "correct": is_correct,
                "latency_ms": latency,
                "tokens": result.tokens_used,
            })

            total_latency += latency
            total_tokens += result.tokens_used

        return BenchmarkResult(
            framework=self.NAME,
            accuracy=correct / len(questions) if questions else 0,
            avg_latency_ms=total_latency / len(questions) if questions else 0,
            total_tokens=total_tokens,
            details=details,
        )

    def _check_answer(self, answer: str, expected: str) -> bool:
        """检查答案是否正确（简单包含检查）"""
        if not expected:
            return True
        return expected.lower() in answer.lower()
