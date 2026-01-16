# RAG 基准测试数据
from typing import Any

TEST_DOCS: list[str] = [
    """
    RAG (Retrieval-Augmented Generation) is a technique that combines retrieval 
    and generation. It first retrieves relevant documents from a knowledge base, 
    then uses an LLM to generate answers based on the retrieved context.
    """,
    """
    Vector databases store embeddings and enable similarity search. Popular options 
    include Chroma (local), Pinecone (cloud), Qdrant, and Milvus. Choose based on 
    scale, latency requirements, and deployment preferences.
    """,
    """
    Chunking strategies affect retrieval quality. Common approaches: fixed-size 
    (simple but may split context), recursive (respects structure), semantic 
    (groups related content). Typical chunk size: 500-1000 tokens.
    """,
]

TEST_QUESTIONS: list[dict[str, Any]] = [
    {"question": "What is RAG?", "expected": "retrieval"},
    {"question": "What are popular vector databases?", "expected": "Chroma"},
    {"question": "What is a good chunk size?", "expected": "500"},
]
