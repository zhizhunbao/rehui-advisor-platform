# Haystack 实现 - Pipeline 式 RAG
from scripts.discover.evaluate.rag.base import RAGFramework, RAGResult


class HaystackRAG(RAGFramework):
    """Haystack RAG 实现"""

    NAME = "haystack"

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        super().__init__(docs_dir)
        self.document_store = None
        self.pipeline = None

    def build_index(self, docs: list[str]) -> None:
        """构建 Haystack 索引"""
        from haystack import Document, Pipeline
        from haystack.document_stores.in_memory import InMemoryDocumentStore
        from haystack.components.embedders import (
            OpenAITextEmbedder,
            OpenAIDocumentEmbedder,
        )
        from haystack.components.retrievers.in_memory import (
            InMemoryEmbeddingRetriever,
        )
        from haystack.components.builders import PromptBuilder
        from haystack.components.generators import OpenAIGenerator

        self.document_store = InMemoryDocumentStore()

        documents = [Document(content=doc) for doc in docs]

        doc_embedder = OpenAIDocumentEmbedder()
        docs_with_embeddings = doc_embedder.run(documents)
        self.document_store.write_documents(docs_with_embeddings["documents"])

        template = """
        Answer the question based on the context.
        Context: {% for doc in documents %}{{ doc.content }}{% endfor %}
        Question: {{ question }}
        Answer:
        """

        self.pipeline = Pipeline()
        self.pipeline.add_component("embedder", OpenAITextEmbedder())
        self.pipeline.add_component(
            "retriever",
            InMemoryEmbeddingRetriever(document_store=self.document_store, top_k=4)
        )
        self.pipeline.add_component("prompt", PromptBuilder(template=template))
        self.pipeline.add_component("llm", OpenAIGenerator(model="gpt-4o-mini"))

        self.pipeline.connect("embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever", "prompt.documents")
        self.pipeline.connect("prompt", "llm")

    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """Haystack 查询"""
        result = self.pipeline.run({
            "embedder": {"text": question},
            "prompt": {"question": question}
        })

        answer = result["llm"]["replies"][0] if result["llm"]["replies"] else ""

        return RAGResult(
            answer=answer,
            sources=[],
            latency_ms=0,
            tokens_used=0,
        )
