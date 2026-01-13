# Implementation Plan: Frontend Refactor

## Overview

本实现计划将前端代码重构为符合编码规范的分层架构。重构从 Views 开始，逐步向下重构 Components、Hooks、Services。

## Tasks

### Phase 1: Admin Views 重构

- [x] 1. 重构 Admin ConversationsView

  - [x] 1.1 分析 ConversationsView 依赖

    - 检查直接 fetch 调用
    - 检查 className 使用
    - 检查 service 导入
    - _Requirements: 1.1, 2.1_

  - [x] 1.2 创建/更新 useConversations Hook

    - 封装所有 API 调用逻辑
    - 封装筛选状态管理
    - 从 common/types.ts 导入类型
    - _Requirements: 1.3, 5.1_

  - [x] 1.3 创建 AdminConversationFilter 组件

    - 从 View 抽取筛选表单
    - 使用 useConversations hook
    - _Requirements: 2.4_

  - [x] 1.4 创建 AdminConversationTable 组件

    - 从 View 抽取表格渲染
    - 使用 useConversations hook
    - _Requirements: 2.2_

  - [x] 1.5 创建 AdminConversationDetailDialog 组件

    - 从 View 抽取对话详情弹窗
    - 使用 useConversations hook
    - _Requirements: 2.3_

  - [x] 1.6 重构 ConversationsView
    - 移除 fetch 调用和 className
    - 组合新 Components
    - _Requirements: 1.3, 2.1, 2.8_

- [x] 2. 重构 Admin SkillsView

  - [x] 2.1 分析 SkillsView 依赖

    - 检查 skillService 导入
    - 检查 className 使用
    - _Requirements: 1.1, 2.1_

  - [x] 2.2 更新 useSkills Hook

    - 移入 skillService.getList() 调用
    - 移入 skillService.toggle() 调用
    - 添加 getCategoryLabel/getSourceLabel 方法
    - 修复 label_zh/label_en 为 labelZh/labelEn
    - _Requirements: 1.2, 7.3_

  - [x] 2.3 创建 AdminSkillsHeader 组件

    - 从 View 抽取头部和同步按钮
    - _Requirements: 2.1_

  - [x] 2.4 创建 AdminSkillsStats 组件

    - 从 View 抽取统计卡片区域
    - _Requirements: 2.1_

  - [x] 2.5 创建 AdminSkillsFilter 组件

    - 从 View 抽取筛选区域
    - _Requirements: 2.1_

  - [x] 2.6 创建 AdminSkillsList 组件

    - 从 View 抽取技能列表
    - _Requirements: 2.1_

  - [x] 2.7 重构 SkillsView
    - 移除 skillService 导入
    - 移除 className
    - 组合新 Components
    - _Requirements: 1.2, 2.1, 2.8_

- [x] 3. 重构 Admin PromptsView

  - [x] 3.1 分析 PromptsView 依赖

    - 检查 usePrompts 返回值不匹配问题
    - _Requirements: 3.1_

  - [x] 3.2 更新 usePrompts Hook

    - 添加 stats, categoryLabels, sourceLabels 状态
    - 添加 hasMore, total, loadMoreRef
    - 添加 search, category, source 状态
    - 添加 getCategoryLabel, getSourceLabel 方法
    - 添加 handleToggle, handleSync, handleReset 方法
    - 添加 isSyncing 状态
    - 修改签名接受 lang 参数
    - _Requirements: 3.1, 7.1_

  - [x] 3.3 创建 AdminPromptsHeader 组件

    - 从 View 抽取头部
    - _Requirements: 2.1_

  - [x] 3.4 创建 AdminPromptsStats 组件

    - 从 View 抽取统计区域
    - _Requirements: 2.1_

  - [x] 3.5 创建 AdminPromptsFilter 组件

    - 从 View 抽取筛选区域
    - _Requirements: 2.1_

  - [x] 3.6 创建 AdminPromptsList 组件

    - 从 View 抽取提示词列表
    - _Requirements: 2.1_

  - [x] 3.7 重构 PromptsView
    - 更新 usePrompts 调用
    - 移除 className
    - 组合新 Components
    - _Requirements: 3.1, 2.1, 2.8_

- [x] 4. 重构 Admin UsersView

  - [x] 4.1 分析 UsersView 依赖

    - _Requirements: 1.1, 2.1_

  - [x] 4.2 更新/创建 useUsers Hook

    - 封装用户列表和操作
    - _Requirements: 1.1_

  - [x] 4.3 创建 AdminUsersHeader 组件

    - _Requirements: 2.1_

  - [x] 4.4 创建 AdminUsersFilter 组件

    - _Requirements: 2.1_

  - [x] 4.5 创建 AdminUsersTable 组件

    - _Requirements: 2.1_

  - [x] 4.6 重构 UsersView
    - _Requirements: 1.1, 2.1, 2.8_

- [x] 5. 重构 Admin LLMView

  - [x] 5.1 分析 LLMView 依赖

    - _Requirements: 1.1, 2.1_

  - [x] 5.2 更新/创建 useLLM Hook

    - _Requirements: 1.1_

  - [x] 5.3 创建 AdminLLMHeader 组件

    - _Requirements: 2.1_

  - [x] 5.4 创建 AdminLLMStats 组件

    - _Requirements: 2.1_

  - [x] 5.5 创建 AdminLLMFilter 组件

    - _Requirements: 2.1_

  - [x] 5.6 创建 AdminLLMTable 组件

    - _Requirements: 2.1_

  - [x] 5.7 创建 AdminLLMFormDialog 组件

    - _Requirements: 2.1_

  - [x] 5.8 重构 LLMView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 6. 重构 Admin RetrievalView

  - [ ] 6.1 分析 RetrievalView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 6.2 更新 useRetrieval Hook

    - _Requirements: 1.1, 5.4_

  - [ ] 6.3 创建 AdminRetrievalHeader 组件

    - _Requirements: 2.1_

  - [ ] 6.4 创建 AdminRetrievalList 组件

    - _Requirements: 2.1_

  - [ ] 6.5 创建 AdminRetrievalTestPanel 组件

    - _Requirements: 2.1_

  - [ ] 6.6 重构 RetrievalView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 7. 重构 Admin DataSourcesView

  - [ ] 7.1 分析 DataSourcesView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 7.2 更新 useDataSources Hook

    - _Requirements: 1.1_

  - [ ] 7.3 创建 AdminDataSourcesHeader 组件

    - _Requirements: 2.1_

  - [ ] 7.4 创建 AdminDataSourcesStats 组件

    - _Requirements: 2.1_

  - [ ] 7.5 创建 AdminDataSourcesFilter 组件

    - _Requirements: 2.1_

  - [ ] 7.6 创建 AdminDataSourcesList 组件

    - _Requirements: 2.1_

  - [ ] 7.7 重构 DataSourcesView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 8. 重构 Admin SchedulerView

  - [ ] 8.1 分析 SchedulerView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 8.2 更新 useScheduler Hook

    - _Requirements: 1.1_

  - [ ] 8.3 创建 AdminSchedulerHeader 组件

    - _Requirements: 2.1_

  - [ ] 8.4 创建 AdminSchedulerTable 组件

    - _Requirements: 2.1_

  - [ ] 8.5 创建 AdminSchedulerFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 8.6 重构 SchedulerView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 9. 重构 Admin DomainsView

  - [ ] 9.1 分析 DomainsView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 9.2 更新 useDomains Hook (Admin)

    - _Requirements: 1.1_

  - [ ] 9.3 创建 AdminDomainsHeader 组件

    - _Requirements: 2.1_

  - [ ] 9.4 创建 AdminDomainsList 组件

    - _Requirements: 2.1_

  - [ ] 9.5 创建 AdminDomainFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 9.6 重构 DomainsView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 10. 重构 Admin QuestionsView

  - [ ] 10.1 分析 QuestionsView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 10.2 更新 useQuestions Hook

    - _Requirements: 1.1_

  - [ ] 10.3 创建 AdminQuestionsHeader 组件

    - _Requirements: 2.1_

  - [ ] 10.4 创建 AdminQuestionsList 组件

    - _Requirements: 2.1_

  - [ ] 10.5 创建 AdminQuestionFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 10.6 重构 QuestionsView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 11. 重构 Admin RecommendationsView

  - [ ] 11.1 分析 RecommendationsView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 11.2 更新 useRecommendations Hook

    - _Requirements: 1.1_

  - [ ] 11.3 创建 AdminRecommendationsHeader 组件

    - _Requirements: 2.1_

  - [ ] 11.4 创建 AdminRecommendationsTable 组件

    - _Requirements: 2.1_

  - [ ] 11.5 创建 AdminRecommendationEditDialog 组件

    - _Requirements: 2.1_

  - [ ] 11.6 重构 RecommendationsView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 12. 重构 Admin SubscriptionsView

  - [ ] 12.1 分析 SubscriptionsView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 12.2 更新 useSubscriptions Hook

    - _Requirements: 1.1_

  - [ ] 12.3 创建 AdminSubscriptionsHeader 组件

    - _Requirements: 2.1_

  - [ ] 12.4 创建 AdminSubscriptionsTable 组件

    - _Requirements: 2.1_

  - [ ] 12.5 创建 AdminSubscriptionFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 12.6 重构 SubscriptionsView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 13. 重构 Admin CrawlersView

  - [ ] 13.1 分析 CrawlersView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 13.2 更新 useCrawlers Hook

    - _Requirements: 1.1_

  - [ ] 13.3 创建 AdminCrawlersHeader 组件

    - _Requirements: 2.1_

  - [ ] 13.4 创建 AdminCrawlersTable 组件

    - _Requirements: 2.1_

  - [ ] 13.5 创建 AdminCrawlerFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 13.6 重构 CrawlersView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 14. 重构 Admin ConfigView

  - [ ] 14.1 分析 ConfigView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 14.2 更新 useConfigs Hook

    - _Requirements: 1.1_

  - [ ] 14.3 创建 AdminConfigHeader 组件

    - _Requirements: 2.1_

  - [ ] 14.4 创建 AdminConfigTable 组件

    - _Requirements: 2.1_

  - [ ] 14.5 创建 AdminConfigFormDialog 组件

    - _Requirements: 2.1_

  - [ ] 14.6 重构 ConfigView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 15. 重构 Admin AnalyticsView

  - [ ] 15.1 分析 AnalyticsView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 15.2 更新 useAnalytics Hook

    - _Requirements: 1.1_

  - [ ] 15.3 创建 AdminAnalyticsHeader 组件

    - _Requirements: 2.1_

  - [ ] 15.4 创建 AdminAnalyticsCharts 组件

    - _Requirements: 2.1_

  - [ ] 15.5 重构 AnalyticsView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 16. 重构 Admin DashboardView

  - [ ] 16.1 分析 DashboardView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 16.2 创建 AdminDashboardStats 组件

    - _Requirements: 2.1_

  - [ ] 16.3 创建 AdminDashboardCharts 组件

    - _Requirements: 2.1_

  - [ ] 16.4 重构 DashboardView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 17. 重构 Admin AgentFrameworksView

  - [ ] 17.1 分析 AgentFrameworksView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 17.2 创建相关 Hook (如需要)

    - _Requirements: 1.1_

  - [ ] 17.3 创建 AdminAgentFrameworksHeader 组件

    - _Requirements: 2.1_

  - [ ] 17.4 创建 AdminAgentFrameworksList 组件

    - _Requirements: 2.1_

  - [ ] 17.5 重构 AgentFrameworksView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 18. 重构 Admin LoginView

  - [ ] 18.1 分析 LoginView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 18.2 创建 AdminLoginForm 组件

    - _Requirements: 2.1_

  - [ ] 18.3 重构 LoginView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 19. Checkpoint - Admin Views 重构完成
  - 运行 `tsc --noEmit` 确保无类型错误
  - 验证所有 Admin View 文件不导入 Services
  - 验证所有 Admin View 文件不包含 className
  - 验证所有 Admin View 文件不直接使用 fetch

### Phase 2: Member Views 重构

- [ ] 20. 重构 Member HomeView

  - [ ] 20.1 分析 HomeView 依赖

    - 检查 domainService 导入
    - 检查 className 使用
    - _Requirements: 1.1, 2.1_

  - [ ] 20.2 创建 useDomains Hook (Member)

    - 封装产品线和分类获取
    - 封装 activeLineId 状态
    - _Requirements: 1.4_

  - [ ] 20.3 创建 MemberHomeHeader 组件

    - 从 View 抽取头部区域
    - _Requirements: 2.5_

  - [ ] 20.4 创建 MemberProductLineSelector 组件

    - 从 View 抽取产品线选择器
    - 使用 useDomains hook
    - _Requirements: 2.6_

  - [ ] 20.5 创建 MemberTopicCategoryGrid 组件

    - 从 View 抽取分类网格
    - 使用 useDomains hook
    - _Requirements: 2.7_

  - [ ] 20.6 重构 HomeView
    - 移除 domainService 导入
    - 移除 className
    - 组合新 Components
    - _Requirements: 1.4, 2.1, 2.8_

- [ ] 21. 重构 Member ConversationView

  - [ ] 21.1 分析 ConversationView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 21.2 创建 useConversation Hook (Member)

    - 封装对话状态和消息发送
    - _Requirements: 1.1_

  - [ ] 21.3 创建 MemberConversationHeader 组件

    - _Requirements: 2.1_

  - [ ] 21.4 创建 MemberConversationMessages 组件

    - _Requirements: 2.1_

  - [ ] 21.5 创建 MemberConversationInput 组件

    - _Requirements: 2.1_

  - [ ] 21.6 重构 ConversationView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 22. 重构 Member LearningDashboard

  - [ ] 22.1 分析 LearningDashboard 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 22.2 更新 useLearning Hook

    - _Requirements: 1.1_

  - [ ] 22.3 创建 MemberLearningHeader 组件

    - _Requirements: 2.1_

  - [ ] 22.4 创建 MemberLearningCourseList 组件

    - _Requirements: 2.1_

  - [ ] 22.5 创建 MemberLearningLabList 组件

    - _Requirements: 2.1_

  - [ ] 22.6 重构 LearningDashboard
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 23. 重构 Member AuthView

  - [ ] 23.1 分析 AuthView 依赖

    - _Requirements: 1.1, 2.1_

  - [ ] 23.2 创建 MemberLoginForm 组件

    - _Requirements: 2.1_

  - [ ] 23.3 创建 MemberRegisterForm 组件

    - _Requirements: 2.1_

  - [ ] 23.4 重构 AuthView
    - _Requirements: 1.1, 2.1, 2.8_

- [ ] 24. Checkpoint - Member Views 重构完成
  - 运行 `tsc --noEmit` 确保无类型错误
  - 验证所有 Member View 文件不导入 Services
  - 验证所有 Member View 文件不包含 className
  - 验证所有 Member View 文件不直接使用 fetch

### Phase 3: Hooks 类型迁移

- [ ] 25. 迁移 Admin Hooks 中的 interface 定义

  - [ ] 25.1 迁移 useSkills 中的 UseSkillsOptions

    - _Requirements: 5.2_

  - [ ] 25.2 迁移 usePrompts 中的 UsePromptsOptions

    - _Requirements: 5.3_

  - [ ] 25.3 迁移 useRetrieval 中的 UseRetrievalOptions

    - _Requirements: 5.4_

  - [ ] 25.4 迁移其他 Hooks 中的 interface 定义
    - _Requirements: 5.1_

- [ ] 26. 迁移 Member Hooks 中的 interface 定义

  - [ ] 26.1 检查并迁移 useAuth 中的 interface

    - _Requirements: 5.1_

  - [ ] 26.2 检查并迁移 useLearning 中的 interface
    - _Requirements: 5.1_

- [ ] 27. Checkpoint - Hooks 类型迁移完成
  - 运行 `tsc --noEmit` 确保无类型错误
  - 验证所有 Hook 文件不包含 interface 定义

### Phase 4: Services 类型检查

- [ ] 28. 检查 Admin Services 类型导出

  - [ ] 28.1 检查所有 Admin service 文件
    - 确保无 interface/type 导出
    - _Requirements: 4.1, 4.3_

- [ ] 29. 检查 Member Services 类型导出

  - [ ] 29.1 检查 domain.service.ts

    - 确保 TopicCategory/ProductLine 从 common/types.ts 导入
    - _Requirements: 4.2_

  - [ ] 29.2 检查其他 Member service 文件
    - _Requirements: 4.1, 4.3_

- [ ] 30. Checkpoint - Services 类型检查完成
  - 验证所有 Service 文件不导出 interface/type

### Phase 5: Components 检查

- [ ] 31. 检查 Admin Components

  - [ ] 31.1 检查所有 Admin component 文件
    - 确保不导入 services
    - 确保不直接使用 fetch
    - _Requirements: 6.2_

- [ ] 32. 检查 Member Components

  - [ ] 32.1 检查所有 Member component 文件
    - 确保不导入 services
    - 确保不直接使用 fetch
    - _Requirements: 6.2_

- [ ] 33. Checkpoint - Components 检查完成
  - 验证所有 Component 文件不导入 Services
  - 验证所有 Component 文件不直接使用 fetch

### Phase 6: 最终验证

- [ ] 34. TypeScript 编译验证

  - 运行 `tsc --noEmit` 确保无类型错误
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 35. 功能回归测试
  - 手动验证所有 Admin 页面功能正常
  - 手动验证所有 Member 页面功能正常
  - _Requirements: 8.1, 8.2, 8.3_

## Notes

- 重构顺序：View → Components → Hooks → Services
- 每个 View 重构时，先分析依赖，再创建/更新 Hook，然后抽取 Components，最后重构 View
- 每个 Phase 完成后进行 Checkpoint 验证
- 如遇问题可回滚到上一个 Checkpoint
