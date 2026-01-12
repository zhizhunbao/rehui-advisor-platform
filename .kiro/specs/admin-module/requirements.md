# 需求文档

## 简介

管理员模块为北美生活决策顾问平台提供后台管理功能，包括管理员认证、领域配置、Prompt 模板管理、问题库管理和数据抓取源管理。基于现有代码基础设施进行补全和完善。

## 术语表

- **Admin_User**: 管理员用户，拥有后台管理权限的用户
- **Super_Admin**: 超级管理员，拥有创建其他管理员权限的用户
- **Domain**: 领域配置，如机票、酒店、工作等咨询类别的配置信息
- **Prompt_Template**: Prompt 模板，用于 AI 对话的系统提示词模板
- **Question**: 问题库，各领域的预设问题
- **Crawl_Source**: 抓取源，数据抓取的来源配置
- **Crawl_Task**: 抓取任务，数据抓取的执行记录
- **Recommendation**: 推荐方案，AI 为用户推荐的各类方案（机票、酒店、保险等）
- **Subscription_Plan**: 订阅方案，用户的付费订阅套餐配置
- **Platform_User**: 平台用户，使用顾问服务的普通用户
- **Conversation**: 对话记录，用户与 AI 的对话历史
- **System_Config**: 系统配置，全局设置和 API 密钥等

## 需求

### 需求 1: 管理员认证

**用户故事:** 作为管理员，我想要安全地登录后台系统，以便管理平台配置

#### 验收标准

1. WHEN 管理员访问后台路径 THEN Admin_System 应当显示登录页面
2. WHEN 管理员提交正确的用户名和密码 THEN Admin_System 应当返回 Access_Token 和 Refresh_Token
3. WHEN 登录凭证错误 THEN Admin_System 应当返回通用错误信息
4. THE Access_Token 有效期应当为 24 小时
5. THE Refresh_Token 有效期应当为 7 天
6. WHEN Access_Token 过期 THEN 前端应当自动使用 Refresh_Token 刷新
7. WHEN 管理员登出 THEN Admin_System 应当清除本地存储的所有令牌

### 需求 2: 管理员路由保护

**用户故事:** 作为系统，我想要保护管理后台路由，以便只有已认证的管理员可以访问

#### 验收标准

1. WHEN 未认证用户访问管理后台 THEN Admin_System 应当重定向到登录页面
2. WHEN 已认证管理员访问管理后台 THEN Admin_System 应当显示管理界面
3. THE Admin_System 应当在页面刷新后保持登录状态
4. WHEN 令牌失效 THEN Admin_System 应当自动跳转到登录页面

### 需求 3: 领域管理

**用户故事:** 作为管理员，我想要管理咨询领域配置，以便控制用户可见的领域选项

#### 验收标准

1. THE Admin_System 应当显示所有领域列表
2. WHEN 管理员创建领域 THEN Admin_System 应当保存领域配置
3. WHEN 管理员编辑领域 THEN Admin_System 应当更新领域配置
4. WHEN 管理员删除领域 THEN Admin_System 应当移除领域配置
5. THE 领域配置应当支持中英文双语
6. THE 领域配置应当包含图标、颜色、排序等属性

### 需求 4: Prompt 模板管理

**用户故事:** 作为管理员，我想要管理 AI 对话的 Prompt 模板，以便优化 AI 响应质量

#### 验收标准

1. THE Admin_System 应当显示所有 Prompt 模板列表
2. WHEN 管理员创建 Prompt THEN Admin_System 应当保存模板
3. WHEN 管理员编辑 Prompt THEN Admin_System 应当更新模板
4. WHEN 管理员删除 Prompt THEN Admin_System 应当移除模板
5. THE Prompt 模板应当支持中英文双语
6. THE Prompt 模板应当支持分类管理

### 需求 5: 问题库管理

**用户故事:** 作为管理员，我想要管理各领域的预设问题，以便引导用户进行咨询

#### 验收标准

1. THE Admin_System 应当显示所有问题列表
2. WHEN 管理员按领域筛选 THEN Admin_System 应当显示该领域的问题
3. WHEN 管理员创建问题 THEN Admin_System 应当保存问题
4. WHEN 管理员删除问题 THEN Admin_System 应当移除问题
5. THE 问题应当支持中英文双语
6. THE 问题应当支持单选、多选、文本三种类型

### 需求 6: 抓取源管理

**用户故事:** 作为管理员，我想要管理数据抓取源，以便获取外部数据

#### 验收标准

1. THE Admin_System 应当显示所有抓取源列表
2. WHEN 管理员创建抓取源 THEN Admin_System 应当保存配置
3. WHEN 管理员编辑抓取源 THEN Admin_System 应当更新配置
4. WHEN 管理员删除抓取源 THEN Admin_System 应当移除配置
5. WHEN 管理员手动触发抓取 THEN Admin_System 应当创建抓取任务
6. THE Admin_System 应当显示抓取任务历史和状态

### 需求 7: 管理员账户管理

**用户故事:** 作为超级管理员，我想要管理其他管理员账户，以便控制后台访问权限

#### 验收标准

1. WHEN Super_Admin 创建管理员 THEN Admin_System 应当创建新管理员账户
2. THE 普通管理员不应当有创建其他管理员的权限
3. WHEN 管理员修改密码 THEN Admin_System 应当验证旧密码后更新
4. THE 密码应当使用 bcrypt 哈希存储

### 需求 8: 推荐方案管理

**用户故事:** 作为管理员，我想要管理 AI 推荐的方案数据，以便审核和优化推荐质量

#### 验收标准

1. THE Admin_System 应当显示所有推荐方案列表
2. WHEN 管理员按领域筛选 THEN Admin_System 应当显示该领域的推荐方案
3. WHEN 管理员按状态筛选 THEN Admin_System 应当显示对应状态的方案
4. WHEN 管理员查看方案详情 THEN Admin_System 应当显示完整方案信息
5. WHEN 管理员编辑方案 THEN Admin_System 应当更新方案内容
6. WHEN 管理员删除方案 THEN Admin_System 应当移除方案
7. THE 推荐方案应当支持启用/禁用状态切换
8. THE 推荐方案应当记录来源和创建时间

### 需求 9: 订阅方案管理

**用户故事:** 作为管理员，我想要管理用户订阅套餐，以便控制不同等级用户的权益

#### 验收标准

1. THE Admin_System 应当显示所有订阅方案列表
2. WHEN 管理员创建订阅方案 THEN Admin_System 应当保存方案配置
3. WHEN 管理员编辑订阅方案 THEN Admin_System 应当更新方案配置
4. WHEN 管理员删除订阅方案 THEN Admin_System 应当移除方案
5. THE 订阅方案应当包含名称、价格、配额限制等属性
6. THE 订阅方案应当支持中英文双语
7. THE 订阅方案应当支持启用/禁用状态
8. THE Admin_System 应当显示各方案的订阅用户数统计

### 需求 10: 用户管理

**用户故事:** 作为管理员，我想要管理平台用户，以便监控用户活动和处理问题

#### 验收标准

1. THE Admin_System 应当显示所有用户列表
2. WHEN 管理员搜索用户 THEN Admin_System 应当按邮箱或 ID 筛选
3. WHEN 管理员查看用户详情 THEN Admin_System 应当显示用户信息和配额使用情况
4. WHEN 管理员禁用用户 THEN Admin_System 应当阻止该用户登录
5. WHEN 管理员启用用户 THEN Admin_System 应当恢复该用户访问权限
6. THE Admin_System 应当显示用户的注册时间和最后活跃时间
7. THE Admin_System 应当显示用户的订阅状态

### 需求 11: 对话记录管理

**用户故事:** 作为管理员，我想要查看用户对话记录，以便审核内容和分析用户需求

#### 验收标准

1. THE Admin_System 应当显示对话记录列表
2. WHEN 管理员按用户筛选 THEN Admin_System 应当显示该用户的对话
3. WHEN 管理员按领域筛选 THEN Admin_System 应当显示该领域的对话
4. WHEN 管理员查看对话详情 THEN Admin_System 应当显示完整对话内容
5. WHEN 管理员删除对话 THEN Admin_System 应当移除对话记录
6. THE Admin_System 应当支持按时间范围筛选对话

### 需求 12: 数据统计分析

**用户故事:** 作为管理员，我想要查看平台数据统计，以便了解运营状况

#### 验收标准

1. THE Admin_System 应当显示用户总数和新增用户趋势
2. THE Admin_System 应当显示对话总数和日活跃对话数
3. THE Admin_System 应当显示各领域的使用占比
4. THE Admin_System 应当显示配额使用统计
5. THE Admin_System 应当显示订阅转化率
6. THE Admin_System 应当支持按时间范围查看统计数据

### 需求 13: 系统配置管理

**用户故事:** 作为超级管理员，我想要管理系统全局配置，以便控制平台行为

#### 验收标准

1. WHEN Super_Admin 访问系统配置 THEN Admin_System 应当显示配置列表
2. THE 普通管理员不应当有访问系统配置的权限
3. WHEN Super_Admin 编辑配置 THEN Admin_System 应当更新配置值
4. THE 系统配置应当包含 AI 模型设置
5. THE 系统配置应当包含配额默认值设置
6. THE 系统配置应当包含功能开关设置

### 需求 14: 数据库迁移

**用户故事:** 作为开发者，我想要确保管理员相关数据表已正确创建

#### 验收标准

1. THE 数据库应当包含 admin_users 表
2. THE 数据库应当包含 domains 表
3. THE 数据库应当包含 prompt_templates 表
4. THE 数据库应当包含 questions 表
5. THE 数据库应当包含 crawl_sources 表
6. THE 数据库应当包含 crawl_tasks 表
7. THE 数据库应当包含 recommendations 表
8. THE 数据库应当包含 subscription_plans 表
9. THE 数据库应当包含 system_configs 表
10. THE 数据库应当有初始超级管理员种子数据
11. THE 数据库应当有默认订阅方案种子数据
12. THE 数据库应当有默认系统配置种子数据
