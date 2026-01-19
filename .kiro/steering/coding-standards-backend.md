---
inclusion: fileMatch
fileMatchPattern:
  [
    "**/backend/**/*.py",
    "**/backend/**/pyproject.toml",
    "**/backend/**/uv.lock",
  ]
---

# Backend Coding Standards

## Technology Stack

- **Framework**: FastAPI with Pydantic for validation
- **Package Manager**: uv (never use pip or conda)
- **Python Version**: 3.10+ with modern type hints
- **Database**: Supabase (PostgreSQL) via Python client
- **Authentication**: JWT tokens via `common/auth.py`

## Module Structure

```
backend/src/modules/{admin|member}/{feature}/
├── dto.py      # Data Transfer Objects (Pydantic models)
├── service.py  # Business logic
└── router.py   # API endpoints
```

## Import Dependency Rules

**Strict hierarchy - never violate:**

1. `common/` → No dependencies, can be imported by any layer
2. `modules/*/dto.py` → Only import `pydantic` and `common/enum.py`
3. `modules/*/service.py` → Import `common/`, same module `dto`
4. `modules/*/router.py` → Import `common/`, same module `dto` and `service`

**Import from specific files, never use `__init__.py` re-exports:**

```python
# Good
from common.response import success_response
from common.errors import AppError

# Bad
from common import success_response, AppError
```

## Common Module Exports

- `common/enum.py` → Enums and constants only
- `common/helper.py` → Pure utility functions (no side effects)
- `common/errors.py` → Custom exception classes
- `common/response.py` → `success_response()`, `paginate()`
- `common/config.py` → All configuration values
- `common/auth.py` → Authentication utilities
- `common/supabase.py` → Supabase client initialization

## Naming Conventions

- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Type aliases**: `PascalCase` (e.g., `UserDict = dict[str, Any]`)

## Type Annotations

Use Python 3.10+ native types:

```python
# Good
def process_items(items: list[str]) -> dict[str, int]:
    return {"count": len(items)}

# Bad - don't use typing module for basic types
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:
    return {"count": len(items)}
```

Always annotate function signatures and complex variables.

## Layer Responsibilities

### Router Layer (`router.py`)

- Define API endpoints with FastAPI decorators
- Handle request/response serialization via DTOs
- Call service layer methods
- Return responses using `success_response()`
- **Never** contain business logic or database queries

```python
@router.get("/users")
async def get_users(page: int = 1, size: int = 20):
    users = await user_service.get_users(page, size)
    return success_response(data=users)
```

### Service Layer (`service.py`)

- Implement all business logic
- Interact with database (Supabase)
- Raise `AppError` for business errors
- **Never** return HTTP responses or status codes
- **Never** silently catch exceptions

```python
async def get_user_by_id(user_id: str) -> dict:
    user = await supabase.table("users").select("*").eq("id", user_id).single()
    if not user:
        raise AppError("User not found", status_code=404)
    return user
```

### DTO Layer (`dto.py`)

- Define Pydantic models for request/response validation
- Include field validators if needed
- **Never** contain business logic

```python
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)
```

## Error Handling

- Use `AppError` from `common/errors.py` for all business errors
- Include descriptive messages and appropriate status codes
- Let exceptions bubble up to middleware (don't catch unless handling)

```python
from common.errors import AppError

# Good
if not user:
    raise AppError("User not found", status_code=404)

# Bad - don't silently catch
try:
    result = await some_operation()
except Exception:
    pass  # Silent failure
```

## Response Formatting

Always use `success_response()` from `common/response.py`:

```python
from common.response import success_response, paginate

# Simple response
return success_response(data={"user": user})

# Paginated response
return success_response(data=paginate(items, total, page, size))
```

## Configuration Management

- All config values in `common/config.py`
- Use environment variables via `.env` file
- Never hardcode URLs, API keys, or magic numbers

```python
# Good
from common.config import settings
api_url = settings.API_URL

# Bad
api_url = "https://api.example.com"
```

## Code Quality Rules

- **Function length**: Max 50 lines (extract helpers if longer)
- **File length**: Max 500 lines (split into multiple files)
- **Cyclomatic complexity**: Keep functions simple and focused
- **No print statements**: Use `logger` from `common/logger.py`
- **No magic numbers**: Define as named constants

```python
# Good
from common.logger import logger
MAX_RETRY_ATTEMPTS = 3

logger.info(f"Processing user {user_id}")

# Bad
print(f"Processing user {user_id}")
if retry_count > 3:  # Magic number
```

## Database Queries

- Use Supabase Python client from `common/supabase.py`
- Never return raw database objects - transform to dicts/DTOs
- Use proper error handling for database operations

```python
from common.supabase import get_supabase_client

supabase = get_supabase_client()
result = await supabase.table("users").select("*").execute()
```

## Prohibited Practices

- ❌ Using pip or conda (must use uv)
- ❌ Hardcoding configuration values
- ❌ Business logic in router layer
- ❌ HTTP responses in service layer
- ❌ Silent exception catching
- ❌ Print statements in production code
- ❌ Importing from `__init__.py` re-exports
- ❌ Using `typing.List`, `typing.Dict` (use `list`, `dict`)
- ❌ Functions over 50 lines
- ❌ Files over 500 lines
- ❌ Magic numbers without named constants
- ❌ Returning raw database objects

## Dependency Management

```bash
# Add dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Sync dependencies
uv sync

# Never use
pip install package-name  # ❌
```
