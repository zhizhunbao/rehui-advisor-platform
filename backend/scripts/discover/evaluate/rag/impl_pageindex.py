# PageIndex 实现 - 无向量、基于推理的 RAG
from scripts.discover.evaluate.rag.base import RAGFramework, RAGResult


class PageIndexRAG(RAGFramework):
    """PageIndex RAG 实现 - Vectorless, Reasoning-based"""

    NAME = "pageindex"

    def __init__(self, docs_dir: str = "./test_docs") -> None:
        super().__init__(docs_dir)
        self.tree_index = None
        self.docs = []

    def build_index(self, docs: list[str]) -> None:
        """构建 PageIndex 树形索引"""
        self.docs = docs
        self.tree_index = self._build_tree_structure(docs)

    def _build_tree_structure(self, docs: list[str]) -> dict:
        """构建层级树结构（简化版，实际需调用 PageIndex API）"""
        tree = {"root": {"children": []}}

        for i, doc in enumerate(docs):
            lines = doc.strip().split("\n")
            title = lines[0][:50] if lines else f"Section {i}"

            node = {
                "id": f"node_{i}",
                "title": title,
                "content": doc,
                "children": []
            }
            tree["root"]["children"].append(node)

        return tree

    def query(self, question: str, top_k: int = 4) -> RAGResult:
        """PageIndex 查询 - 通过树搜索推理"""
        relevant_nodes = self._tree_search(question)
        context = "\n".join([node["content"] for node in relevant_nodes[:top_k]])
        answer = self._generate_answer(question, context)

        return RAGResult(
            answer=answer,
            sources=[node["title"] for node in relevant_nodes[:top_k]],
            latency_ms=0,
            tokens_used=0,
        )

    def _tree_search(self, question: str) -> list[dict]:
        """树搜索找相关节点（简化版）"""
        nodes = self.tree_index["root"]["children"]
        scored = []

        for node in nodes:
            score = self._relevance_score(question, node["content"])
            scored.append((score, node))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [node for _, node in scored]

    def _relevance_score(self, question: str, content: str) -> float:
        """计算相关性分数（简化版，实际用 LLM 推理）"""
        q_words = set(question.lower().split())
        c_words = set(content.lower().split())
        overlap = len(q_words & c_words)
        return overlap / len(q_words) if q_words else 0

    def _generate_answer(self, question: str, context: str) -> str:
        """生成答案"""
        from groq import Groq
        import os

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            messages=[
                {"role": "system", "content": "Answer based on the context provided."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content
