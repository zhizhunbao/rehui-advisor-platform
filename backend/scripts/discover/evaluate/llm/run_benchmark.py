# LLM Provider 基准测试 - 对比各免费 LLM 的效果
from dotenv import load_dotenv
load_dotenv()

from scripts.discover.evaluate.llm.base import LLMBenchmarkResult
from scripts.discover.evaluate.llm.impl_groq import GroqProvider
from scripts.discover.evaluate.llm.impl_gemini import GeminiProvider
from scripts.discover.evaluate.llm.impl_openrouter import OpenRouterProvider
from scripts.discover.evaluate.llm.impl_together import TogetherProvider
from scripts.discover.evaluate.llm.impl_cerebras import CerebrasProvider
from scripts.discover.evaluate.llm.impl_sambanova import SambaNovaProvider
from scripts.discover.evaluate.llm.impl_cohere import CohereProvider
from scripts.discover.evaluate.llm.data.test_prompts import TEST_PROMPTS


def run_benchmark() -> list[LLMBenchmarkResult]:
    """运行所有 provider 的基准测试"""
    providers = [
        GroqProvider(),
        GeminiProvider(),
        OpenRouterProvider(),
        TogetherProvider(),
        CerebrasProvider(),
        SambaNovaProvider(),
        CohereProvider(),
    ]

    results = []
    for provider in providers:
        print(f"\n{'='*50}")
        print(f"Testing: {provider.NAME} ({provider.MODEL})")
        print("="*50)

        try:
            result = provider.benchmark(TEST_PROMPTS)
            results.append(result)

            print(f"Accuracy: {result.accuracy:.1%}")
            print(f"Avg Latency: {result.avg_latency_ms:.0f}ms")
            print(f"Free: {'Yes' if result.is_free else 'No'}")

        except Exception as e:
            print(f"Error: {e}")

    return results


def print_comparison(results: list[LLMBenchmarkResult]) -> None:
    """打印对比结果"""
    print("\n" + "="*70)
    print("LLM Provider Comparison (Free Tier)")
    print("="*70)
    print(f"{'Provider':<15} {'Model':<30} {'Accuracy':<10} {'Latency':<10}")
    print("-"*70)

    for r in sorted(results, key=lambda x: x.accuracy, reverse=True):
        print(f"{r.provider:<15} {r.model:<30} {r.accuracy:.1%}      {r.avg_latency_ms:.0f}ms")

    if results:
        winner = max(results, key=lambda x: x.accuracy)
        print(f"\n🏆 Best: {winner.provider} - {winner.model} ({winner.accuracy:.1%})")


if __name__ == "__main__":
    results = run_benchmark()
    print_comparison(results)
