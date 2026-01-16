# Skill 创建脚本
import json
import os
from pathlib import Path

from scripts.base import ScriptBase, ScriptResult


class CreateSkillScript(ScriptBase):
    """创建自定义 Skill"""

    NAME = "create_skill"
    DESCRIPTION = "创建自定义 Claude Skill"
    SKILLS_DATA_DIR = Path(__file__).parents[1] / "data" / "skills"
    TEMPLATE_DIR = Path(__file__).parents[1] / "discover" / "raw_data" / "ai_skills" / "skills" / "template"

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        os.makedirs(self.SKILLS_DATA_DIR, exist_ok=True)

    def create_from_domain(self, domain: dict) -> ScriptResult:
        """从 domain 数据创建 skill"""
        domain_code = domain["code"]
        category_code = domain.get("category_code", "general")
        skill_name = f"{category_code}-{domain_code}"
        
        description = self._generate_domain_description(domain)
        instructions = self._generate_domain_instructions(domain)
        keywords = self._generate_domain_keywords(domain)
        
        return self.create(
            name=skill_name,
            description=description,
            instructions=instructions,
            keywords=keywords,
            is_public=True,
            domain_code=domain_code,
            category_code=category_code,
        )

    def _generate_domain_description(self, domain: dict) -> str:
        """生成符合官方标准的 skill 描述"""
        name = domain.get("name", "")
        name_en = domain.get("name_en", "")
        desc = domain.get("description", "")
        category = domain.get("category_code", "")
        
        use_cases = self._generate_use_cases(domain)
        
        return f"专业的{name}({name_en})顾问助手，{desc}。当用户询问以下问题时使用：{use_cases}"

    def _generate_use_cases(self, domain: dict) -> str:
        """根据 domain 生成具体的使用场景"""
        code = domain.get("code", "")
        category = domain.get("category_code", "")
        
        use_case_templates = {
            "immigration": "(1) 签证类型和申请条件 (2) 申请流程和所需材料 (3) 政策解读和注意事项 (4) 续签和身份转换 (5) 常见问题解答",
            "housing": "(1) 房源查找和筛选 (2) 租赁流程和合同 (3) 价格评估和谈判 (4) 入住准备和注意事项 (5) 权益保护",
            "career": "(1) 职业规划和发展 (2) 求职策略和技巧 (3) 简历和面试准备 (4) 行业信息和趋势 (5) 职场问题解答",
            "finance": "(1) 金融产品选择 (2) 账户开设和管理 (3) 投资理财建议 (4) 税务规划 (5) 常见问题解答",
            "healthcare": "(1) 医疗服务查找 (2) 就医流程指导 (3) 保险申请和使用 (4) 健康咨询 (5) 常见问题解答",
            "education": "(1) 学校选择和申请 (2) 课程规划 (3) 学习资源推荐 (4) 认证和评估 (5) 常见问题解答",
            "ai": "(1) 技术选型和对比 (2) 使用指南和最佳实践 (3) 问题诊断和解决 (4) 资源推荐 (5) 常见问题解答",
        }
        
        return use_case_templates.get(category, "(1) 基础咨询 (2) 流程指导 (3) 问题解答 (4) 资源推荐 (5) 注意事项")

    def _generate_domain_instructions(self, domain: dict) -> str:
        """生成 domain 对应的使用说明"""
        name = domain.get("name", "")
        category_code = domain.get("category_code", "")
        
        return f"""# {name}顾问

## 核心能力

提供专业、准确、实用的{name}咨询服务。

## 工作流程

1. **理解需求** - 明确用户的具体问题和背景
2. **提供信息** - 给出准确可靠的专业信息
3. **实用建议** - 提供可操作的具体建议
4. **资源推荐** - 推荐相关的官方资源和服务

## 回答原则

- **准确性** - 基于最新政策和可靠信息
- **实用性** - 提供可执行的具体步骤
- **清晰性** - 用通俗易懂的语言解释
- **完整性** - 涵盖关键注意事项和风险提示

## 重要提示

- 如遇复杂情况，建议咨询专业机构
- 提醒用户注意信息时效性和地区差异
- 必要时提供官方网站和联系方式

## TODO

以下内容需要人工补充：

- [ ] 添加具体的流程指南到 `references/process_guide.md`
- [ ] 添加常见问题清单到 `references/faq.md`
- [ ] 添加官方资源链接到 `references/official_links.md`
- [ ] 添加案例和示例到 `references/examples.md`
"""

    def _generate_domain_keywords(self, domain: dict) -> list[str]:
        """生成 domain 对应的关键词（仅用于 metadata，不放入 frontmatter）"""
        code = domain.get("code", "")
        name = domain.get("name", "")
        name_en = domain.get("name_en", "")
        category = domain.get("category_code", "")
        
        keywords = [code, category, "advisor", "顾问"]
        
        if name:
            keywords.append(name)
        if name_en:
            keywords.extend(name_en.lower().split())
        
        return keywords

    def _create_skill_resources(self, skill_dir: Path) -> None:
        """创建 skill 资源目录和示例文件"""
        references_dir = skill_dir / "references"
        os.makedirs(references_dir, exist_ok=True)
        
        readme_template = """# 参考资料

此目录用于存放详细的参考文档，按需加载。

## 待添加的文件

- `process_guide.md` - 详细流程指南
- `faq.md` - 常见问题解答
- `official_links.md` - 官方资源链接
- `examples.md` - 实际案例和示例

## 使用说明

在 SKILL.md 中引用这些文件：

```markdown
详细流程请参考 [流程指南](references/process_guide.md)
```

Claude 会在需要时自动加载这些文件。
"""
        
        with open(references_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_template)

    def create(
        self,
        name: str,
        description: str,
        instructions: str = "",
        keywords: list[str] | None = None,
        is_public: bool = True,
        domain_code: str | None = None,
        category_code: str | None = None,
    ) -> ScriptResult:
        """创建新的 skill"""
        self.info(f"创建 skill: {name}")

        skill_dir = self.SKILLS_DATA_DIR / name
        if skill_dir.exists():
            return ScriptResult(
                success=False,
                message=f"Skill {name} 已存在",
                errors=[f"目录已存在: {skill_dir}"],
            )

        os.makedirs(skill_dir, exist_ok=True)

        skill_md = self._generate_skill_md(name, description, instructions)
        skill_md_path = skill_dir / "SKILL.md"
        with open(skill_md_path, "w", encoding="utf-8") as f:
            f.write(skill_md)

        self._create_skill_resources(skill_dir)

        metadata = {
            "name": name,
            "description": description,
            "keywords": keywords or [],
            "is_public": is_public,
            "is_official": False,
            "domain_code": domain_code,
            "category_code": category_code,
            "created_at": self._get_timestamp(),
            "repo": "custom",
            "platform": "rehui-advisor",
        }
        metadata_path = skill_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        self.success(f"Skill 已创建: {skill_dir}")
        self.info(f"下一步: 运行导入脚本将 skill 导入数据库")
        return ScriptResult(success=True, message=f"Created skill: {name}", created=1)

    def _generate_skill_md(
        self,
        name: str,
        description: str,
        instructions: str,
    ) -> str:
        """生成符合官方标准的 SKILL.md 内容"""
        frontmatter = f"""---
name: {name}
description: {description}
---

"""
        
        content = frontmatter + instructions
        return content

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def run(self) -> ScriptResult:
        """交互式创建 skill"""
        self.info("=== Claude Skill 创建向导 ===\n")

        name = input("Skill 名称 (小写，用连字符分隔): ").strip()
        if not name:
            return ScriptResult(success=False, message="名称不能为空", errors=["名称为空"])

        description = input("描述 (说明何时使用此 skill): ").strip()
        if not description:
            return ScriptResult(success=False, message="描述不能为空", errors=["描述为空"])

        keywords_input = input("关键词 (逗号分隔，可选): ").strip()
        keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None

        print("\n请输入使用说明 (输入 'END' 结束):")
        instructions_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            instructions_lines.append(line)
        instructions = "\n".join(instructions_lines) if instructions_lines else ""

        return self.create(name, description, instructions, keywords)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "domains",
            Path(__file__).parents[1] / "data" / "domain" / "domains.py"
        )
        domains_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(domains_module)
        DOMAINS = domains_module.DOMAINS
        
        domain = DOMAINS[0]
        print(f"测试创建 skill: {domain['code']} - {domain['name']} ({domain['category_code']})")
        
        script = CreateSkillScript(verbose=True)
        result = script.create_from_domain(domain)
        print(result)
    else:
        script = CreateSkillScript(verbose=True)

        if len(sys.argv) > 1:
            name = sys.argv[1]
            description = sys.argv[2] if len(sys.argv) > 2 else "Custom skill"
            result = script.create(name, description)
        else:
            result = script.run()

        print(result)
