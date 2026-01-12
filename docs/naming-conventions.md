---
inclusion: always
---

# 命名规范

## 文件命名

### 后端 (Python/FastAPI)

| 类型     | 命名规则                 | 示例                 |
| -------- | ------------------------ | -------------------- |
| 模块目录 | `{module}/`              | `auth/`, `advisor/`  |
| Router   | `{module}/router.py`     | `auth/router.py`     |
| Service  | `{module}/service.py`    | `auth/service.py`    |
| DTO      | `{module}/dto.py`        | `auth/dto.py`        |
| Model    | `models/{module}.py`     | `models/user.py`     |
| 测试     | `tests/test_{module}.py` | `tests/test_auth.py` |

### 前端

| 类型    | 命名规则                           | 示例                  |
| ------- | ---------------------------------- | --------------------- |
| 组件    | `{ComponentName}.tsx` (PascalCase) | `FlightCard.tsx`      |
| Hook    | `use{HookName}.ts`                 | `useFlightSearch.ts`  |
| Service | `{module}.service.ts`              | `flight.service.ts`   |
| Types   | `{module}.types.ts`                | `flight.types.ts`     |
| Locales | `locales/index.ts`                 | 每层/模块一个         |
| 测试    | `{file}.test.tsx`                  | `FlightCard.test.tsx` |

## 变量命名 (Python)

```python
# 变量和函数：snake_case
flight_list = []
def search_flights(): ...

# 常量：UPPER_SNAKE_CASE
MAX_SEARCH_RESULTS = 100

# 类：PascalCase
class FlightService: ...

# Pydantic Model：PascalCase
class FlightSearchParams(BaseModel): ...

# 枚举成员：UPPER_SNAKE_CASE
class CabinClass(str, Enum):
    ECONOMY = "ECONOMY"
    BUSINESS = "BUSINESS"

# 布尔变量：is_, has_, can_, should_ 前缀
is_loading = True
has_error = False
```

## 函数命名 (Python)

```python
# 获取：get_, fetch_, find_
def get_flight_by_id(id: str): ...

# 设置：set_, update_
def set_search_params(): ...

# 检查：is_, has_, can_, validate_
def is_valid_airport_code(): ...

# 转换：to_, from_, parse_, format_
def to_response_dto(): ...

# 异步：async def
async def fetch_flights(): ...
```

## API 路由

```typescript
GET    /api/flights           // 获取列表
GET    /api/flights/:id       // 获取单个
POST   /api/flights           // 创建
PUT    /api/flights/:id       // 更新
DELETE /api/flights/:id       // 删除
```

## 国际化 Locales

```typescript
// 导出名：{module}Locales
export const advisorLocales = { zh: {}, en: {} };
export const adminLocales = { zh: {}, en: {} };
export const authLocales = { zh: {}, en: {} };
export const viewsLocales = { zh: {}, en: {} };
```
