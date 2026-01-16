# 从 awesome-chatgpt-prompts 提取 Prompts
import json
import os
import re
from pathlib import Path

from scripts.base import ScriptBase, ScriptResult


class ExtractPromptsScript(ScriptBase):
    """从下载的样例中提取 Prompts"""

    NAME = "extract_prompts"
    DESCRIPTION = "从 awesome-chatgpt-prompts 提取 Prompts"
    SOURCE_FILE = Path(__file__).parents[1] / "discover" / "raw_data" / "ai_prompts" / "examples" / "awesome-chatgpt-prompts" / "PROMPTS.md"
    PROMPTS_DATA_DIR = Path(__file__).parents[1] / "data" / "prompts"
    
    PROMPT_MAPPING = {
        "English Translator and Improver": {
            "name": "translate",
            "category": "text_processing",
            "tags": ["translation", "language", "text"],
        },
        "Proofreader": {
            "name": "proofread",
            "category": "text_processing",
            "tags": ["proofreading", "grammar", "text"],
        },
        "Plagiarism Checker": {
            "name": "plagiarism_check",
            "category": "analysis",
            "tags": ["plagiarism", "originality", "analysis"],
        },
        "Summarizer": {
            "name": "summarize",
            "category": "text_processing",
            "tags": ["summary", "text", "condensing"],
        },
        "Spoken English Teacher and Improver": {
            "name": "simplify",
            "category": "text_processing",
            "tags": ["simplification", "text", "readability"],
        },
        "Essay Expander": {
            "name": "expand",
            "category": "text_processing",
            "tags": ["expansion", "writing", "text"],
        },
        "Debater": {
            "name": "pros_cons",
            "category": "analysis",
            "tags": ["analysis", "decision", "comparison"],
        },
        "Advertiser": {
            "name": "generate_email",
            "category": "generation",
            "tags": ["email", "generation", "communication"],
        },
        "Career Counselor": {
            "name": "generate_checklist",
            "category": "generation",
            "tags": ["checklist", "generation", "planning"],
        },
        "Accountant": {
            "name": "extract_key_points",
            "category": "analysis",
            "tags": ["extraction", "analysis", "key-points"],
        },
        "Real Estate Agent": {
            "name": "compare_options",
            "category": "analysis",
            "tags": ["comparison", "analysis", "decision"],
        },
        "Life Coach": {
            "name": "generate_questions",
            "category": "generation",
            "tags": ["questions", "generation", "planning"],
        },
        "Mental Health Adviser": {
            "name": "sentiment_analysis",
            "category": "analysis",
            "tags": ["sentiment", "emotion", "analysis"],
        },
        "Excel Sheet": {
            "name": "json_to_table",
            "category": "format_conversion",
            "tags": ["json", "table", "conversion"],
        },
        "Logistician": {
            "name": "extract_structured_data",
            "category": "format_conversion",
            "tags": ["extraction", "structure", "data"],
        },
    }

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        os.makedirs(self.PROMPTS_DATA_DIR, exist_ok=True)

    def run(self) -> ScriptResult:
        """提取 prompts"""
        self.info("开始提取 Prompts...")

        if not self.SOURCE_FILE.exists():
            return ScriptResult(
                success=False,
                message="源文件不存在",
                errors=[f"文件不存在: {self.SOURCE_FILE}"],
            )

        try:
            with open(self.SOURCE_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            prompts = self._parse_prompts(content)
            created = self._save_prompts(prompts)
            
            self.success(f"成功提取 {created} 个 Prompts")
            return ScriptResult(success=True, message=f"Extracted {created} prompts", created=created)
            
        except Exception as e:
            self.error(f"提取失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])

    def _parse_prompts(self, content: str) -> list[dict]:
        """解析 PROMPTS.md 内容"""
        prompts = []
        
        pattern = r'<summary><strong>(.*?)</strong></summary>\s*##\s*\1\s*(?:Contributed by.*?\n\n)?```md\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for title, instruction in matches:
            if title in self.PROMPT_MAPPING:
                mapping = self.PROMPT_MAPPING[title]
                prompts.append({
                    "title": title,
                    "name": mapping["name"],
                    "category": mapping["category"],
                    "tags": mapping["tags"],
                    "instruction": instruction.strip(),
                })
                self.info(f"  找到: {title} -> {mapping['name']}")
        
        return prompts

    def _save_prompts(self, prompts: list[dict]) -> int:
        """保存提取的 prompts"""
        created = 0
        
        for prompt in prompts:
            prompt_name = f"{prompt['category']}-{prompt['name']}"
            prompt_dir = self.PROMPTS_DATA_DIR / prompt_name
            
            if prompt_dir.exists():
                self.info(f"  跳过已存在: {prompt_name}")
                continue
            
            os.makedirs(prompt_dir, exist_ok=True)
            
            self._save_prompt_md(prompt_dir, prompt)
            self._save_metadata(prompt_dir, prompt)
            
            created += 1
            self.info(f"  ✓ 创建: {prompt_name}")
        
        return created

    def _save_prompt_md(self, prompt_dir: Path, prompt: dict) -> None:
        """保存 PROMPT.md"""
        description = self._generate_description(prompt["name"])
        
        content = f"""---
name: {prompt['name']}
description: {description}
---

{prompt['instruction']}
"""
        
        with open(prompt_dir / "PROMPT.md", "w", encoding="utf-8") as f:
            f.write(content)

    def _save_metadata(self, prompt_dir: Path, prompt: dict) -> None:
        """保存 metadata.json"""
        description = self._generate_description(prompt["name"])
        variables = self._extract_variables(prompt["instruction"])
        
        metadata = {
            "name": prompt["name"],
            "description": description,
            "category": prompt["category"],
            "tags": prompt["tags"],
            "variables": variables,
            "is_public": True,
            "source": "awesome-chatgpt-prompts",
            "original_title": prompt["title"],
            "created_at": self._get_timestamp(),
        }
        
        with open(prompt_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def _generate_description(self, name: str) -> str:
        """生成描述"""
        descriptions = {
            "translate": "翻译文本到指定语言",
            "proofread": "校对文本的语法和拼写",
            "plagiarism_check": "检查文本原创性",
            "summarize": "总结文本的核心内容",
            "simplify": "简化文本使其更易理解",
            "expand": "扩展文本内容",
            "pros_cons": "分析选项的优缺点",
            "generate_email": "生成专业邮件",
            "generate_checklist": "生成任务清单",
            "generate_questions": "生成相关问题",
            "extract_key_points": "提取文本要点",
            "compare_options": "对比多个选项",
            "sentiment_analysis": "分析文本情感",
            "json_to_table": "将JSON转换为表格",
            "extract_structured_data": "提取结构化数据",
        }
        return descriptions.get(name, f"{name} prompt")

    def _extract_variables(self, instruction: str) -> list[dict]:
        """从指令中提取变量"""
        variables = []
        
        patterns = [
            r'\$\{([^}:]+)(?::([^}]+))?\}',
            r'\{\{([^}]+)\}\}',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, instruction)
            for match in matches:
                if isinstance(match, tuple):
                    var_name = match[0]
                    default_value = match[1] if len(match) > 1 and match[1] else None
                else:
                    var_name = match
                    default_value = None
                
                variables.append({
                    "name": var_name,
                    "type": "string",
                    "required": default_value is None,
                    "default": default_value,
                })
        
        return variables

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == "__main__":
    import sys
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    script = ExtractPromptsScript(verbose=True)
    result = script.run()
    print(result)
