# RAG 评测测试文档
TEST_DOCS = [
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
