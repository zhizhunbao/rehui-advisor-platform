# 脚本基类 - 提供公共方法如数据库连接、配置加载、日志输出
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional
import sys


@dataclass
class ScriptResult:
    """脚本执行结果"""
    success: bool
    message: str
    created: int = 0
    updated: int = 0
    deleted: int = 0
    errors: Optional[List[str]] = field(default=None)


class ScriptBase(ABC):
    """脚本基类"""

    NAME: str = ""
    DESCRIPTION: str = ""

    BACKEND_ROOT: Path = Path(__file__).parent.parent
    SCRIPTS_ROOT: Path = Path(__file__).parent

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self._setup_paths()
        self._load_env()

    def _setup_paths(self) -> None:
        """设置 Python 路径"""
        src_path = str(self.BACKEND_ROOT / "src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

    def _load_env(self) -> None:
        """加载环境变量"""
        from dotenv import load_dotenv
        load_dotenv(self.BACKEND_ROOT / ".env")

    def info(self, msg: str) -> None:
        """输出信息日志"""
        print(f"ℹ️  {msg}")

    def success(self, msg: str) -> None:
        """输出成功日志"""
        print(f"✅ {msg}")

    def warning(self, msg: str) -> None:
        """输出警告日志"""
        print(f"⚠️  {msg}")

    def error(self, msg: str) -> None:
        """输出错误日志"""
        print(f"❌ {msg}")

    def progress(self, current: int, total: int, msg: str = "") -> None:
        """输出进度日志"""
        pct = (current / total * 100) if total > 0 else 0
        print(f"  [{current}/{total}] {pct:.0f}% {msg}")

    def get_settings(self) -> Any:
        """获取配置"""
        from common.config import get_settings
        return get_settings()

    def get_supabase_client(self) -> Any:
        """获取 Supabase 客户端"""
        from common.supabase import get_supabase_admin
        return get_supabase_admin()

    def get_document_store(self) -> Any:
        """获取文档存储"""
        from common.document import DocumentStore
        return DocumentStore()

    @abstractmethod
    def run(self) -> ScriptResult:
        """执行脚本的主方法"""
        pass


class CheckScript(ScriptBase):
    """检查脚本基类"""

    @abstractmethod
    def check(self) -> bool:
        """执行检查，返回是否通过"""
        pass

    def run(self) -> ScriptResult:
        """运行检查"""
        try:
            passed = self.check()
            if passed:
                self.success(f"{self.NAME} 检查通过")
                return ScriptResult(success=True, message="Check passed")
            else:
                self.error(f"{self.NAME} 检查失败")
                return ScriptResult(success=False, message="Check failed")
        except Exception as e:
            self.error(f"{self.NAME} 检查出错: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


class SeedScript(ScriptBase):
    """种子数据脚本基类"""

    @abstractmethod
    def seed(self) -> tuple[int, int]:
        """执行种子数据填充，返回 (created, updated)"""
        pass

    def run(self) -> ScriptResult:
        """运行种子脚本"""
        self.info(f"开始填充数据...")

        try:
            created, updated = self.seed()
            self.success(f"完成: 创建 {created}, 更新 {updated}")
            return ScriptResult(
                success=True,
                message="Seeded data",
                created=created,
                updated=updated
            )
        except Exception as e:
            self.error(f"填充失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


class SyncScript(ScriptBase):
    """同步脚本基类"""

    @abstractmethod
    def sync(self) -> int:
        """执行同步，返回同步的记录数"""
        pass

    def run(self) -> ScriptResult:
        """运行同步脚本"""
        self.info(f"开始同步...")

        try:
            count = self.sync()
            self.success(f"同步完成: {count} 条记录")
            return ScriptResult(
                success=True,
                message=f"Synced {count} records",
                updated=count
            )
        except Exception as e:
            self.error(f"同步失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


class MigrateScript(ScriptBase):
    """迁移脚本基类"""

    @abstractmethod
    def migrate(self) -> int:
        """执行迁移，返回影响的行数"""
        pass

    def run(self) -> ScriptResult:
        """运行迁移脚本"""
        self.info(f"开始迁移...")

        try:
            affected = self.migrate()
            self.success(f"迁移完成，影响 {affected} 行")
            return ScriptResult(
                success=True,
                message=f"Migrated {affected} rows",
                updated=affected
            )
        except Exception as e:
            self.error(f"迁移失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])
