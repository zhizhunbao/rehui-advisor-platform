# LlamaIndex 实现
from scripts.discover.evaluate.rag.base import RAGFramework, RAGResult


class LlamaIndexRAG(RAGFramework):
    """LlamaIndex RAG 实现"""

    NAME = "llamaindex"

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        super().__init__(docs_dir)
        self.index = None
        self.query_engine = None

    def build_index(self, docs: list[str]) -> None:
        """构建 LlamaIndex 索引"""
        from llama_index.core import VectorStoreIndex, Document, Settings
        from llama_index.llms.openai import OpenAI
        from llama_index.embeddings.openai import OpenAIEmbedding

        Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
        Settings.embed_model = OpenAIEmbedding()

        documents = [Document(text=doc) for doc in docs]
        self.index = VectorStoreIndex.from_documents(documents)
        self.query_engine = self.index.as_query_engine(similarity_top_k=4)

    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """LlamaIndex 查询"""
        response = self.query_engine.query(question)

        sources = []
        if hasattr(response, "source_nodes"):
            sources = [node.text[:100] for node in response.source_nodes]

        return RAGResult(
            answer=str(response),
            sources=sources,
            latency_ms=0,
            tokens_used=0,
        )
