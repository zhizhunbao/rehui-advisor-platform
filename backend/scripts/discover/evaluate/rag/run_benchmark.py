# RAG 框架基准测试 - 用相同数据和问题对比各框架
from dotenv import load_dotenv
load_dotenv()

from scripts.discover.evaluate.rag.base import BenchmarkResult
from scripts.discover.evaluate.rag.impl_langchain import LangChainRAG
from scripts.discover.evaluate.rag.impl_llamaindex import LlamaIndexRAG
from scripts.discover.evaluate.rag.impl_dspy import DSPyRAG
from scripts.discover.evaluate.rag.impl_haystack import HaystackRAG
from scripts.discover.evaluate.rag.impl_pageindex import PageIndexRAG
from scripts.discover.evaluate.rag.data.test_docs import TEST_DOCS
from scripts.discover.evaluate.rag.data.test_questions import TEST_QUESTIONS


def run_benchmark() -> list[BenchmarkResult]:
    """运行所有框架的基准测试"""
    frameworks = [
        LangChainRAG(),
        PageIndexRAG(),
    ]

    results = []
    for fw in frameworks:
        print(f"\n{'='*50}")
        print(f"Testing: {fw.NAME}")
        print("="*50)

        try:
            print("Building index...")
            fw.build_index(TEST_DOCS)

            print("Running benchmark...")
            result = fw.benchmark(TEST_QUESTIONS)
            results.append(result)

            print(f"Accuracy: {result.accuracy:.1%}")
            print(f"Avg Latency: {result.avg_latency_ms:.0f}ms")

        except Exception as e:
            print(f"Error: {e}")

    return results


def print_comparison(results: list[BenchmarkResult]) -> None:
    """打印对比结果"""
    print("\n" + "="*60)
    print("RAG Framework Comparison")
    print("="*60)
    print(f"{'Framework':<15} {'Accuracy':<12} {'Latency':<12} {'Tokens':<10}")
    print("-"*60)

    for r in sorted(results, key=lambda x: x.accuracy, reverse=True):
        print(f"{r.framework:<15} {r.accuracy:.1%}        {r.avg_latency_ms:.0f}ms        {r.total_tokens}")

    if results:
        winner = max(results, key=lambda x: x.accuracy)
        print(f"\n🏆 Best: {winner.framework} ({winner.accuracy:.1%} accuracy)")


if __name__ == "__main__":
    results = run_benchmark()
    print_comparison(results)
