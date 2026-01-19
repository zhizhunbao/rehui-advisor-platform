#!/usr/bin/env python3
# 课程目录标准化脚本

import shutil
from pathlib import Path
from typing import Dict, List

# 标准目录结构
STANDARD_DIRS = [
    "slides",
    "labs", 
    "assignments",
    "notes",
    "code",
    "textbook",
    "resources",
    "quizzes",
    "schedule",
    "skills",
    "prompts",
]

# Brightspace 目录映射到标准目录
BRIGHTSPACE_MAPPING = {
    "Lecture Slides": "slides",
    "Lectures": "slides",
    "Labs": "labs",
    "Assignments": "assignments",
    "Textbook": "textbook",
    "Weekly Schedule": "schedule",
    "Course Information": "schedule",
    "Hybrid Activities": "resources",
    "Hybrid Resources": "resources",
    "Asynchronous material": "resources",
}

# 课程配置
COURSES = {
    "rl": {
        "name": "强化学习",
        "name_en": "Reinforcement Learning",
        "code": "CST8509",
        "semester": "2026 Winter",
    },
    "ml": {
        "name": "机器学习",
        "name_en": "Machine Learning", 
        "code": "CST8506",
        "semester": "2025 Fall",
    },
    "nlp": {
        "name": "自然语言处理",
        "name_en": "Natural Language Processing",
        "code": "CST8xxx",
        "semester": "2026 Winter",
    },
    "dl": {
        "name": "深度学习",
        "name_en": "Deep Learning",
        "code": "CST8xxx",
        "semester": "",
    },
    "mv": {
        "name": "机器视觉",
        "name_en": "Machine Vision",
        "code": "CST8xxx",
        "semester": "",
    },
    "llm": {
        "name": "大语言模型",
        "name_en": "Large Language Models",
        "code": "",
        "semester": "",
    },
}


def create_standard_structure(course_dir: Path, dry_run: bool = True):
    """创建标准目录结构"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}处理课程: {course_dir.name}")
    
    for dir_name in STANDARD_DIRS:
        target_dir = course_dir / dir_name
        if not target_dir.exists():
            print(f"  创建目录: {dir_name}/")
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                (target_dir / ".gitkeep").touch()


def migrate_brightspace_data(course_dir: Path, brightspace_dir: Path, dry_run: bool = True):
    """从 Brightspace 数据迁移到标准目录"""
    if not brightspace_dir.exists():
        print(f"  跳过: Brightspace 数据不存在 ({brightspace_dir})")
        return
    
    print(f"  从 Brightspace 迁移数据...")
    
    for bs_dir in brightspace_dir.iterdir():
        if not bs_dir.is_dir():
            continue
        
        bs_name = bs_dir.name
        target_name = BRIGHTSPACE_MAPPING.get(bs_name)
        
        if not target_name:
            print(f"    跳过未映射目录: {bs_name}/")
            continue
        
        target_dir = course_dir / target_name
        
        # 检查是否已有文件
        existing_files = list(target_dir.glob("*")) if target_dir.exists() else []
        existing_files = [f for f in existing_files if f.name != ".gitkeep"]
        
        if existing_files:
            print(f"    跳过 {bs_name}/ → {target_name}/ (目标已有文件)")
            continue
        
        print(f"    迁移 {bs_name}/ → {target_name}/")
        
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            for item in bs_dir.iterdir():
                if item.name.startswith("."):
                    continue
                # 跳过 HTML 文件和 links.md（Brightspace 原始数据）
                if item.is_file() and (item.suffix == ".html" or item.name == "links.md"):
                    continue
                target_path = target_dir / item.name
                if item.is_file():
                    shutil.copy2(item, target_path)
                else:
                    shutil.copytree(item, target_path, dirs_exist_ok=True)


def migrate_existing_files(course_dir: Path, dry_run: bool = True):
    """迁移现有非标准目录的文件"""
    print(f"  整理现有文件...")
    
    for item in course_dir.iterdir():
        if not item.is_dir():
            continue
        
        old_name = item.name
        
        # 已经是标准目录，跳过
        if old_name in STANDARD_DIRS:
            continue
        
        # 映射旧目录名到新目录名
        new_name = BRIGHTSPACE_MAPPING.get(old_name)
        
        if new_name:
            target_dir = course_dir / new_name
            print(f"    迁移 {old_name}/ → {new_name}/")
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                # 复制文件而不是移动
                for sub_item in item.iterdir():
                    target_path = target_dir / sub_item.name
                    if target_path.exists():
                        print(f"      跳过已存在: {sub_item.name}")
                    else:
                        try:
                            if sub_item.is_file():
                                shutil.copy2(sub_item, target_path)
                            else:
                                shutil.copytree(sub_item, target_path)
                            print(f"      复制: {sub_item.name}")
                        except Exception as e:
                            print(f"      失败: {sub_item.name} ({e})")
                print(f"      提示: 请手动删除旧目录 {old_name}/")

        else:
            print(f"    保留非标准目录: {old_name}/")


def generate_readme(course_dir: Path, course_key: str, dry_run: bool = True):
    """生成或更新 README.md"""
    readme_path = course_dir / "README.md"
    
    if readme_path.exists():
        print(f"  README.md 已存在，跳过")
        return
    
    course_info = COURSES.get(course_key, {})
    name = course_info.get("name", "")
    name_en = course_info.get("name_en", "")
    code = course_info.get("code", "")
    semester = course_info.get("semester", "")
    
    content = f"""# {name} ({name_en})

**课程代码：** {code}  
**学期：** {semester}

## 课程简介

[待补充]

## 目录结构

- `slides/` - 课件 PPT/PDF
- `labs/` - 实验材料和代码
- `assignments/` - 作业要求和提交
- `notes/` - 个人学习笔记
- `code/` - 代码练习和项目
- `textbook/` - 教材 PDF
- `resources/` - 补充学习资源
- `quizzes/` - 测验题目
- `schedule/` - 课程安排表
- `skills/` - 技能点总结（按主题）
- `prompts/` - AI 辅助学习提示词
- `links.md` - 外部链接汇总

## 学习进度

- [ ] Week 1: 
- [ ] Week 2: 
- [ ] Week 3: 

## 重要链接

- [课程主页]()
- [Brightspace]()
"""
    
    print(f"  生成 README.md")
    if not dry_run:
        readme_path.write_text(content, encoding="utf-8")


def generate_links_md(course_dir: Path, dry_run: bool = True):
    """生成 links.md 模板"""
    links_path = course_dir / "links.md"
    
    if links_path.exists():
        print(f"  links.md 已存在，跳过")
        return
    
    content = """# 外部资源链接

## 视频教程

- 

## 博客文章

- 

## 工具和库

- 

## 论文

- 

## 其他

- 
"""
    
    print(f"  生成 links.md")
    if not dry_run:
        links_path.write_text(content, encoding="utf-8")


def organize_course(course_key: str, dry_run: bool = True):
    """组织单个课程目录"""
    base_dir = Path(__file__).parent.parent
    course_dir = base_dir / "courses" / course_key
    brightspace_dir = base_dir / "scripts" / "scrapers" / "brightspace" / "data" / course_key
    
    if not course_dir.exists():
        print(f"\n跳过: 课程目录不存在 ({course_key})")
        return
    
    # 1. 创建标准目录结构
    create_standard_structure(course_dir, dry_run)
    
    # 2. 迁移现有文件
    migrate_existing_files(course_dir, dry_run)
    
    # 3. 从 Brightspace 迁移数据
    migrate_brightspace_data(course_dir, brightspace_dir, dry_run)
    
    # 4. 生成 README
    generate_readme(course_dir, course_key, dry_run)
    
    # 5. 生成 links.md
    generate_links_md(course_dir, dry_run)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="课程目录标准化工具")
    parser.add_argument("--course", "-c", help="指定课程 (rl, ml, nlp, dl, cv, llm)")
    parser.add_argument("--all", "-a", action="store_true", help="处理所有课程")
    parser.add_argument("--execute", "-e", action="store_true", help="执行操作（默认为预览模式）")
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    if dry_run:
        print("=" * 60)
        print("预览模式 - 不会实际修改文件")
        print("使用 --execute 或 -e 参数执行实际操作")
        print("=" * 60)
    
    if args.all:
        for course_key in COURSES.keys():
            organize_course(course_key, dry_run)
    elif args.course:
        if args.course not in COURSES:
            print(f"错误: 未知课程 '{args.course}'")
            print(f"可用课程: {', '.join(COURSES.keys())}")
            return
        organize_course(args.course, dry_run)
    else:
        parser.print_help()
        print(f"\n可用课程: {', '.join(COURSES.keys())}")
    
    if dry_run:
        print("\n" + "=" * 60)
        print("预览完成 - 使用 -e 参数执行实际操作")
        print("=" * 60)


if __name__ == "__main__":
    main()
