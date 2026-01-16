# 从 domains 批量创建 skills
import importlib.util
from pathlib import Path

from scripts.base import ScriptBase, ScriptResult
from scripts.generate.create_skill import CreateSkillScript


class CreateSkillsFromDomainsScript(ScriptBase):
    """从所有 domains 批量创建 skills"""

    NAME = "create_skills_from_domains"
    DESCRIPTION = "从 domains 数据批量创建对应的 skills"

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.skill_creator = CreateSkillScript(verbose=verbose)
        self._load_domains()

    def _load_domains(self) -> None:
        """动态加载 domains 数据"""
        spec = importlib.util.spec_from_file_location(
            "domains",
            Path(__file__).parents[1] / "data" / "domain" / "domains.py"
        )
        domains_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(domains_module)
        self.DOMAINS = domains_module.DOMAINS

    def run(self) -> ScriptResult:
        """批量创建 skills"""
        self.info(f"开始从 {len(self.DOMAINS)} 个 domains 创建 skills...")

        created = 0
        skipped = 0
        errors = []

        for domain in self.DOMAINS:
            domain_code = domain["code"]
            domain_name = domain["name"]

            try:
                result = self.skill_creator.create_from_domain(domain)
                if result.success:
                    created += 1
                    self.info(f"  ✓ {domain_name} ({domain_code})")
                else:
                    skipped += 1
                    self.info(f"  - {domain_name} ({domain_code}): {result.message}")
            except Exception as e:
                errors.append(f"{domain_code}: {str(e)}")
                self.error(f"  ✗ {domain_name} ({domain_code}): {e}")

        self.success(f"完成！创建 {created} 个，跳过 {skipped} 个")
        if errors:
            self.error(f"错误: {len(errors)} 个")

        return ScriptResult(
            success=len(errors) == 0,
            message=f"Created {created} skills",
            created=created,
            errors=errors if errors else None,
        )


if __name__ == "__main__":
    import sys
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    script = CreateSkillsFromDomainsScript(verbose=True)
    result = script.run()
    print(result)
