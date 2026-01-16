# DSPy 实现 - 编程式 LLM，无需写 prompt
from scripts.discover.evaluate.rag.base import RAGFramework, RAGResult


class DSPyRAG(RAGFramework):
    """DSPy RAG 实现"""

    NAME = "dspy"

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        super().__init__(docs_dir)
        self.retriever = None
        self.rag_module = None

    def build_index(self, docs: list[str]) -> None:
        """构建 DSPy 索引"""
        import dspy
        from dspy.retrieve.chromadb_rm import ChromadbRM

        lm = dspy.LM("openai/gpt-4o-mini", temperature=0)
        dspy.configure(lm=lm)

        self.retriever = ChromadbRM(
            collection_name="test_collection",
            persist_directory="./chroma_dspy",
            k=4
        )

        for i, doc in enumerate(docs):
            self.retriever._collection.add(
                documents=[doc],
                ids=[f"doc_{i}"]
            )

        self.rag_module = self._create_rag_module()

    def _create_rag_module(self):
        """创建 DSPy RAG 模块"""
        import dspy

        class RAG(dspy.Module):
            def __init__(self, retriever):
                super().__init__()
                self.retriever = retriever
                self.generate = dspy.ChainOfThought("context, question -> answer")

            def forward(self, question):
                context = self.retriever(question)
                return self.generate(context=context, question=question)

        return RAG(self.retriever)

    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """DSPy 查询"""
        result = self.rag_module(question)

        return RAGResult(
            answer=result.answer,
            sources=[],
            latency_ms=0,
            tokens_used=0,
        )
