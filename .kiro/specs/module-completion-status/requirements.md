# 模块完成状态评估与下一步计划

## 背景

管理后台包含多个模块，需要评估各模块的完成状态并确定下一步开发优先级。

## 当前模块状态

### ✅ 已完成模块

| 模块              | 后端 | 前端 | 备注                      |
| ----------------- | ---- | ---- | ------------------------- |
| Data Sources      | ✅   | ✅   | 完整的 CRUD + 统计 + 筛选 |
| Retrieval Engines | ✅   | ✅   | 完整的 CRUD + 统计        |
| Domains           | ✅   | ✅   | 领域分类管理              |

### ⚠️ 需要修复的模块

| 模块     | 问题                            | 优先级 |
| -------- | ------------------------------- | ------ |
| Crawlers | 前端调用的 API 端点与后端不匹配 | 高     |

**Crawlers 问题详情：**

- 前端调用 `/admin/crawlers/sources/{id}/run`，后端是 `/admin/crawlers/sources/{id}/trigger`
- 前端 `getTasks` 使用 `sourceId` 参数，后端使用 `source_id`
- 前端缺少分页支持

### ❓ 待评估模块

| 模块            | 后端路径                  | 前端视图                  |
| --------------- | ------------------------- | ------------------------- |
| LLM             | `modules/llm/`            | `LLMView.tsx`             |
| Prompts         | `modules/prompt/`         | `PromptsView.tsx`         |
| Skills          | `modules/skill/`          | `SkillsView.tsx`          |
| Questions       | `modules/admin/`          | `QuestionsView.tsx`       |
| Recommendations | `modules/recommendation/` | `RecommendationsView.tsx` |
| Users           | `modules/admin/`          | `UsersView.tsx`           |
| Conversations   | -                         | `ConversationsView.tsx`   |
| Subscriptions   | `modules/admin/`          | `SubscriptionsView.tsx`   |
| Analytics       | -                         | `AnalyticsView.tsx`       |
| Config          | -                         | `ConfigView.tsx`          |

## 用户故事

### US-1: 修复 Crawlers 模块 API 对接

**作为** 管理员
**我想要** 能够正常使用数据抓取功能
**以便于** 管理抓取源和查看任务历史

**验收标准：**

- [ ] 前端 API 调用与后端端点匹配
- [ ] 能够查看抓取源列表
- [ ] 能够触发抓取任务
- [ ] 能够查看任务历史（支持分页）
- [ ] 能够添加/编辑/删除抓取源

### US-2: 评估并完善 AI 核心模块

**作为** 管理员
**我想要** 完整的 LLM、Prompts、Skills 管理功能
**以便于** 配置 AI 系统的核心组件

**验收标准：**

- [ ] LLM 模块：查看/配置 LLM 模型
- [ ] Prompts 模块：CRUD 操作 + 版本管理
- [ ] Skills 模块：CRUD 操作 + 关联 Prompts

### US-3: 完善内容管理模块

**作为** 管理员
**我想要** 管理问题库和推荐内容
**以便于** 丰富系统的知识库

**验收标准：**

- [ ] Questions 模块：CRUD + 分类筛选
- [ ] Recommendations 模块：CRUD + 状态管理

## 建议开发顺序

1. **Crawlers 模块修复** - 高优先级，影响数据采集流程
2. **LLM 模块** - AI 核心，其他模块依赖
3. **Prompts 模块** - Skills 依赖 Prompts
4. **Skills 模块** - 顾问功能依赖 Skills
5. **Questions 模块** - 内容管理
6. **Recommendations 模块** - 内容管理

## 技术规范

- 后端：FastAPI + Supabase Python Client
- 前端：React + TypeScript + shadcn/ui
- 遵循 steering 规则中的模板和规范
