# 实现计划: 用户认证系统

## 概述

基于现有 FastAPI + SQLAlchemy 架构实现用户认证系统，包括邮箱注册登录、OAuth 第三方登录、令牌管理和账户安全功能。

## 任务列表

- [x] 1. 数据模型和数据库迁移

  - [x] 1.1 扩展 User 模型添加认证相关字段
    - 添加 email_verified, oauth_provider, oauth_provider_id, last_login_at, last_login_ip, account_locked_until, deletion_requested_at 字段
    - _Requirements: 1.6, 1.7, 2.7, 3.3, 7.2, 9.3_
  - [x] 1.2 创建 RefreshToken 模型
    - 包含 user_id, token_hash, expires_at, is_revoked, device_info, ip_address 字段
    - _Requirements: 2.4, 4.4, 5.1_
  - [x] 1.3 创建 PasswordResetToken 模型
    - 包含 user_id, token_hash, expires_at, is_used 字段
    - _Requirements: 6.1, 6.2, 6.3_
  - [x] 1.4 创建 LoginAttempt 模型
    - 包含 email, ip_address, success, attempted_at 字段
    - _Requirements: 7.1, 7.2_
  - [x] 1.5 生成并运行 Alembic 迁移
    - 创建迁移脚本并应用到数据库
    - _Requirements: 1.1-9.5_

- [ ] 2. 核心认证服务

  - [ ] 2.1 实现密码哈希和验证工具
    - 使用 bcrypt 实现 hash_password 和 verify_password 函数
    - _Requirements: 1.5_
  - [ ]\* 2.2 编写密码哈希属性测试
    - **Property 1: 密码哈希不可逆**
    - **Validates: Requirements 1.5**
  - [ ] 2.3 实现密码强度验证
    - 验证最少 8 位，包含大小写字母和数字
    - _Requirements: 1.4_
  - [ ] 2.4 实现 JWT 令牌生成和验证
    - Access_Token 15 分钟过期，Refresh_Token 7 天过期
    - _Requirements: 2.4, 2.5, 2.6_
  - [ ]\* 2.5 编写令牌过期时间属性测试
    - **Property 2: 令牌过期时间正确**
    - **Validates: Requirements 2.5, 2.6**

- [ ] 3. 检查点 - 核心工具完成

  - 确保所有测试通过，如有问题请询问用户

- [ ] 4. 邮箱注册登录功能

  - [ ] 4.1 实现注册服务方法
    - 验证邮箱格式、检查重复、创建用户、发送验证邮件
    - _Requirements: 1.1, 1.2, 1.3, 1.6_
  - [ ] 4.2 实现登录服务方法
    - 验证凭证、检查账户状态、生成令牌、记录登录信息
    - _Requirements: 2.1, 2.2, 2.3, 2.7_
  - [ ]\* 4.3 编写登录错误信息一致性属性测试
    - **Property 3: 登录错误信息一致性**
    - **Validates: Requirements 2.2**
  - [ ] 4.4 实现邮箱验证服务方法
    - 生成验证令牌、验证令牌、激活账户
    - _Requirements: 1.6, 1.7_
  - [ ] 4.5 实现注册和登录 API 路由
    - POST /api/auth/register, POST /api/auth/login
    - _Requirements: 1.1-2.7_

- [ ] 5. 令牌刷新和登出

  - [ ] 5.1 实现令牌刷新服务方法
    - 验证 Refresh_Token、生成新令牌对、实现令牌轮换
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [ ]\* 5.2 编写令牌刷新轮换属性测试
    - **Property 4: 令牌刷新轮换**
    - **Validates: Requirements 4.4**
  - [ ] 5.3 实现登出服务方法
    - 单设备登出和全设备登出
    - _Requirements: 5.1, 5.2_
  - [ ] 5.4 实现令牌刷新和登出 API 路由
    - POST /api/auth/refresh, POST /api/auth/logout, POST /api/auth/logout-all
    - _Requirements: 4.1-5.4_

- [ ] 6. 检查点 - 基础认证完成

  - 确保所有测试通过，如有问题请询问用户

- [ ] 7. 密码重置功能

  - [ ] 7.1 实现密码重置请求服务方法
    - 生成重置令牌、发送重置邮件、防止邮箱枚举
    - _Requirements: 6.1, 6.6_
  - [ ] 7.2 实现密码重置执行服务方法
    - 验证令牌、更新密码、使所有会话失效
    - _Requirements: 6.2, 6.3, 6.4, 6.5_
  - [ ]\* 7.3 编写密码重置链接一次性属性测试
    - **Property 5: 密码重置链接一次性**
    - **Validates: Requirements 6.3**
  - [ ] 7.4 实现密码重置 API 路由
    - POST /api/auth/forgot-password, POST /api/auth/reset-password
    - _Requirements: 6.1-6.6_

- [ ] 8. 账户安全功能

  - [ ] 8.1 实现登录尝试记录和锁定检查
    - 记录登录尝试、检查 IP 锁定、检查账户锁定
    - _Requirements: 7.1, 7.2_
  - [ ]\* 8.2 编写登录锁定阈值属性测试
    - **Property 6: 登录锁定阈值**
    - **Validates: Requirements 7.1**
  - [ ] 8.3 实现速率限制中间件
    - 对认证端点实施速率限制
    - _Requirements: 7.3_
  - [ ] 8.4 集成登录安全检查到登录流程
    - 在登录前检查锁定状态，登录后记录尝试
    - _Requirements: 7.1, 7.2_

- [ ] 9. OAuth 第三方登录

  - [ ] 9.1 实现 Google OAuth 服务
    - 生成授权 URL、处理回调、获取用户信息
    - _Requirements: 3.1, 3.3, 3.4, 3.5_
  - [ ] 9.2 实现 GitHub OAuth 服务
    - 生成授权 URL、处理回调、获取用户信息
    - _Requirements: 3.2, 3.3, 3.4, 3.5_
  - [ ] 9.3 实现 OAuth 账户关联逻辑
    - 新用户创建账户、已有邮箱关联账户
    - _Requirements: 3.3, 3.4_
  - [ ] 9.4 实现 OAuth API 路由
    - GET /api/auth/oauth/google, GET /api/auth/oauth/google/callback
    - GET /api/auth/oauth/github, GET /api/auth/oauth/github/callback
    - _Requirements: 3.1-3.6_

- [ ] 10. 检查点 - 后端认证完成

  - 确保所有测试通过，如有问题请询问用户

- [ ] 11. 用户资料和账户管理

  - [ ] 11.1 实现获取和更新用户资料服务方法
    - 获取当前用户、更新显示名称/头像/语言偏好
    - _Requirements: 8.1, 8.2_
  - [ ] 11.2 实现修改密码服务方法
    - 验证当前密码、更新新密码
    - _Requirements: 8.5_
  - [ ] 11.3 实现修改邮箱服务方法
    - 发送验证邮件到新邮箱、验证后更新
    - _Requirements: 8.3, 8.4_
  - [ ] 11.4 实现账户删除服务方法
    - 请求删除、取消删除、执行删除
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  - [ ]\* 11.5 编写账户删除冷静期属性测试
    - **Property 7: 账户删除冷静期**
    - **Validates: Requirements 9.3, 9.4**
  - [ ] 11.6 实现用户资料和账户管理 API 路由
    - GET/PUT /api/auth/me, PUT /api/auth/password, DELETE /api/auth/me, POST /api/auth/cancel-deletion
    - _Requirements: 8.1-9.5_

- [ ] 12. 邮件服务

  - [ ] 12.1 实现邮件服务基础设施
    - 配置 SMTP 或第三方邮件服务（如 SendGrid）
    - _Requirements: 1.6, 6.1, 7.2_
  - [ ] 12.2 实现验证邮件模板和发送
    - 注册验证邮件、邮箱变更验证邮件
    - _Requirements: 1.6, 8.3_
  - [ ] 12.3 实现密码重置邮件模板和发送
    - 密码重置链接邮件
    - _Requirements: 6.1_
  - [ ] 12.4 实现安全提醒邮件模板和发送
    - 账户锁定通知、异常登录提醒
    - _Requirements: 7.2, 7.4_

- [ ] 13. 检查点 - 后端全部完成

  - 确保所有测试通过，如有问题请询问用户

- [ ] 14. 前端认证组件

  - [ ] 14.1 创建认证模块目录结构和类型定义
    - 创建 src/modules/auth/ 目录结构和 auth.types.ts
    - _Requirements: 1.1-9.5_
  - [ ] 14.2 实现认证 API 服务
    - 创建 auth.service.ts 封装所有认证 API 调用
    - _Requirements: 1.1-9.5_
  - [ ] 14.3 实现 useAuth Hook
    - 管理认证状态、用户信息、登录登出方法
    - _Requirements: 2.1-5.4_
  - [ ] 14.4 实现 useTokenRefresh Hook
    - 自动刷新令牌、处理过期
    - _Requirements: 4.1-4.5_
  - [ ] 14.5 实现登录表单组件
    - 邮箱密码输入、表单验证、错误提示
    - _Requirements: 2.1-2.7_
  - [ ] 14.6 实现注册表单组件
    - 邮箱密码输入、密码强度提示、表单验证
    - _Requirements: 1.1-1.7_
  - [ ] 14.7 实现 OAuth 登录按钮组件
    - Google 和 GitHub 登录按钮
    - _Requirements: 3.1-3.6_
  - [ ] 14.8 实现忘记密码和重置密码表单组件
    - 请求重置表单、设置新密码表单
    - _Requirements: 6.1-6.6_
  - [ ] 14.9 实现用户资料表单组件
    - 显示和编辑用户资料
    - _Requirements: 8.1-8.5_
  - [ ] 14.10 创建认证模块国际化文本
    - 创建 locales/index.ts 包含中英文文本
    - _Requirements: 1.1-9.5_

- [ ] 15. 前端路由和页面集成

  - [ ] 15.1 创建登录页面
    - 集成登录表单和 OAuth 按钮
    - _Requirements: 2.1-3.6_
  - [ ] 15.2 创建注册页面
    - 集成注册表单和 OAuth 按钮
    - _Requirements: 1.1-3.6_
  - [ ] 15.3 创建密码重置页面
    - 集成忘记密码和重置密码表单
    - _Requirements: 6.1-6.6_
  - [ ] 15.4 创建邮箱验证页面
    - 处理验证链接、显示验证结果
    - _Requirements: 1.6, 1.7_
  - [ ] 15.5 创建用户资料页面
    - 集成用户资料表单、账户删除功能
    - _Requirements: 8.1-9.5_
  - [ ] 15.6 配置路由保护
    - 实现认证路由守卫、未登录重定向
    - _Requirements: 2.1-5.4_

- [ ] 16. 最终检查点
  - 确保所有测试通过，前后端集成正常，如有问题请询问用户

## 备注

- 标记 `*` 的任务为可选的属性测试任务
- 每个任务都引用了对应的需求编号以便追溯
- 检查点用于阶段性验证，确保增量开发的稳定性
- 属性测试使用 hypothesis 库实现
