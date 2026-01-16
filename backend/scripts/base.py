# 脚本基类
from dataclasses import dataclass


@dataclass
class ScriptResult:
    """脚本执行结果"""
    success: bool
    message: str
    created: int = 0
    updated: int = 0
    deleted: int = 0
    errors: list[str] | None = None


class ScriptBase:
    """脚本基类"""

    NAME: str = ""
    DESCRIPTION: str = ""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def info(self, msg: str) -> None:
        if self.verbose:
            print(f"[INFO] {msg}")

    def success(self, msg: str) -> None:
        if self.verbose:
            print(f"[SUCCESS] {msg}")

    def error(self, msg: str) -> None:
        if self.verbose:
            print(f"[ERROR] {msg}")

    def run(self) -> ScriptResult:
        """执行脚本，子类需实现"""
        raise NotImplementedError
