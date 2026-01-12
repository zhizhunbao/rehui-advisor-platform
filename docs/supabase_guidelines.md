# Supabase 使用规范

## 核心原则

**禁止使用 SQLAlchemy + AsyncSession，统一使用 Supabase Python Client API**

## 客户端获取

```python
from src.common.supabase import get_supabase, get_supabase_admin

# 普通客户端（受 RLS 保护）
client = get_supabase()

# 管理员客户端（绕过 RLS，仅后端使用）
admin = get_supabase_admin()
```

## Service 模板

```python
"""示例服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class ExampleService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "examples"

    # ========== 查询 ==========
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

    # ========== 创建 ==========
    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create")
        return response.data[0]

    # ========== 更新 ==========
    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Record {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        response = (
            self.client.table(self.table)
            .update(update_data)
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    # ========== 删除 ==========
    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Record {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()
```

## Router 模板

```python
"""示例路由 - 使用 Supabase API"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from src.modules.example.dto import CreateRequest, UpdateRequest
from src.modules.example.service import ExampleService

router = APIRouter(
    prefix="/examples",
    tags=["examples"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def get_all(page: int = 1, limit: int = 20):
    service = ExampleService()
    data, total = service.find_all(page, limit)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/{id}")
def get_by_id(id: str):
    service = ExampleService()
    data = service.find_by_id(id)
    return success_response(data)


@router.post("/")
def create(data: CreateRequest):
    service = ExampleService()
    result = service.create(data.model_dump(exclude_unset=True))
    return success_response(result)


@router.put("/{id}")
def update(id: str, data: UpdateRequest):
    service = ExampleService()
    result = service.update(id, data.model_dump(exclude_unset=True))
    return success_response(result)


@router.delete("/{id}")
def delete(id: str):
    service = ExampleService()
    service.delete(id)
    return success_response(None)
```

## 常用查询模式

### 基础查询

```python
# 查询所有
response = client.table("users").select("*").execute()

# 条件查询
response = client.table("users").select("*").eq("status", "active").execute()

# 单条查询（可能为空）
response = client.table("users").select("*").eq("id", id).maybe_single().execute()

# 单条查询（必须存在）
response = client.table("users").select("*").eq("id", id).single().execute()
```

### 分页查询

```python
response = (
    client.table("users")
    .select("*", count="exact")
    .order("created_at", desc=True)
    .range((page - 1) * limit, page * limit - 1)
    .execute()
)
data = response.data
total = response.count
```

### 复杂过滤

```python
# 多条件
response = (
    client.table("users")
    .select("*")
    .eq("status", "active")
    .gte("created_at", start_date)
    .lte("created_at", end_date)
    .execute()
)

# OR 条件
response = (
    client.table("users")
    .select("*")
    .or_("name.ilike.%search%,email.ilike.%search%")
    .execute()
)

# IN 条件
response = (
    client.table("users")
    .select("*")
    .in_("status", ["active", "pending"])
    .execute()
)

# NULL 检查
response = (
    client.table("users")
    .select("*")
    .is_("deleted_at", "null")
    .execute()
)
```

### 关联查询

```python
# 查询关联数据
response = (
    client.table("orders")
    .select("*, users(name, email)")
    .eq("status", "pending")
    .execute()
)
```

## 常用过滤器速查

| 方法 | 说明 | 示例 |
|------|------|------|
| `eq(col, val)` | 等于 | `.eq("name", "John")` |
| `neq(col, val)` | 不等于 | `.neq("status", "deleted")` |
| `gt(col, val)` | 大于 | `.gt("age", 18)` |
| `gte(col, val)` | 大于等于 | `.gte("price", 100)` |
| `lt(col, val)` | 小于 | `.lt("stock", 10)` |
| `lte(col, val)` | 小于等于 | `.lte("rating", 5)` |
| `like(col, pattern)` | 模糊匹配 | `.like("name", "%John%")` |
| `ilike(col, pattern)` | 忽略大小写模糊匹配 | `.ilike("name", "%john%")` |
| `is_(col, val)` | IS (null/true/false) | `.is_("deleted_at", "null")` |
| `in_(col, vals)` | IN 数组 | `.in_("id", ["a", "b"])` |
| `or_(filters)` | OR 条件 | `.or_("a.eq.1,b.eq.2")` |

## 常用修饰器速查

| 方法 | 说明 | 示例 |
|------|------|------|
| `order(col, desc=False)` | 排序 | `.order("created_at", desc=True)` |
| `limit(count)` | 限制数量 | `.limit(10)` |
| `range(start, end)` | 分页范围 | `.range(0, 9)` |
| `single()` | 返回单条（必须存在） | `.single()` |
| `maybe_single()` | 返回单条或 None | `.maybe_single()` |

## 注意事项

1. **Service 不需要 db 参数** - 直接在 `__init__` 中获取 client
2. **Router 不需要 Depends(get_db)** - 移除所有 AsyncSession 依赖
3. **使用同步方法** - Supabase Python Client 是同步的，不需要 async/await
4. **错误处理** - 查询前检查记录是否存在，抛出 AppError
5. **分页使用 range** - `range(start, end)` 是包含边界的
