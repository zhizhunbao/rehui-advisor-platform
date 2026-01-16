# LangChain 实现
from scripts.discover.evaluate.rag.base import RAGFramework, RAGResult


class LangChainRAG(RAGFramework):
    """LangChain RAG 实现"""

    NAME = "langchain"

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        super().__init__(docs_dir)
        self.vectorstore = None
        self.retriever = None
        self.llm = None

    def build_index(self, docs: list[str]) -> None:
        """构建 LangChain 索引"""
        from langchain_groq import ChatGroq
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = [Document(page_content=doc) for doc in docs]
        chunks = splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma.from_documents(chunks, embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """LangChain 查询"""
        docs = self.retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"Answer based on context:\n{context}\n\nQuestion: {question}"
        response = self.llm.invoke(prompt)

        return RAGResult(
            answer=response.content,
            sources=[doc.page_content[:100] for doc in docs],
            latency_ms=0,
            tokens_used=0,
        )
