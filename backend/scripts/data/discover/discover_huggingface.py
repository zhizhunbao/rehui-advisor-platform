# HuggingFace 资源发现脚本 - 通过标签搜索模型和数据集
import time
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS


class DiscoverHuggingFaceScript(ScriptBase):
    """通过标签搜索 HuggingFace 发现模型和数据集"""

    NAME = "discover_huggingface"
    DESCRIPTION = "通过标签搜索 HuggingFace 模型和数据集"

    API_URL = "https://huggingface.co/api"

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"] for tag in TAGS]

    def search_models(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索模型"""
        url = f"{self.API_URL}/models"
        params = {"search": query, "limit": limit, "sort": "downloads"}
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            self.error(f"搜索模型失败: {query} - {e}")
            return []

    def search_datasets(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索数据集"""
        url = f"{self.API_URL}/datasets"
        params = {"search": query, "limit": limit, "sort": "downloads"}
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            self.error(f"搜索数据集失败: {query} - {e}")
            return []

    def discover_all(self) -> List[Dict[str, Any]]:
        """发现所有资源"""
        tags = self.get_all_tags()
        results: List[Dict[str, Any]] = []
        seen_urls: set = set()

        for tag in tags:
            self.info(f"搜索标签: {tag}")

            for model in self.search_models(tag):
                url = f"https://huggingface.co/{model['id']}"
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append({
                    "url": url,
                    "name": model["id"],
                    "description": model.get("pipeline_tag", ""),
                    "source_type": "huggingface",
                    "resource_type": "model",
                    "downloads": model.get("downloads", 0),
                    "tags": [tag.lower()],
                })

            for dataset in self.search_datasets(tag):
                url = f"https://huggingface.co/datasets/{dataset['id']}"
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append({
                    "url": url,
                    "name": dataset["id"],
                    "description": "",
                    "source_type": "huggingface",
                    "resource_type": "dataset",
                    "downloads": dataset.get("downloads", 0),
                    "tags": [tag.lower()],
                })

            time.sleep(0.5)

        return results

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 HuggingFace 资源发现...")

        try:
            results = self.discover_all()
            self.success(f"发现 {len(results)} 个资源")
            return ScriptResult(
                success=True,
                message=f"Discovered {len(results)} resources",
                created=len(results),
            )
        except Exception as e:
            self.error(f"发现失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


if __name__ == "__main__":
    script = DiscoverHuggingFaceScript(verbose=True)
    result = script.run()
    print(result)
