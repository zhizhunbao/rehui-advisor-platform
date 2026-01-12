# 实现计划: 管理员模块

## 概述

基于现有代码基础设施补全管理员模块功能。优先实现核心功能，测试任务标记为可选。

## 任务列表

- [x] 1. 数据库模型和迁移

  - [x] 1.1 创建 SubscriptionPlan 模型
  - [x] 1.2 创建 SystemConfig 模型
  - [x] 1.3 创建数据库迁移文件
  - [x] 1.4 创建种子数据脚本

- [x] 2. 检查点 - 数据库准备完成

- [x] 3. 后端抓取源管理 API (补全)

  - [x] 3.1 实现 CrawlerService
  - [x] 3.2 实现 CrawlerRouter
  - [ ]\* 3.3 编写抓取源 CRUD 属性测试

- [x] 4. 后端用户管理 API

  - [x] 4.1 实现 UserAdminService
  - [x] 4.2 实现 UserAdminRouter
  - [ ]\* 4.3 编写用户状态管理属性测试

- [x] 5. 后端订阅方案管理 API

  - [x] 5.1 实现 SubscriptionService
  - [x] 5.2 实现 SubscriptionRouter
  - [ ]\* 5.3 编写订阅方案 CRUD 属性测试

- [x] 6. 后端推荐方案管理 API

  - [x] 6.1 实现 RecommendationAdminService
  - [x] 6.2 实现 RecommendationAdminRouter

- [x] 7. 后端对话记录管理 API

  - [x] 7.1 实现 ConversationAdminService
  - [x] 7.2 实现 ConversationAdminRouter

- [x] 8. 后端系统配置管理 API

  - [x] 8.1 实现 ConfigService
  - [x] 8.2 实现 ConfigRouter
  - [ ]\* 8.3 编写系统配置权限属性测试

- [x] 9. 检查点 - 后端 API 完成

- [x] 10. 前端管理员认证

  - [x] 10.1 创建管理员认证 Context (AdminAuthContext.tsx)
  - [x] 10.2 创建管理员登录页面 (LoginView.tsx)
  - [x] 10.3 创建管理员路由保护组件 (AdminRoute.tsx)
  - [ ]\* 10.4 编写登录错误信息一致性属性测试

- [x] 11. 前端管理员布局

  - [x] 11.1 创建管理员布局组件 (AdminLayout.tsx)
  - [x] 11.2 更新管理员侧边栏导航

- [x] 12. 前端用户管理页面

  - [x] 12.1 创建用户管理 Service 和 Hook (user.service.ts, useUsers.ts)
  - [x] 12.2 创建用户管理视图 (UsersView.tsx)

- [x] 13. 前端对话记录页面

  - [x] 13.1 创建对话管理 Service 和 Hook (conversation.service.ts, useConversations.ts)
  - [x] 13.2 创建对话记录视图 (ConversationsView.tsx)

- [x] 14. 前端订阅方案页面

  - [x] 14.1 创建订阅方案 Service 和 Hook (subscription.service.ts, useSubscriptions.ts)
  - [x] 14.2 创建订阅方案视图 (SubscriptionsView.tsx)

- [x] 15. 前端推荐方案页面

  - [x] 15.1 创建推荐方案 Service 和 Hook (recommendation.service.ts, useRecommendations.ts)
  - [x] 15.2 创建推荐方案视图 (RecommendationsView.tsx)

- [x] 16. 前端系统配置页面

  - [x] 16.1 创建系统配置 Service 和 Hook (config.service.ts, useConfigs.ts)
  - [x] 16.2 创建系统配置视图 (ConfigView.tsx)

- [x] 17. 更新前端类型定义和国际化

  - [x] 17.1 更新 admin.types.ts (添加 AdminUser, AdminConversation, SubscriptionPlan, SystemConfig 等类型)
  - [x] 17.2 更新 adminLocales (添加新页面的中英文翻译)

- [x] 18. 检查点 - 前端页面完成

- [x] 19. 路由集成

  - [x] 19.1 更新前端路由配置 (创建 AdminApp.tsx, admin.tsx, admin.html)
  - [x] 19.2 注册后端路由 (已在 main.py 注册)

- [x] 20. 最终检查点
  - 管理员模块功能完成

## 备注

- 标记 `*` 的任务为可选的属性测试任务（未实现）
- 所有后端服务使用 Supabase API，禁止使用 SQLAlchemy + AsyncSession
- 前端使用独立的 admin.html 入口，通过 /admin 路径访问
- 管理员后台支持中英文切换
