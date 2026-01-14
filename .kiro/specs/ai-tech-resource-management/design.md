# Design Document

## Overview

本设计文档基于现有代码结构，优先重构 `backend/scripts` 目录，实现脚本与数据分离、清晰分类。设计遵循现有 `scripts_v2` 的架构模式，统一所有脚本到新的目录结构。

### 设计目标

1. **脚本与数据分离** - 数据定义独立于脚本逻辑
2. **清晰分类** - 按功能类型组织脚本（seed/sync/check/migrate）
3. **统一基类** - 所有脚本继承统一基类，提供一致的接口
4. **可扩展性** - 易于添加新的数据类型和脚本

## Architecture

### 现有问题分析

**scripts 目录（旧版）**：

- 脚本和数据混合在一起
- 重复的数据库连接代码
- 缺乏统一的错误处理
- 文件命名不一致

**scripts_v2 目录（新版）**：

- 已实现脚本与数据分离
- 有统一的基类 `ScriptBase`
- 但数据文件组织还可以优化
- 部分脚本尚未迁移

### 目标目录结构

```
backend/scripts/
├── __init__.py
├── base.py                    # 脚本基类（从 scripts_v2 迁移）
├── runner.py                  # 脚本运行器（批量执行）
│
├── data/                      # 数据定义（纯数据，无逻辑）
│   ├── __init__.py
│   ├── categories.py          # 领域分类数据
│   ├── domains.py             # 子领域数据
│   ├── prompts.py             # Prompt 模板数据
│   ├── llm_models.py          # LLM 模型数据
│   ├── retrieval_engines.py   # 检索引擎数据
│   ├── skills.py              # 技能数据
│   └── data_sources/          # 数据源（按领域分类）
│       ├── __init__.py
│       ├── immigration.py
│       ├── housing.py
│       ├── career.py
│       ├── finance.py
│       ├── healthcare.py
│       ├── education.py
│       ├── travel.py
│       └── ai_tools.py
│
├── seed/                      # 种子数据脚本
│   ├── __init__.py
│   ├── seed_categories.py
│   ├── seed_domains.py
│   ├── seed_prompts.py
│   ├── seed_llm_models.py
│   ├── seed_retrieval_engines.py
│   ├── seed_data_sources.py
│   ├── seed_skills.py
│   └── seed_all.py            # 批量执行所有 seed
│
└── utils/                     # 工具脚本（检查、迁移、同步、数据库管理）
    ├── __init__.py
    │
    │   # 检查类
    ├── check_db.py            # 数据库连接检查
    ├── check_tables.py        # 表结构检查
    ├── check_config.py        # 配置检查
    ├── check_domains.py       # 领域数据完整性检查
    ├── check_prompts.py       # Prompt 数据检查
    ├── check_skills.py        # 技能数据检查
    │
    │   # 同步类
    ├── sync_llm_models.py     # 从外部源同步 LLM 模型
    ├── sync_skills.py         # 从 GitHub 同步技能
    ├── sync_prompts.py        # 从外部源同步 Prompts
    ├── sync_data_sources.py   # 同步数据源元数据
    │
    │   # 迁移/修复类
    ├── fix_domain_icons.py    # 修复领域图标
    ├── fix_missing_icons.py   # 修复缺失图标
    ├── reorder_categories.py  # 重排分类顺序
    │
    │   # 数据库管理类
    ├── reset_db.py            # 重置数据库
    ├── list_tables.py         # 列出表结构
    └── grant_permissions.py   # 授权权限
```

## Components and Interfaces

### 1. 脚本基类 (base.py)

保持现有 `scripts_v2/base.py` 的设计，包含：

```python
@dataclass
class ScriptResult:
    """脚本执行结果"""
    success: bool
    message: str
    created: int = 0
    updated: int = 0
    deleted: int = 0
    errors: Optional[List[str]] = None

class ScriptBase(ABC):
    """脚本基类 - 提供公共方法"""
    # 日志方法: info(), success(), warning(), error(), progress()
    # 工具方法: get_settings(), get_supabase_client(), get_document_store()
    # 抽象方法: run() -> ScriptResult

class SeedScript(ScriptBase):
    """种子数据脚本基类"""
    # 抽象方法: seed() -> tuple[int, int]

class SyncScript(ScriptBase):
    """同步脚本基类"""
    # 抽象方法: sync() -> int

class CheckScript(ScriptBase):
    """检查脚本基类"""
    # 抽象方法: check() -> bool

class MigrateScript(ScriptBase):
    """迁移脚本基类"""
    # 抽象方法: migrate() -> int
```

### 2. 数据定义模块 (data/)

数据文件只包含纯数据定义，不包含任何逻辑：

```python
# data/categories.py
from typing import Any, Dict, List

CATEGORIES: List[Dict[str, Any]] = [
    {
        "code": "immigration",
        "name": "移民签证",
        "name_en": "Immigration & Visa",
        "icon": "Stamp",
        "color": "bg-red-500",
        "description": "工签、PR、入籍、签证续签等移民相关服务",
        "description_en": "Work permit, PR, citizenship, visa renewal services",
        "is_active": True,
        "sort_order": 1,
    },
    # ... 其他分类
]
```

```python
# data/llm_models.py
from typing import Any, Dict, List

LLM_MODELS: List[Dict[str, Any]] = [
    {
        "name": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    # ... 其他模型
]
```

### 3. 种子脚本模块 (seed/)

每个种子脚本负责一种数据类型：

```python
# seed/seed_categories.py
from scripts.base import SeedScript
from scripts.data.categories import CATEGORIES

class SeedCategoriesScript(SeedScript):
    NAME = "领域分类"
    DESCRIPTION = "填充领域分类数据"
    DOC_TYPE = "domain_category"

    def seed(self) -> tuple[int, int]:
        store = self.get_document_store()
        created, updated = 0, 0

        for cat in CATEGORIES:
            existing = store.find_one(self.DOC_TYPE, {"data->>code": cat["code"]})
            if existing:
                store.update(existing["id"], cat)
                updated += 1
            else:
                store.create(self.DOC_TYPE, cat)
                created += 1

        return created, updated
```

### 4. 脚本运行器 (runner.py)

提供批量执行脚本的能力：

```python
# runner.py
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
        from scripts.seed import (
            SeedCategoriesScript,
            SeedDomainsScript,
            SeedPromptsScript,
            SeedLLMModelsScript,
            SeedRetrievalEnginesScript,
        )
        return self.run_all([
            SeedCategoriesScript,
            SeedDomainsScript,
            SeedPromptsScript,
            SeedLLMModelsScript,
            SeedRetrievalEnginesScript,
        ])
```

## Data Models

### 数据文件组织原则

1. **按实体类型分文件** - 每种实体类型一个文件
2. **数据源按领域分文件** - 数据源数据量大，按领域拆分
3. **统一数据格式** - 所有数据使用 `List[Dict[str, Any]]` 格式
4. **双语支持** - 所有文本字段包含中英文版本

### 数据文件清单

| 文件                   | 数据类型    | 说明                 |
| ---------------------- | ----------- | -------------------- |
| `categories.py`        | 领域分类    | 17 个大类            |
| `domains.py`           | 子领域      | 每个分类下的具体领域 |
| `prompts.py`           | Prompt 模板 | AI 对话提示词        |
| `llm_models.py`        | LLM 模型    | 大语言模型配置       |
| `retrieval_engines.py` | 检索引擎    | RAG 检索策略配置     |
| `skills.py`            | 技能定义    | AI 技能描述          |
| `data_sources/*.py`    | 数据源      | 按领域分类的外部资源 |

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

### Property 1: Data Round-Trip Consistency

_For any_ valid data entity (category, domain, prompt, LLM model, retrieval engine), creating it, then reading it back SHALL produce an equivalent object.

**Validates: Requirements 1.2, 1.3, 2.2, 2.3, 3.2, 4.2, 4.3, 5.2, 6.2**

### Property 2: Unique Default Model Per Provider

_For any_ set of LLM models, at most one model per provider SHALL be marked as default. Setting a new default SHALL unset the previous default for that provider.

**Validates: Requirements 1.5**

### Property 3: Unique Category and Domain Codes

_For any_ category code or domain code, there SHALL be exactly one entity with that code. Attempting to create a duplicate SHALL return an error.

**Validates: Requirements 7.6**

### Property 4: Search Results Match Query

_For any_ search query on prompts, skills, or data sources, all returned results SHALL contain the search term in their name, description, or tags.

**Validates: Requirements 2.4, 3.4, 4.5, 8.1**

### Property 5: Filter Results Match Criteria

_For any_ filter applied (category, status, type), all returned results SHALL match the filter criteria.

**Validates: Requirements 2.5, 3.5, 6.5, 8.2**

### Property 6: Quota Decrement Invariant

_For any_ user with remaining quota > 0, sending a query SHALL decrement the quota by exactly 1. _For any_ user with remaining quota = 0, sending a query SHALL be rejected.

**Validates: Requirements 14.2, 14.5**

### Property 7: Sort Order Consistency

_For any_ list of categories or domains, the items SHALL be returned in ascending sort_order. Reordering SHALL update sort_order values correctly.

**Validates: Requirements 7.4, 11.4**

### Property 8: Active Status Cascade

_For any_ category set to inactive, all its child domains SHALL be hidden from member view. Reactivating the category SHALL restore visibility.

**Validates: Requirements 7.5, 11.5**

### Property 9: Conversation Context Preservation

_For any_ conversation, adding a new message SHALL preserve all previous messages in order. Loading a conversation SHALL return all messages with correct timestamps.

**Validates: Requirements 12.4, 13.2, 13.3**

### Property 10: Authentication Token Validity

_For any_ valid login, the returned access token SHALL be valid for authentication. _For any_ logout, the token SHALL be invalidated.

**Validates: Requirements 15.2, 15.5**

### Property 11: Import/Export Round-Trip

_For any_ set of exported resources, importing them into an empty database SHALL produce an equivalent dataset.

**Validates: Requirements 10.1, 10.2**

### Property 12: Localization Consistency

_For any_ language selection, all UI elements and data fields with localized versions SHALL be returned in the selected language.

**Validates: Requirements 17.1, 17.2**

## Error Handling

### 脚本错误处理

所有脚本继承 `ScriptBase`，统一的错误处理模式：

```python
def run(self) -> ScriptResult:
    try:
        # 执行脚本逻辑
        result = self.execute()
        return ScriptResult(success=True, ...)
    except ValidationError as e:
        self.error(f"验证失败: {e}")
        return ScriptResult(success=False, message=str(e), errors=[str(e)])
    except DatabaseError as e:
        self.error(f"数据库错误: {e}")
        return ScriptResult(success=False, message=str(e), errors=[str(e)])
    except Exception as e:
        self.error(f"未知错误: {e}")
        return ScriptResult(success=False, message=str(e), errors=[str(e)])
```

### API 错误处理

使用现有的 `AppError` 异常类：

```python
from common.errors import AppError

# 验证错误
raise AppError(code="VALIDATION_ERROR", message="Invalid model configuration")

# 资源不存在
raise AppError(code="NOT_FOUND", message="Model not found")

# 重复资源
raise AppError(code="DUPLICATE", message="Category code already exists")
```

## Testing Strategy

### 单元测试

- 测试数据验证逻辑
- 测试脚本基类方法
- 测试数据转换函数

### 属性测试

使用 `hypothesis` 库进行属性测试：

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=50))
def test_category_code_uniqueness(code: str):
    """Property 3: 分类代码唯一性"""
    # 创建第一个分类
    create_category(code=code, name="Test")
    # 尝试创建重复分类应该失败
    with pytest.raises(AppError) as exc:
        create_category(code=code, name="Test 2")
    assert exc.value.code == "DUPLICATE"
```

### 集成测试

- 测试完整的种子数据流程
- 测试 API 端到端流程
- 测试外部同步服务

### 测试配置

- 最小 100 次迭代（属性测试）
- 使用测试数据库隔离
- 每个测试后清理数据
