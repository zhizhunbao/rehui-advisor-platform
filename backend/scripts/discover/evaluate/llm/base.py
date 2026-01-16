# LLM 评测基类 - 对比各 LLM provider 的效果和成本
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time


@dataclass
class LLMResult:
    """LLM 调用结果"""
    answer: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass
class LLMBenchmarkResult:
    """LLM 基准测试结果"""
    provider: str
    model: str
    accuracy: float
    avg_latency_ms: float
    total_tokens: int
    total_cost_usd: float
    is_free: bool


class LLMProvider(ABC):
    """LLM Provider 抽象基类"""

    NAME: str = ""
    MODEL: str = ""
    IS_FREE: bool = False
    COST_PER_1K_INPUT: float = 0.0
    COST_PER_1K_OUTPUT: float = 0.0

    @abstractmethod
    def generate(self, prompt: str) -> LLMResult:
        """生成回答"""
        pass

    def benchmark(self, questions: list[dict]) -> LLMBenchmarkResult:
        """运行基准测试"""
        total_latency = 0.0
        total_tokens = 0
        total_cost = 0.0
        correct = 0

        for q in questions:
            start = time.time()
            result = self.generate(q["prompt"])
            latency = (time.time() - start) * 1000

            if self._check_answer(result.answer, q.get("expected", "")):
                correct += 1

            total_latency += latency
            total_tokens += result.input_tokens + result.output_tokens
            total_cost += result.cost_usd

        return LLMBenchmarkResult(
            provider=self.NAME,
            model=self.MODEL,
            accuracy=correct / len(questions) if questions else 0,
            avg_latency_ms=total_latency / len(questions) if questions else 0,
            total_tokens=total_tokens,
            total_cost_usd=total_cost,
            is_free=self.IS_FREE,
        )

    def _check_answer(self, answer: str, expected: str) -> bool:
        if not expected:
            return True
        return expected.lower() in answer.lower()
