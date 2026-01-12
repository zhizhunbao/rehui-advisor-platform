# 调度管理模块

## 背景

系统需要定时执行各种任务，如自动更新数据源、自动探索新资源、定时抓取数据等。需要一个统一的调度管理模块来配置和监控这些定时任务。

## 用户故事

### US-1: 查看调度任务列表

**作为** 管理员
**我想要** 查看所有配置的定时任务
**以便于** 了解系统自动化任务的运行情况

**验收标准：**

- [ ] 显示任务名称、类型、Cron 表达式、状态
- [ ] 显示上次执行时间和下次执行时间
- [ ] 显示最近执行结果（成功/失败）
- [ ] 支持按状态筛选（启用/禁用）

### US-2: 创建调度任务

**作为** 管理员
**我想要** 创建新的定时任务
**以便于** 自动化执行重复性工作

**验收标准：**

- [ ] 选择任务类型（数据源刷新、自动探索、数据抓取等）
- [ ] 配置 Cron 表达式或简单周期（每小时/每天/每周）
- [ ] 配置任务参数（如探索的领域、刷新的分类等）
- [ ] 设置任务启用/禁用状态

### US-3: 手动触发任务

**作为** 管理员
**我想要** 手动触发某个定时任务
**以便于** 立即执行而不等待下次调度

**验收标准：**

- [ ] 点击"立即执行"按钮触发任务
- [ ] 显示执行进度或状态
- [ ] 执行完成后更新最近执行记录

### US-4: 查看执行历史

**作为** 管理员
**我想要** 查看任务的执行历史
**以便于** 排查问题和了解执行情况

**验收标准：**

- [ ] 显示执行时间、耗时、状态
- [ ] 显示执行结果摘要（如：刷新了 X 个数据源）
- [ ] 失败时显示错误信息
- [ ] 支持分页查看历史记录

## 预设任务类型

| 类型                   | 说明             | 参数                      |
| ---------------------- | ---------------- | ------------------------- |
| `refresh_data_sources` | 刷新数据源元数据 | category (可选)           |
| `auto_discover`        | 自动探索新资源   | domain, limit_per_keyword |
| `crawl_sources`        | 执行数据抓取     | source_ids (可选)         |
| `sync_llm_models`      | 同步 LLM 模型    | -                         |
| `sync_prompts`         | 同步 Prompts     | -                         |
| `sync_skills`          | 同步 Skills      | -                         |

## 数据模型

### scheduled_jobs 表

```sql
CREATE TABLE scheduled_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  job_type VARCHAR(50) NOT NULL,
  cron_expression VARCHAR(100) NOT NULL,
  parameters JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  last_run_at TIMESTAMPTZ,
  next_run_at TIMESTAMPTZ,
  last_status VARCHAR(20),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### job_executions 表

```sql
CREATE TABLE job_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID REFERENCES scheduled_jobs(id) ON DELETE CASCADE,
  started_at TIMESTAMPTZ NOT NULL,
  finished_at TIMESTAMPTZ,
  status VARCHAR(20) NOT NULL,
  result JSONB,
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## API 设计

```
GET    /scheduler/jobs              # 获取任务列表
POST   /scheduler/jobs              # 创建任务
GET    /scheduler/jobs/{id}         # 获取任务详情
PUT    /scheduler/jobs/{id}         # 更新任务
DELETE /scheduler/jobs/{id}         # 删除任务
POST   /scheduler/jobs/{id}/toggle  # 启用/禁用任务
POST   /scheduler/jobs/{id}/trigger # 手动触发任务
GET    /scheduler/jobs/{id}/history # 获取执行历史
GET    /scheduler/job-types         # 获取可用任务类型
```

## 技术实现

### 方案 A: APScheduler (推荐)

- 使用 APScheduler 库管理定时任务
- 任务配置存储在数据库
- 应用启动时从数据库加载任务

### 方案 B: Celery Beat

- 使用 Celery + Redis 实现分布式调度
- 适合大规模部署

### 方案 C: 外部调度器

- 使用 cron 或云服务的调度功能
- 通过 API 触发任务执行

## 前端组件

- `SchedulerView.tsx` - 调度管理页面
- `JobFormModal.tsx` - 任务创建/编辑弹窗
- `JobHistoryModal.tsx` - 执行历史弹窗
- `CronExpressionInput.tsx` - Cron 表达式输入组件

## 实现优先级

1. **P0**: 数据库表结构 + 基础 CRUD API
2. **P0**: 前端管理界面
3. **P1**: 手动触发任务
4. **P1**: 执行历史记录
5. **P2**: APScheduler 集成（实际定时执行）
