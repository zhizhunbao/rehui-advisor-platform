# Implementation Plan: Scripts 目录重构

## Overview

优先重构 `backend/scripts` 目录，实现脚本与数据分离、清晰分类。基于现有 `scripts_v2` 的架构模式，统一所有脚本到新的目录结构。

## Tasks

- [x] 1. 创建新的目录结构和基础文件

  - [x] 1.1 创建 `scripts/base.py` 基类文件
    - 从 `scripts_v2/base.py` 迁移，保持现有设计
    - 包含 `ScriptBase`, `SeedScript`, `SyncScript`, `CheckScript`, `MigrateScript`
    - _Requirements: 18.2, 19.2, 20.2_
  - [x] 1.2 创建 `scripts/runner.py` 脚本运行器
    - 实现批量执行脚本的能力
    - 支持 `run_seed_all()` 方法
    - _Requirements: 18.2_
  - [x] 1.3 创建目录结构和 `__init__.py` 文件
    - 创建 `data/`, `seed/`, `utils/` 目录
    - 创建各目录的 `__init__.py`
    - _Requirements: 18.2_

- [x] 2. 迁移数据定义文件到 `data/` 目录

  - [x] 2.1 迁移 `categories.py` 领域分类数据
    - 从 `scripts_v2/data/categories.py` 迁移
    - 包含 17 个领域分类
    - _Requirements: 18.1_
  - [x] 2.2 迁移 `domains.py` 子领域数据
    - 从 `scripts_v2/data/domains.py` 迁移
    - 包含所有子领域定义
    - _Requirements: 18.3_
  - [x] 2.3 迁移 `prompts.py` Prompt 模板数据
    - 从 `scripts_v2/data/prompts.py` 迁移
    - 包含各领域的 Prompt 模板
    - _Requirements: 21.1, 21.4_
  - [x] 2.4 创建 `llm_models.py` LLM 模型数据
    - 从 `scripts/seed/seed_llm.py` 提取数据
    - 包含 6 个主流 LLM 模型配置
    - _Requirements: 19.1_
  - [x] 2.5 创建 `retrieval_engines.py` 检索引擎数据
    - 从 `scripts/seed/seed_retrieval_engines.py` 提取数据
    - 包含 7 种检索策略配置
    - _Requirements: 20.1_
  - [x] 2.6 迁移 `data_sources/` 数据源目录
    - 从 `scripts_v2/data/data_sources/` 迁移
    - 按领域分类组织数据源
    - _Requirements: 6.2_
  - [x] 2.7 创建 `users.py` 用户数据
    - 包含管理员和会员示例数据
    - _Requirements: 7.1_
  - [x] 2.8 创建 `agent_frameworks.py` Agent 框架数据
    - 包含 8 个主流 Agent 框架
    - _Requirements: 3.1_
  - [x] 2.9 创建 `scheduler_jobs.py` 调度任务数据
    - 包含定时任务配置
    - _Requirements: 7.3_

- [x] 3. Checkpoint - 确保数据文件完整

  - 验证所有数据文件可正常导入
  - 确保数据格式一致

- [x] 4. 迁移种子脚本到 `seed/` 目录

  - [x] 4.1 迁移 `seed_categories.py`
    - 从 `scripts_v2/seed/seed_categories.py` 迁移
    - 更新导入路径
    - _Requirements: 18.2_
  - [x] 4.2 迁移 `seed_domains.py`
    - 从 `scripts_v2/seed/seed_domains.py` 迁移
    - 更新导入路径
    - _Requirements: 18.3_
  - [x] 4.3 迁移 `seed_prompts.py`
    - 从 `scripts_v2/seed/seed_prompts.py` 迁移
    - 更新导入路径
    - _Requirements: 21.2, 21.3_
  - [x] 4.4 创建 `seed_llm_models.py`
    - 重构 `scripts/seed/seed_llm.py`
    - 使用新的基类和数据文件
    - _Requirements: 19.2, 19.3_
  - [x] 4.5 创建 `seed_retrieval_engines.py`
    - 重构 `scripts/seed/seed_retrieval_engines.py`
    - 使用新的基类和数据文件
    - _Requirements: 20.2, 20.3_
  - [x] 4.6 迁移 `seed_data_sources.py`
    - 从 `scripts_v2/seed/seed_data_sources.py` 迁移
    - 更新导入路径
    - _Requirements: 6.2_
  - [x] 4.7 创建 `seed_all.py` 批量执行脚本
    - 按顺序执行所有种子脚本
    - 输出执行结果汇总
    - _Requirements: 18.2_
  - [x] 4.8 创建 `seed_users.py` 用户种子脚本
    - 填充管理员和会员示例数据
    - _Requirements: 7.1_
  - [x] 4.9 创建 `seed_agent_frameworks.py` Agent 框架种子脚本
    - 填充 Agent 框架数据源
    - _Requirements: 3.1_
  - [x] 4.10 创建 `seed_scheduler_jobs.py` 调度任务种子脚本
    - 填充定时任务配置
    - _Requirements: 7.3_

- [x] 5. Checkpoint - 确保种子脚本可运行

  - 运行 `seed_all.py` 验证所有脚本
  - 确保数据正确写入数据库

- [x] 6. 迁移工具脚本到 `utils/` 目录

  - [x] 6.1 迁移检查类脚本
    - 迁移 `check_db.py`, `check_domains.py`
    - 更新导入路径，使用新基类
    - _Requirements: 7.1_
  - [x] 6.2 迁移同步类脚本
    - 迁移 `sync_skills.py`
    - 更新导入路径，使用新基类
    - _Requirements: 1.6, 2.6_
  - [x] 6.3 迁移修复/迁移类脚本
    - 迁移 `fix_domain_icons.py`, `fix_missing_icons.py`, `reorder_categories.py`
    - 更新导入路径，使用新基类
    - _Requirements: 7.4_
  - [x] 6.4 迁移数据库管理类脚本
    - 迁移 `reset_db.py`, `list_tables.py`, `grant_permissions.py`
    - 更新导入路径
    - _Requirements: 7.1_

- [x] 7. Checkpoint - 确保工具脚本可运行

  - 测试各类工具脚本
  - 确保功能正常

- [x] 8. 清理旧目录

  - [x] 8.1 删除 `scripts_v2/` 目录
    - 所有内容已迁移到新 `scripts/`
  - [x] 8.2 删除旧的子目录
    - 删除 `check/`, `db/`, `migrate/`, `sync/`, `test/`
    - 保留 `data/`, `seed/`, `utils/`
  - [x] 8.3 补全工具脚本
    - 添加 `sync_models.py`, `sync_prompts.py`
    - 添加 `check_prompts.py`, `check_skills.py`
    - _Requirements: 18.2_

- [x] 9. Final Checkpoint - 完整性验证
  - 运行所有种子脚本
  - 运行所有检查脚本
  - 确保系统正常工作

## Notes

- 任务按优先级排序：先数据文件，再种子脚本，最后工具脚本
- 每个 Checkpoint 确保阶段性成果可用
- 迁移过程中保持旧目录可用，最后统一清理
