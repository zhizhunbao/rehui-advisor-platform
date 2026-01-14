# 脚本运行器 - 批量执行脚本
from typing import List, Type
from scripts.base import ScriptBase, ScriptResult


class ScriptRunner:
    """脚本运行器"""

    def run_all(self, scripts: List[Type[ScriptBase]]) -> List[ScriptResult]:
        """批量执行脚本"""
        results = []
        for script_class in scripts:
            script = script_class()
            result = script.run()
            results.append(result)
        return results

    def run_seed_all(self) -> List[ScriptResult]:
        """执行所有种子脚本"""
        from scripts.seed.seed_categories import SeedCategoriesScript
        from scripts.seed.seed_domains import SeedDomainsScript
        from scripts.seed.seed_prompts import SeedPromptsScript
        from scripts.seed.seed_llm_models import SeedLLMModelsScript
        from scripts.seed.seed_retrieval_engines import SeedRetrievalEnginesScript
        from scripts.seed.seed_data_sources import SeedDataSourcesScript
        from scripts.seed.seed_users import SeedUsersScript
        from scripts.seed.seed_agent_frameworks import SeedAgentFrameworksScript
        from scripts.seed.seed_scheduler_jobs import SeedSchedulerJobsScript

        return self.run_all([
            SeedCategoriesScript,
            SeedDomainsScript,
            SeedPromptsScript,
            SeedLLMModelsScript,
            SeedRetrievalEnginesScript,
            SeedDataSourcesScript,
            SeedUsersScript,
            SeedAgentFrameworksScript,
            SeedSchedulerJobsScript,
        ])

    def print_summary(self, results: List[ScriptResult]) -> None:
        """打印执行结果汇总"""
        total = len(results)
        success = sum(1 for r in results if r.success)
        failed = total - success

        print("\n" + "=" * 50)
        print(f"执行完成: {success}/{total} 成功, {failed} 失败")
        print("=" * 50)

        for i, result in enumerate(results, 1):
            status = "✅" if result.success else "❌"
            print(f"{status} [{i}] {result.message}")
            if result.created or result.updated:
                print(f"    创建: {result.created}, 更新: {result.updated}")
            if result.errors:
                for err in result.errors:
                    print(f"    错误: {err}")


if __name__ == "__main__":
    runner = ScriptRunner()
    results = runner.run_seed_all()
    runner.print_summary(results)
