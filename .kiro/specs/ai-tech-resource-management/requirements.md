# Requirements Document

## Introduction

本文档定义了智能顾问平台的需求，该平台包含两个核心部分：

**管理员端（Admin Portal）**：AI 技术资源探索与管理平台，允许管理员探索、管理和组织各类 AI 技术资源（Prompts、Skills、LLM 模型、RAG 检索技术、Agent 框架等），支持从多种来源（GitHub、RSS、API）自动同步数据，并提供分类、搜索、筛选等功能。

**会员端（Member Portal）**：多领域生活顾问系统，为用户提供移民签证、住房安居、职业发展、金融理财、医疗健康、交通出行、教育培训等 17 个大类的智能咨询服务，通过 AI 对话帮助用户解决北美生活中的各种问题。

## Glossary

### 通用术语

- **Admin_Portal**: 管理员后台系统，用于管理所有 AI 技术资源和顾问系统配置
- **Member_Portal**: 会员前台系统，用于用户与 AI 顾问进行对话咨询
- **Resource_Manager**: 资源管理模块，负责资源的 CRUD 操作
- **Sync_Service**: 同步服务，负责从外部源自动获取和更新数据
- **Search_Engine**: 搜索引擎，提供资源的全文搜索和筛选功能

### 分类体系

- **Domain_Category**: 领域分类，顶级分类（如移民签证、住房安居、职业发展等 17 个大类）
- **Domain**: 子领域，分类下的具体领域（如工签申请、PR 申请、租房、买房等）
- **Discovery_Keywords**: 发现关键词，用于智能匹配用户问题到对应领域

### AI 技术资源

- **LLM_Model**: 大语言模型配置，包含模型参数、定价、能力等信息
- **Prompt_Template**: 提示词模板，用于特定场景的 AI 对话
- **Skill**: 技能定义，描述 AI 可执行的特定任务
- **Agent_Framework**: Agent 框架，多智能体协作框架
- **RAG_Engine**: 检索增强生成引擎，用于知识检索
- **Data_Source**: 数据源，外部资源的来源配置（GitHub、RSS、API、网站）

### 会员系统

- **Advisor_Service**: 顾问服务，处理用户咨询请求并返回 AI 回复
- **Conversation**: 对话会话，用户与 AI 顾问的对话记录
- **Quota_System**: 配额系统，管理用户的查询次数限制
- **Subscription_Plan**: 订阅计划，定义不同会员等级的权益

## Requirements

### Requirement 1: LLM 模型管理

**User Story:** As an administrator, I want to manage LLM models, so that I can configure and monitor available AI models for the system.

#### Acceptance Criteria

1. WHEN an administrator accesses the LLM management page, THE Admin_Portal SHALL display a list of all LLM models with provider, name, pricing, and status information
2. WHEN an administrator creates a new LLM model, THE Resource_Manager SHALL validate the model configuration and persist it to the database
3. WHEN an administrator updates an LLM model, THE Resource_Manager SHALL update the model configuration and reflect changes immediately
4. WHEN an administrator toggles a model's active status, THE Resource_Manager SHALL update the status and affect model availability in the system
5. WHEN an administrator sets a model as default, THE Resource_Manager SHALL ensure only one model is marked as default per provider
6. WHEN the sync service runs, THE Sync_Service SHALL fetch latest model information from configured sources and update the database
7. IF a model configuration is invalid, THEN THE Resource_Manager SHALL return a descriptive error message

### Requirement 2: Prompt 模板管理

**User Story:** As an administrator, I want to manage prompt templates, so that I can create and organize prompts for different use cases.

#### Acceptance Criteria

1. WHEN an administrator accesses the prompts page, THE Admin_Portal SHALL display prompts grouped by category with search and filter capabilities
2. WHEN an administrator creates a new prompt, THE Resource_Manager SHALL validate the prompt structure and persist it with category association
3. WHEN an administrator updates a prompt template, THE Resource_Manager SHALL update the content and maintain version history
4. WHEN an administrator searches for prompts, THE Search_Engine SHALL return matching prompts based on name, description, or content
5. WHEN an administrator filters prompts by category, THE Admin_Portal SHALL display only prompts belonging to the selected category
6. WHEN the sync service syncs prompts from external sources, THE Sync_Service SHALL merge new prompts without overwriting manual edits
7. IF a prompt template contains invalid placeholders, THEN THE Resource_Manager SHALL validate and report the errors

### Requirement 3: Skill 技能管理

**User Story:** As an administrator, I want to manage AI skills, so that I can define and organize capabilities available to the AI system.

#### Acceptance Criteria

1. WHEN an administrator accesses the skills page, THE Admin_Portal SHALL display skills with category, source, and status information
2. WHEN an administrator creates a new skill, THE Resource_Manager SHALL validate the skill definition and persist it
3. WHEN an administrator imports skills from GitHub, THE Sync_Service SHALL parse the repository and extract skill definitions
4. WHEN an administrator searches for skills, THE Search_Engine SHALL return matching skills based on name, description, or tags
5. WHEN an administrator filters skills by source, THE Admin_Portal SHALL display only skills from the selected source
6. WHEN skill statistics are requested, THE Resource_Manager SHALL return aggregated counts by category and source

### Requirement 4: Agent 框架管理

**User Story:** As an administrator, I want to manage Agent frameworks, so that I can track and organize multi-agent collaboration tools.

#### Acceptance Criteria

1. WHEN an administrator accesses the agent frameworks page, THE Admin_Portal SHALL display frameworks with GitHub stats and description
2. WHEN an administrator adds a new framework by URL, THE Sync_Service SHALL fetch repository metadata from GitHub
3. WHEN an administrator updates framework information, THE Resource_Manager SHALL persist the changes
4. WHEN GitHub sync runs, THE Sync_Service SHALL update stars, forks, and other metadata for all frameworks
5. WHEN an administrator searches for frameworks, THE Search_Engine SHALL return matching frameworks based on name, description, or tags
6. IF a GitHub URL is invalid, THEN THE Sync_Service SHALL return an error with details

### Requirement 5: RAG 检索引擎管理

**User Story:** As an administrator, I want to manage retrieval engines, so that I can configure different retrieval strategies for the system.

#### Acceptance Criteria

1. WHEN an administrator accesses the retrieval page, THE Admin_Portal SHALL display all configured retrieval engines with type and status
2. WHEN an administrator creates a new retrieval engine, THE Resource_Manager SHALL validate the configuration schema and persist it
3. WHEN an administrator tests a retrieval engine, THE RAG_Engine SHALL execute a test query and return results with latency metrics
4. WHEN an administrator sets an engine as default, THE Resource_Manager SHALL ensure only one engine is marked as default
5. WHEN an administrator configures domain-specific engines, THE Resource_Manager SHALL associate engines with specific domains
6. IF an engine configuration is invalid, THEN THE Resource_Manager SHALL return validation errors with field details

### Requirement 6: 数据源管理

**User Story:** As an administrator, I want to manage data sources, so that I can configure where the system fetches external resources.

#### Acceptance Criteria

1. WHEN an administrator accesses the data sources page, THE Admin_Portal SHALL display sources grouped by type with status and sync information
2. WHEN an administrator adds a new data source, THE Resource_Manager SHALL validate the URL and create the source configuration
3. WHEN an administrator triggers a manual sync, THE Sync_Service SHALL fetch data from the source and update the database
4. WHEN an administrator views source statistics, THE Admin_Portal SHALL display counts by type, status, and category
5. WHEN an administrator filters sources by category or domain, THE Admin_Portal SHALL display only matching sources
6. WHEN a scheduled sync runs, THE Sync_Service SHALL process all active sources and log results
7. IF a data source URL is unreachable, THEN THE Sync_Service SHALL mark the source as error and log the failure

### Requirement 7: 分类体系管理

**User Story:** As an administrator, I want to manage the category hierarchy, so that I can organize resources in a structured way.

#### Acceptance Criteria

1. WHEN an administrator accesses the categories page, THE Admin_Portal SHALL display the category hierarchy with domain counts
2. WHEN an administrator creates a new category, THE Resource_Manager SHALL validate uniqueness and persist the category
3. WHEN an administrator creates a new domain under a category, THE Resource_Manager SHALL associate the domain with the category
4. WHEN an administrator reorders categories or domains, THE Resource_Manager SHALL update sort orders and reflect changes immediately
5. WHEN an administrator toggles category/domain active status, THE Resource_Manager SHALL cascade the status to related resources
6. IF a category code already exists, THEN THE Resource_Manager SHALL return a duplicate error

### Requirement 8: 搜索与筛选

**User Story:** As an administrator, I want to search and filter resources, so that I can quickly find specific items across all resource types.

#### Acceptance Criteria

1. WHEN an administrator enters a search query, THE Search_Engine SHALL search across all resource types and return ranked results
2. WHEN an administrator applies filters, THE Search_Engine SHALL combine filters with AND logic and return matching results
3. WHEN search results are displayed, THE Admin_Portal SHALL show resource type, name, and relevance score
4. WHEN an administrator clears filters, THE Admin_Portal SHALL reset to showing all resources
5. WHEN pagination is applied, THE Search_Engine SHALL return paginated results with total count

### Requirement 9: 数据同步与调度

**User Story:** As an administrator, I want to schedule automatic data synchronization, so that resources stay up-to-date without manual intervention.

#### Acceptance Criteria

1. WHEN an administrator creates a sync job, THE Sync_Service SHALL validate the cron expression and create the scheduled task
2. WHEN a scheduled job runs, THE Sync_Service SHALL execute the sync and log execution results
3. WHEN an administrator views job history, THE Admin_Portal SHALL display recent executions with status and duration
4. WHEN an administrator manually triggers a job, THE Sync_Service SHALL execute immediately and return results
5. WHEN a job fails, THE Sync_Service SHALL log the error and optionally notify administrators
6. IF a cron expression is invalid, THEN THE Sync_Service SHALL return a validation error

### Requirement 10: 数据导入导出

**User Story:** As an administrator, I want to import and export resource data, so that I can backup data and migrate between environments.

#### Acceptance Criteria

1. WHEN an administrator exports resources, THE Resource_Manager SHALL generate a JSON file containing selected resource types
2. WHEN an administrator imports resources, THE Resource_Manager SHALL validate the JSON structure and merge data
3. WHEN importing duplicate resources, THE Resource_Manager SHALL provide options to skip, overwrite, or rename
4. WHEN export completes, THE Admin_Portal SHALL provide a download link for the generated file
5. IF import data is malformed, THEN THE Resource_Manager SHALL return detailed validation errors

---

## Part B: 会员端 - 多领域生活顾问系统

### Requirement 11: 领域分类浏览

**User Story:** As a member, I want to browse advisor categories, so that I can find the right advisor for my specific needs.

#### Acceptance Criteria

1. WHEN a member accesses the home page, THE Member_Portal SHALL display all 17 domain categories with icons and descriptions
2. WHEN a member clicks on a category, THE Member_Portal SHALL display all sub-domains under that category
3. WHEN a member selects a domain, THE Member_Portal SHALL start a new conversation with the domain-specific advisor
4. WHEN displaying categories, THE Member_Portal SHALL show categories in the configured sort order
5. WHEN a category or domain is inactive, THE Member_Portal SHALL hide it from the member view

### Requirement 12: AI 顾问对话

**User Story:** As a member, I want to chat with AI advisors, so that I can get answers to my questions about life in North America.

#### Acceptance Criteria

1. WHEN a member sends a message, THE Advisor_Service SHALL process the message using the domain-specific prompt template
2. WHEN the AI generates a response, THE Advisor_Service SHALL stream the response in real-time to the member
3. WHEN the response includes sources, THE Advisor_Service SHALL display source links with the response
4. WHEN a member asks a follow-up question, THE Advisor_Service SHALL maintain conversation context
5. WHEN the AI cannot answer a question, THE Advisor_Service SHALL suggest related domains or provide general guidance
6. IF the member exceeds their quota, THEN THE Quota_System SHALL display a quota exceeded message

### Requirement 13: 对话历史管理

**User Story:** As a member, I want to manage my conversation history, so that I can review past conversations and continue where I left off.

#### Acceptance Criteria

1. WHEN a member accesses the conversation list, THE Member_Portal SHALL display all past conversations with titles and timestamps
2. WHEN a member clicks on a conversation, THE Member_Portal SHALL load the full conversation history
3. WHEN a member continues a conversation, THE Advisor_Service SHALL maintain the previous context
4. WHEN a member deletes a conversation, THE Member_Portal SHALL remove it from the list and database
5. WHEN a new conversation starts, THE Member_Portal SHALL auto-generate a title based on the first message

### Requirement 14: 用户配额管理

**User Story:** As a member, I want to see my usage quota, so that I can manage my queries and upgrade if needed.

#### Acceptance Criteria

1. WHEN a member views their profile, THE Quota_System SHALL display current usage and remaining quota
2. WHEN a member sends a query, THE Quota_System SHALL decrement the remaining quota
3. WHEN the quota resets, THE Quota_System SHALL restore the quota to the plan limit
4. WHEN a member approaches their limit, THE Quota_System SHALL display a warning message
5. IF a member has no remaining quota, THEN THE Quota_System SHALL block new queries and suggest upgrading

### Requirement 15: 会员认证

**User Story:** As a user, I want to register and login, so that I can access personalized advisor services.

#### Acceptance Criteria

1. WHEN a user registers, THE Member_Portal SHALL create an account with email and password
2. WHEN a user logs in, THE Member_Portal SHALL authenticate and return access tokens
3. WHEN a user accesses without login, THE Member_Portal SHALL create an anonymous session with limited quota
4. WHEN an anonymous user registers, THE Member_Portal SHALL migrate their conversation history to the new account
5. WHEN a user logs out, THE Member_Portal SHALL invalidate the session tokens
6. IF login credentials are invalid, THEN THE Member_Portal SHALL return an authentication error

### Requirement 16: 智能领域推荐

**User Story:** As a member, I want to get domain recommendations, so that I can discover relevant advisors based on my questions.

#### Acceptance Criteria

1. WHEN a member types a question, THE Search_Engine SHALL suggest relevant domains based on keywords
2. WHEN displaying suggestions, THE Member_Portal SHALL show domain name, category, and match confidence
3. WHEN a member selects a suggestion, THE Member_Portal SHALL start a conversation in that domain
4. WHEN no exact match is found, THE Search_Engine SHALL suggest the closest matching domains
5. WHEN the member is in a conversation, THE Advisor_Service SHALL suggest related domains if the question is out of scope

### Requirement 17: 多语言支持

**User Story:** As a member, I want to use the system in my preferred language, so that I can communicate more effectively.

#### Acceptance Criteria

1. WHEN a member selects a language, THE Member_Portal SHALL display all UI elements in that language
2. WHEN displaying domain information, THE Member_Portal SHALL show localized names and descriptions
3. WHEN the AI responds, THE Advisor_Service SHALL respond in the same language as the user's message
4. WHEN switching languages, THE Member_Portal SHALL persist the preference for future sessions

---

## Part C: 初始化数据需求

### Requirement 18: 领域分类初始化数据

**User Story:** As a system administrator, I want pre-configured domain categories, so that the system is ready to use after deployment.

#### Acceptance Criteria

1. THE System SHALL include 17 pre-configured domain categories:

   - 移民签证 (Immigration & Visa)
   - 住房安居 (Housing)
   - 职业发展 (Career)
   - 金融理财 (Finance)
   - 医疗健康 (Healthcare)
   - 交通出行 (Transportation)
   - 教育培训 (Education)
   - 日常生活 (Daily Life)
   - 法律权益 (Legal)
   - 社交融入 (Social)
   - 身份证件 (Identity)
   - 出行旅游 (Travel)
   - 通讯网络 (Communication)
   - 餐饮购物 (Food & Shopping)
   - 休闲娱乐 (Leisure)
   - 家政服务 (Home Services)
   - 人生大事 (Life Events)

2. WHEN the system initializes, THE Resource_Manager SHALL seed all categories with icons, colors, and bilingual descriptions
3. WHEN a category is seeded, THE Resource_Manager SHALL also seed its associated sub-domains

### Requirement 19: LLM 模型初始化数据

**User Story:** As a system administrator, I want pre-configured LLM models, so that the AI advisors can function immediately.

#### Acceptance Criteria

1. THE System SHALL include pre-configured LLM models:

   - GPT-4o (OpenAI)
   - GPT-4o Mini (OpenAI, default)
   - Claude 3.5 Sonnet (Anthropic)
   - DeepSeek Chat (DeepSeek)
   - Gemini 2.0 Flash (Google)
   - Llama 3.3 70B (Groq)

2. WHEN the system initializes, THE Resource_Manager SHALL seed all models with provider, endpoint, and configuration
3. WHEN models are seeded, THE Resource_Manager SHALL mark one model as the default

### Requirement 20: 检索引擎初始化数据

**User Story:** As a system administrator, I want pre-configured retrieval engines, so that the system can retrieve relevant information.

#### Acceptance Criteria

1. THE System SHALL include pre-configured retrieval engines:

   - 关键词匹配 (Keyword Match)
   - 结构化查询 (Structured Query, default)
   - RAG 向量检索 (RAG Vector)
   - PageIndex 树形推理 (PageIndex)
   - Agent 工具调用 (Agent Tools)
   - 实时网络搜索 (Realtime Search)
   - 混合引擎 (Hybrid)

2. WHEN the system initializes, THE Resource_Manager SHALL seed all engines with type, configuration, and description
3. WHEN engines are seeded, THE Resource_Manager SHALL configure domain-specific engine mappings

### Requirement 21: Prompt 模板初始化数据

**User Story:** As a system administrator, I want pre-configured prompt templates, so that AI advisors have proper instructions.

#### Acceptance Criteria

1. THE System SHALL include pre-configured prompt templates for each domain category
2. WHEN the system initializes, THE Resource_Manager SHALL seed prompts with system prompts and user templates
3. WHEN prompts are seeded, THE Resource_Manager SHALL associate prompts with their respective domains
4. THE prompts SHALL include bilingual support (Chinese and English)
