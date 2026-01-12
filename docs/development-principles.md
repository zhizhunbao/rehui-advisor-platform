---
inclusion: always
---

# 开发原则

## 核心原则

### 1. 单一职责原则 (SRP)

每个模块、类、函数只做一件事。

**TypeScript:**

```typescript
// ❌ 错误：一个函数做多件事
async function createUserAndSendEmail(data: UserDto) {
  const user = await prisma.user.create({ data });
  await sendWelcomeEmail(user.email);
  await logUserCreation(user.id);
  return user;
}

// ✅ 正确：职责分离
async function createUser(data: UserDto) {
  return prisma.user.create({ data });
}
// 邮件发送由事件或独立服务处理
```

**Python:**

```python
# ❌ 错误：一个函数做多件事
async def create_user_and_send_email(data: UserDto) -> User:
    user = await db.execute(insert(User).values(**data.model_dump()))
    await send_welcome_email(user.email)
    await log_user_creation(user.id)
    return user

# ✅ 正确：职责分离
async def create_user(data: UserDto) -> User:
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user
# 邮件发送由事件或独立服务处理
```

### 2. 最小原则

- 最小代码：只写必要的代码，不过度设计
- 最小依赖：不引入不必要的包
- 最小暴露：只导出必要的接口

**TypeScript:**

```typescript
// ❌ 错误：过度设计
interface IUserRepository { ... }
class UserRepositoryImpl implements IUserRepository { ... }
class UserRepositoryFactory { ... }

// ✅ 正确：够用就好
export const userRepository = { ... }
```

**Python:**

```python
# ❌ 错误：过度设计
class IUserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> User: ...

class UserRepositoryImpl(IUserRepository):
    async def find_by_id(self, id: str) -> User: ...

class UserRepositoryFactory:
    @staticmethod
    def create() -> IUserRepository: ...

# ✅ 正确：够用就好
class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_id(self, id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()
```

### 3. 开闭原则 (OCP)

对扩展开放，对修改关闭。

**TypeScript:**

```typescript
// ❌ 错误：每次新增类型都要改代码
function getPrice(type: string) {
  if (type === "flight") return flightPrice;
  if (type === "hotel") return hotelPrice;
}

// ✅ 正确：通过配置/注册扩展
const priceHandlers: Record<string, PriceHandler> = {};
function registerHandler(type: string, handler: PriceHandler) {
  priceHandlers[type] = handler;
}
```

**Python:**

```python
# ❌ 错误：每次新增类型都要改代码
def get_price(type: str) -> float:
    if type == "flight":
        return flight_price
    if type == "hotel":
        return hotel_price

# ✅ 正确：通过配置/注册扩展
price_handlers: dict[str, Callable[[], float]] = {}

def register_handler(type: str, handler: Callable[[], float]) -> None:
    price_handlers[type] = handler

def get_price(type: str) -> float:
    handler = price_handlers.get(type)
    if handler:
        return handler()
    raise AppError(AppErrorCode.NOT_FOUND, f"Unknown type: {type}")
```

## 代码复用

### 规则：能复用绝不新建

1. 先搜索现有代码是否有类似实现
2. 优先 copy 现有模式，保持一致性
3. 通用逻辑提取到 `common` 模块

**TypeScript:**

```typescript
// ❌ 错误：重复造轮子
// flight/utils.ts
function formatDate(date: Date) { ... }
// hotel/utils.ts
function formatDateTime(date: Date) { ... }

// ✅ 正确：复用 common
import { formatDate } from "@/common/utils";
```

**Python:**

```python
# ❌ 错误：重复造轮子
# flight/utils.py
def format_date(date: datetime) -> str: ...
# hotel/utils.py
def format_datetime(date: datetime) -> str: ...

# ✅ 正确：复用 common
from src.common.utils import format_date
```

## 日志规范

### 规则：禁止手动记录日志

日志由 AOP 中间件统一处理，业务代码不应包含日志语句。

**TypeScript:**

```typescript
// ❌ 错误：手动记录日志
async function createFlight(data: FlightDto) {
  console.log("Creating flight:", data);
  logger.info("Flight creation started");
  const result = await flightRepository.create(data);
  return result;
}

// ✅ 正确：纯业务逻辑，日志由中间件处理
async function createFlight(data: FlightDto) {
  return flightRepository.create(data);
}
```

**Python:**

```python
# ❌ 错误：手动记录日志
async def create_flight(data: FlightDto) -> Flight:
    print(f"Creating flight: {data}")
    logger.info("Flight creation started")
    result = await flight_repository.create(data)
    logger.info(f"Flight created: {result.id}")
    return result

# ✅ 正确：纯业务逻辑，日志由中间件处理
async def create_flight(data: FlightDto) -> Flight:
    return await flight_repository.create(data)
```

日志切面已覆盖：

- 请求入口/出口 (`RequestLoggerMiddleware`)
- 数据库操作 (SQLAlchemy echo)
- 异常捕获 (`app_error_handler`)

## 异常处理

### 规则：所有异常向上抛，禁止吞掉

业务层不捕获异常，统一由顶层中间件处理。

**TypeScript:**

```typescript
// ❌ 错误：吞掉异常
async function findUser(id: string) {
  try {
    return await userRepository.findById(id);
  } catch (error) {
    console.error("Error:", error);
    return null; // 吞掉了异常
  }
}

// ✅ 正确：直接抛出，不捕获
async function findUser(id: string) {
  const user = await userRepository.findById(id);
  if (!user) {
    throw new AppError("NOT_FOUND", `User ${id} not found`);
  }
  return user;
}
```

**Python:**

```python
# ❌ 错误：吞掉异常
async def find_user(id: str) -> User | None:
    try:
        return await user_repository.find_by_id(id)
    except Exception as e:
        print(f"Error: {e}")
        return None  # 吞掉了异常

# ❌ 错误：捕获后重新包装但丢失信息
async def find_user(id: str) -> User:
    try:
        return await user_repository.find_by_id(id)
    except Exception:
        raise AppError(AppErrorCode.INTERNAL_ERROR, "查询失败")  # 丢失原始错误

# ✅ 正确：直接抛出，不捕获
async def find_user(id: str) -> User:
    user = await user_repository.find_by_id(id)
    if not user:
        raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")
    return user

# ✅ 正确：需要转换时保留原始信息
async def call_external_api() -> dict:
    try:
        return await external_service.call()
    except Exception as e:
        raise AppError(
            AppErrorCode.EXTERNAL_SERVICE_ERROR,
            "External API failed",
            details={"cause": str(e)},
        ) from e
```

异常处理层级：

```
Repository → 直接抛出数据库异常
Service    → 抛出业务异常 (AppError)
Router     → 不捕获，由异常处理器传递
Middleware → app_error_handler 统一处理
```

## 分层架构

### 严格分层，禁止跨层调用

```
Router → Service → Database
  ↓         ↓         ↓
验证     业务逻辑   数据访问
```

**TypeScript:**

```typescript
// ❌ 错误：Controller 直接访问数据库
router.get("/:id", async (req, res) => {
  const data = await prisma.flight.findUnique({ where: { id: req.params.id } });
  res.json(data);
});

// ✅ 正确：通过 Service 层
router.get(
  "/:id",
  asyncHandler(async (req, res) => {
    const data = await flightService.findById(req.params.id);
    res.json({ success: true, data });
  })
);
```

**Python:**

```python
# ❌ 错误：Router 直接访问数据库
@router.get("/{id}")
async def get_flight(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flight).where(Flight.id == id))
    return result.scalar_one_or_none()

# ✅ 正确：通过 Service 层
@router.get("/{id}")
async def get_flight(id: str, db: AsyncSession = Depends(get_db)):
    service = FlightService(db)
    data = await service.find_by_id(id)
    if not data:
        raise AppError(AppErrorCode.NOT_FOUND, "Flight not found")
    return success_response(data.__dict__)
```

## 模块化

### 每个模块独立完整

**TypeScript:**

```
modules/{module}/
├── controller.ts    # 路由处理
├── service.ts       # 业务逻辑
├── types.ts         # 类型定义
└── index.ts         # 统一导出
```

**Python:**

```
modules/{module}/
├── router.py        # 路由处理
├── service.py       # 业务逻辑
├── dto.py           # 数据传输对象
└── __init__.py      # 统一导出
```

## 命名规范

### 变量命名

**TypeScript:**

```typescript
// 布尔值：is/has/can/should 前缀
const isLoading = true;
const hasPermission = false;

// 数组：复数形式
const users: User[] = [];

// 常量：UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
```

**Python:**

```python
# 变量和函数：snake_case
flight_list = []
def search_flights(): ...

# 常量：UPPER_SNAKE_CASE
MAX_SEARCH_RESULTS = 100

# 类：PascalCase
class FlightService: ...

# 布尔变量：is_, has_, can_, should_ 前缀
is_loading = True
has_error = False
```

### 函数命名

**TypeScript:**

```typescript
// 获取：get/fetch/find
function getUserById(id: string) {}
// 创建：create/add
function createUser(data: UserDto) {}
// 更新：update/set
function updateUser(id: string, data: UpdateUserDto) {}
// 删除：delete/remove
function deleteUser(id: string) {}
```

**Python:**

```python
# 获取：get_, fetch_, find_
def get_flight_by_id(id: str): ...
async def find_user(id: str): ...

# 创建：create_
async def create_user(data: UserDto): ...

# 更新：update_, set_
async def update_user(id: str, data: UpdateUserDto): ...

# 删除：delete_, remove_
async def delete_user(id: str): ...

# 校验：is_, has_, can_, validate_
def is_valid_email(email: str) -> bool: ...
def validate_token(token: str): ...
```

## 类型安全

### TypeScript：严格类型，禁止 any

```typescript
// ❌ 错误
function process(data: any) { ... }

// ✅ 正确
function process(data: ProcessDto) { ... }

// 确实不知道类型时用 unknown
function handleUnknown(data: unknown) {
  if (isUser(data)) { ... }
}
```

### Python：使用类型注解

```python
# ❌ 错误：无类型注解
def process(data):
    return data["name"]

# ✅ 正确：完整类型注解
def process(data: ProcessDto) -> str:
    return data.name

# 可选类型
def find_user(id: str) -> User | None:
    ...

# 泛型
T = TypeVar("T")
def get_first(items: list[T]) -> T | None:
    return items[0] if items else None
```

## 异步处理

### TypeScript：async/await 优于 Promise 链

```typescript
// ❌ 错误：Promise 链
function fetchData() {
  return fetch(url)
    .then((res) => res.json())
    .then((data) => process(data));
}

// ✅ 正确：async/await
async function fetchData() {
  const res = await fetch(url);
  const data = await res.json();
  return process(data);
}
```

### Python：使用 async/await

```python
# ❌ 错误：同步阻塞
def fetch_data() -> dict:
    response = requests.get(url)
    return response.json()

# ✅ 正确：异步
async def fetch_data() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# 并行执行
async def fetch_all() -> tuple[User, list[Order]]:
    user, orders = await asyncio.gather(
        get_user(id),
        get_orders(id),
    )
    return user, orders
```

## 注释规范

### 规则：代码自解释，注释说明 Why

**TypeScript:**

```typescript
// ❌ 错误：注释说明 What
// 获取用户
const user = await getUser(id);

// ✅ 正确：注释说明 Why
// 免费用户每日限制 10 次查询
if (user.plan === "free" && user.dailyQueries >= 10) {
  throw new AppError("FORBIDDEN", "Daily limit exceeded");
}
```

**Python:**

```python
# ❌ 错误：注释说明 What
# 获取用户
user = await get_user(id)

# ✅ 正确：注释说明 Why
# 免费用户每日限制 10 次查询
if user.plan == "free" and user.daily_queries >= 10:
    raise AppError(AppErrorCode.FORBIDDEN, "Daily limit exceeded")
```

## 检查清单

新增代码前确认：

- [ ] 是否已有类似实现可复用？
- [ ] 是否遵循单一职责？
- [ ] 是否放在正确的层级？
- [ ] 是否需要手动日志？（答案应为否）
- [ ] 是否引入不必要的依赖？
- [ ] 异常是否向上抛出？
- [ ] 是否使用了 any 类型（TS）或缺少类型注解（Python）？
- [ ] 命名是否清晰自解释？
