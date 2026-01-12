"""
重构导入路径脚本
- 模块内部使用相对导入
- 生成顶层 __init__.py 统一导出
"""
import os
import re
from pathlib import Path

MODULES_DIR = Path("src/modules")


def get_module_path(file_path: Path) -> str:
    """获取文件所属的模块路径，如 member.auth"""
    rel = file_path.relative_to(MODULES_DIR)
    parts = list(rel.parts[:-1])  # 去掉文件名
    return ".".join(parts)


def convert_to_relative_import(file_path: Path, content: str) -> str:
    """将模块内的绝对导入转换为相对导入"""
    module_path = get_module_path(file_path)
    if not module_path:
        return content
    
    module_parts = module_path.split(".")
    module_prefix = f"src.modules.{module_path}"
    
    lines = content.split("\n")
    new_lines = []
    
    for line in lines:
        # 匹配 from src.modules.xxx.yyy import zzz
        match = re.match(r'^from (src\.modules\.[^\s]+) import (.+)$', line)
        if match:
            import_path = match.group(1)
            imports = match.group(2)
            
            # 检查是否是同一模块内的导入
            if import_path.startswith(module_prefix + "."):
                # 同模块内，转为相对导入
                relative_part = import_path[len(module_prefix) + 1:]
                new_line = f"from .{relative_part} import {imports}"
                new_lines.append(new_line)
                print(f"  {file_path}: {line.strip()} -> {new_line.strip()}")
            elif import_path == module_prefix:
                # 同目录
                new_line = f"from . import {imports}"
                new_lines.append(new_line)
                print(f"  {file_path}: {line.strip()} -> {new_line.strip()}")
            else:
                # 不同模块，检查是否是兄弟模块
                import_parts = import_path.replace("src.modules.", "").split(".")
                
                # 计算相对路径
                # 例如 member.auth 导入 member.advisor -> from ..advisor import xxx
                if len(module_parts) >= 1 and len(import_parts) >= 1:
                    if module_parts[0] == import_parts[0]:
                        # 同一顶级模块下的兄弟模块
                        dots = ".." 
                        rest = ".".join(import_parts[1:])
                        new_line = f"from {dots}{rest} import {imports}"
                        new_lines.append(new_line)
                        print(f"  {file_path}: {line.strip()} -> {new_line.strip()}")
                    else:
                        # 不同顶级模块，保持绝对导入但简化
                        new_lines.append(line)
                else:
                    new_lines.append(line)
        else:
            new_lines.append(line)
    
    return "\n".join(new_lines)


def process_module(module_dir: Path):
    """处理单个模块目录"""
    print(f"\n处理模块: {module_dir}")
    
    for py_file in module_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        if py_file.name == "__init__.py":
            continue
            
        content = py_file.read_text(encoding="utf-8")
        new_content = convert_to_relative_import(py_file, content)
        
        if new_content != content:
            py_file.write_text(new_content, encoding="utf-8")


def generate_top_level_init():
    """生成顶层 __init__.py"""
    exports = []
    
    # 扫描所有模块的 __init__.py 找到导出的 router
    for init_file in MODULES_DIR.rglob("__init__.py"):
        if "__pycache__" in str(init_file):
            continue
        
        rel_path = init_file.relative_to(MODULES_DIR).parent
        if not rel_path.parts:
            continue
            
        module_path = ".".join(rel_path.parts)
        content = init_file.read_text(encoding="utf-8")
        
        # 查找导出的 router
        for match in re.finditer(r'(\w+_router)', content):
            router_name = match.group(1)
            exports.append((module_path, router_name))
    
    # 生成 __init__.py
    lines = ['"""模块统一导出 - 外部只需从这里导入"""', ""]
    
    # 按模块分组
    by_top_module: dict[str, list] = {}
    for module_path, router_name in exports:
        top = module_path.split(".")[0]
        if top not in by_top_module:
            by_top_module[top] = []
        by_top_module[top].append((module_path, router_name))
    
    for top_module, items in sorted(by_top_module.items()):
        lines.append(f"# {top_module.title()} 模块")
        for module_path, router_name in items:
            lines.append(f"from src.modules.{module_path} import {router_name}")
        lines.append("")
    
    # __all__
    all_exports = [r for _, r in exports]
    lines.append(f"__all__ = {all_exports}")
    
    init_content = "\n".join(lines)
    (MODULES_DIR / "__init__.py").write_text(init_content, encoding="utf-8")
    print(f"\n生成 {MODULES_DIR / '__init__.py'}")
    print(init_content)


def main():
    os.chdir(Path(__file__).parent.parent)
    
    print("=" * 60)
    print("重构模块导入")
    print("=" * 60)
    
    # 处理 admin 模块
    process_module(MODULES_DIR / "admin")
    
    # 处理 member 模块
    process_module(MODULES_DIR / "member")
    
    # 生成顶层 __init__.py
    print("\n" + "=" * 60)
    print("生成顶层导出")
    print("=" * 60)
    generate_top_level_init()
    
    print("\n完成！")


if __name__ == "__main__":
    main()
