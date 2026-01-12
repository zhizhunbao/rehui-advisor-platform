# 设计文档

## 概述

用户认证系统基于现有的 FastAPI + SQLAlchemy 架构，使用 JWT 进行无状态认证。系统支持匿名用户、邮箱注册用户和 OAuth 用户三种身份类型，并与 Freemium 配额系统集成。

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │ Login   │  │Register │  │ OAuth   │  │ Token Manager   │ │
│  │ Form    │  │ Form    │  │ Buttons │  │ (Auto Refresh)  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘ │
└───────┼────────────┼────────────┼────────────────┼──────────┘
        │            │            │                │
        ▼            ▼            ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Auth Middleware                          │   │
│  │  - JWT Validation                                     │   │
│  │  - Rate Limiting                                      │   │
│  │  - Session Token Support                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Auth Module                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Router    │  │   Service   │  │   OAuth Service     │  │
│  │             │  │             │  │                     │  │
│  │ /register   │  │ - register  │  │ - google_callback   │  │
│  │ /login      │  │ - login     │  │ - github_callback   │  │
│  │ /logout     │  │ - logout    │  │ - link_account      │  │
│  │ /refresh    │  │ - refresh   │  │                     │  │
│  │ /oauth/*    │  │ - reset_pwd │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    User     │  │RefreshToken │  │   PasswordReset     │  │
│  │   Model     │  │   Model     │  │      Model          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 组件和接口

### 后端组件

#### 1. AuthService (扩展现有)

```python
class AuthService:
    # 现有方法
    async def register(email: str, password: str, name: str) -> User
    async def login(email: str, password: str) -> User
    def create_access_token(user_id: str, user_type: str) -> str
    def create_refresh_token(user_id: str) -> str

    # 新增方法
    async def send_verification_email(user: User) -> None
    async def verify_email(token: str) -> User
    async def request_password_reset(email: str) -> None
    async def reset_password(token: str, new_password: str) -> User
    async def logout(user_id: str, refresh_token: str) -> None
    async def logout_all_devices(user_id: str) -> None
    async def record_login_attempt(email: str, ip: str, success: bool) -> None
    async def check_login_lockout(email: str, ip: str) -> bool
```

#### 2. OAuthService (新增)

```python
class OAuthService:
    async def get_google_auth_url() -> str
    async def google_callback(code: str) -> User
    async def get_github_auth_url() -> str
    async def github_callback(code: str) -> User
    async def link_oauth_account(user: User, provider: str, provider_id: str) -> None
```

#### 3. EmailService (新增)

```python
class EmailService:
    async def send_verification_email(email: str, token: str) -> None
    async def send_password_reset_email(email: str, token: str) -> None
    async def send_security_alert(email: str, event: str, details: dict) -> None
```

### 数据模型

#### RefreshToken (新增)

```python
class RefreshToken(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String)  # 存储 hash 而非明文
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    device_info: Mapped[str | None] = mapped_column(String, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
```

#### PasswordResetToken (新增)

```python
class PasswordResetToken(Base, UUIDMixin):
    __tablename__ = "password_reset_tokens"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
```

#### LoginAttempt (新增)

```python
class LoginAttempt(Base, UUIDMixin):
    __tablename__ = "login_attempts"

    email: Mapped[str] = mapped_column(String, index=True)
    ip_address: Mapped[str] = mapped_column(String, index=True)
    success: Mapped[bool] = mapped_column(Boolean)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
```

#### User (扩展现有)

```python
# 新增字段
email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
oauth_provider: Mapped[str | None] = mapped_column(String, nullable=True)  # google, github
oauth_provider_id: Mapped[str | None] = mapped_column(String, nullable=True)
last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
last_login_ip: Mapped[str | None] = mapped_column(String, nullable=True)
account_locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
deletion_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

### API 端点

```
POST   /api/auth/register              # 邮箱注册
POST   /api/auth/login                 # 邮箱登录
POST   /api/auth/logout                # 登出当前设备
POST   /api/auth/logout-all            # 登出所有设备
POST   /api/auth/refresh               # 刷新令牌
POST   /api/auth/verify-email          # 验证邮箱
POST   /api/auth/resend-verification   # 重发验证邮件
POST   /api/auth/forgot-password       # 请求密码重置
POST   /api/auth/reset-password        # 重置密码
GET    /api/auth/me                    # 获取当前用户
PUT    /api/auth/me                    # 更新用户资料
PUT    /api/auth/password              # 修改密码
DELETE /api/auth/me                    # 请求删除账户
POST   /api/auth/cancel-deletion       # 取消删除请求

GET    /api/auth/oauth/google          # Google OAuth 跳转
GET    /api/auth/oauth/google/callback # Google OAuth 回调
GET    /api/auth/oauth/github          # GitHub OAuth 跳转
GET    /api/auth/oauth/github/callback # GitHub OAuth 回调
```

### 前端组件

```
src/modules/auth/
├── components/
│   ├── LoginForm.tsx           # 登录表单
│   ├── RegisterForm.tsx        # 注册表单
│   ├── ForgotPasswordForm.tsx  # 忘记密码表单
│   ├── ResetPasswordForm.tsx   # 重置密码表单
│   ├── OAuthButtons.tsx        # OAuth 登录按钮
│   └── ProfileForm.tsx         # 用户资料表单
├── hooks/
│   ├── useAuth.ts              # 认证状态管理
│   └── useTokenRefresh.ts      # 令牌自动刷新
├── services/
│   └── auth.service.ts         # API 调用
├── types/
│   └── auth.types.ts           # 类型定义
└── locales/
    └── index.ts                # 国际化文本
```

## 正确性属性

_正确性属性是系统必须满足的形式化规则，用于验证实现的正确性。每个属性都是一个可测试的断言，应该对所有有效输入都成立。_

### Property 1: 密码哈希不可逆

_对于任意_ 密码字符串，存储的 password_hash 不应能还原出原始密码，且相同密码的两次哈希结果应不同（bcrypt salt）

**Validates: Requirements 1.5**

### Property 2: 令牌过期时间正确

_对于任意_ 生成的 Access_Token，其过期时间应在生成时间后 15 分钟内；_对于任意_ Refresh_Token，其过期时间应在生成时间后 7 天内

**Validates: Requirements 2.5, 2.6**

### Property 3: 登录错误信息一致性

_对于任意_ 登录请求，无论是邮箱不存在还是密码错误，返回的错误信息应完全相同

**Validates: Requirements 2.2**

### Property 4: 令牌刷新轮换

_对于任意_ 成功的令牌刷新操作，旧的 Refresh_Token 应被标记为已使用，新的 Refresh_Token 应被创建

**Validates: Requirements 4.4**

### Property 5: 密码重置链接一次性

_对于任意_ 密码重置链接，使用后再次使用应返回错误

**Validates: Requirements 6.3**

### Property 6: 登录锁定阈值

_对于任意_ IP 地址，连续 5 次失败登录后，该 IP 应被锁定 15 分钟

**Validates: Requirements 7.1**

### Property 7: 账户删除冷静期

_对于任意_ 账户删除请求，在 7 天内应可撤销，7 天后数据应被永久删除

**Validates: Requirements 9.3, 9.4**

## 错误处理

| 错误场景     | 错误码                 | HTTP 状态 | 用户提示                              |
| ------------ | ---------------------- | --------- | ------------------------------------- |
| 邮箱已注册   | DUPLICATE              | 409       | 该邮箱已被注册                        |
| 密码强度不足 | VALIDATION_ERROR       | 400       | 密码需至少 8 位，包含大小写字母和数字 |
| 登录凭证错误 | UNAUTHORIZED           | 401       | 邮箱或密码错误                        |
| 账户未验证   | FORBIDDEN              | 403       | 请先验证邮箱                          |
| 令牌过期     | UNAUTHORIZED           | 401       | 登录已过期，请重新登录                |
| 账户被锁定   | FORBIDDEN              | 403       | 账户已被锁定，请稍后重试              |
| 重置链接过期 | UNAUTHORIZED           | 401       | 重置链接已过期                        |
| OAuth 失败   | EXTERNAL_SERVICE_ERROR | 502       | 第三方登录失败，请重试                |

## 测试策略

### 单元测试

- 密码哈希和验证
- JWT 生成和解析
- 密码强度验证
- 邮箱格式验证

### 属性测试

- Property 1: 生成随机密码，验证哈希不可逆
- Property 2: 生成令牌，验证过期时间范围
- Property 3: 模拟各种登录失败，验证错误信息一致
- Property 4: 执行令牌刷新，验证旧令牌失效
- Property 5: 使用重置链接两次，验证第二次失败
- Property 6: 模拟连续失败登录，验证锁定触发
- Property 7: 请求删除后验证冷静期和最终删除

### 集成测试

- 完整注册流程（注册 → 验证邮箱 → 登录）
- OAuth 流程（跳转 → 回调 → 创建/关联账户）
- 密码重置流程（请求 → 邮件 → 重置 → 登录）
- 令牌刷新流程（过期 → 刷新 → 继续使用）

### 测试框架

- 后端: pytest + pytest-asyncio + hypothesis (属性测试)
- 前端: vitest + @testing-library/react
