---
inclusion: always
---

# 后端代码模板 (Python/FastAPI + Supabase)

## 目录结构

```
backend/src/
├── common/                            # 公共模块
│   ├── auth.py                        # 认证 (get_current_admin)
│   ├── errors.py                      # 错误类型 (AppError, AppErrorCode)
│   ├── logger.py                      # 日志工具
│   ├── middleware.py                  # 中间件
│   ├── response.py                    # 响应格式 (success_response)
│   └── supabase.py                    # Supabase 客户端
├── models/                            # Pydantic 模型 (用于类型定义)
│   ├── base.py
│   ├── user.py
│   └── ...
├── modules/                           # 业务模块
│   ├── admin/                         # 管理后台
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── dto.py
│   │   └── __init__.py
│   ├── advisor/
│   ├── auth/
│   └── ...
├── config.py                          # 配置
└── main.py                            # 入口
```

## Service 类

```python
# modules/{module}/service.py
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class {Module}Service:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "{modules}"

    def find_all(self, page: int = 1, limit: int = 20) -> tuple[list[dict], int]:
        response = (
            self.client.table(self.table)
            .select("*", count="exact")
            .order("created_at", desc=True)
            .range((page - 1) * limit, page * limit - 1)
            .execute()
        )
        return response.data, response.count or 0

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create")
        return response.data[0]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"{Module} {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"{Module} {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()
```

## Router

```python
# modules/{module}/router.py
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from src.modules.{module}.dto import Create{Module}Request, Update{Module}Request
from src.modules.{module}.service import {Module}Service

router = APIRouter(
    prefix="/{modules}",
    tags=["{module}"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def find_all(page: int = 1, limit: int = 20):
    service = {Module}Service()
    data, total = service.find_all(page, limit)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/{id}")
def find_by_id(id: str):
    service = {Module}Service()
    data = service.find_by_id(id)
    return success_response(data)


@router.post("/")
def create(data: Create{Module}Request):
    service = {Module}Service()
    result = service.create(data.model_dump(exclude_unset=True))
    return success_response(result)


@router.put("/{id}")
def update(id: str, data: Update{Module}Request):
    service = {Module}Service()
    result = service.update(id, data.model_dump(exclude_unset=True))
    return success_response(result)


@router.delete("/{id}")
def delete(id: str):
    service = {Module}Service()
    service.delete(id)
    return success_response(None)
```

## DTO (Pydantic)

**规则：所有字段必填，不使用默认值**

```python
# modules/{module}/dto.py
from pydantic import BaseModel


# ✅ 正确：所有字段必填
class Create{Module}Request(BaseModel):
    name: str
    description: str
    category: str
    is_active: bool


class Update{Module}Request(BaseModel):
    name: str
    description: str
    category: str
    is_active: bool


# ❌ 错误：使用可选字段或默认值
class Create{Module}Request(BaseModel):
    name: str
    description: str | None = None  # 禁止
    category: str = "general"       # 禁止
```

## 模块导出

```python
# modules/{module}/__init__.py
from src.modules.{module}.router import router as {module}_router
from src.modules.{module}.service import {Module}Service

__all__ = ["{module}_router", "{Module}Service"]
```

---

## 公共模块

### AppError 异常

```python
# common/errors.py
from enum import Enum
from typing import Any


class AppErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    DUPLICATE = "DUPLICATE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AppError(Exception):
    def __init__(self, code: AppErrorCode, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details
```

### 统一响应格式

```python
# common/response.py
from typing import Any


def success_response(data: Any, meta: dict | None = None) -> dict:
    response = {"success": True, "data": data}
    if meta:
        response["meta"] = meta
    return response
```

### Supabase 客户端

```python
# common/supabase.py
from supabase import create_client, Client
from src.common.config import get_settings

settings = get_settings()
_client: Client | None = None
_admin_client: Client | None = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_anon_key)
    return _client


def get_supabase_admin() -> Client:
    global _admin_client
    if _admin_client is None:
        _admin_client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _admin_client
```

---

## API 响应格式

```python
# 成功响应
{"success": True, "data": T}
{"success": True, "data": list[T], "meta": {"total": int, "page": int, "limit": limit}}

# 错误响应
{"success": False, "error": {"code": str, "message": str, "details": Any}}
```

---

## 命名规范

| 类型     | 命名规则             | 示例                |
| -------- | -------------------- | ------------------- |
| 模块目录 | `{module}/`          | `auth/`, `advisor/` |
| Router   | `router.py`          | `auth/router.py`    |
| Service  | `service.py`         | `auth/service.py`   |
| DTO      | `dto.py`             | `auth/dto.py`       |
| Model    | `models/{module}.py` | `models/user.py`    |

---

## 注意事项

1. **Service 不需要 db 参数** - 直接在 `__init__` 中获取 Supabase client
2. **Router 不需要 Depends(get_db)** - 移除所有 AsyncSession 依赖
3. **使用同步方法** - Supabase Python Client 是同步的，不需要 async/await
4. **错误处理** - 查询前检查记录是否存在，抛出 AppError
5. **分页使用 range** - `range(start, end)` 是包含边界的
6. **DTO 字段必填** - 所有 DTO 字段都必须是必填的，禁止使用 `| None` 或默认值
