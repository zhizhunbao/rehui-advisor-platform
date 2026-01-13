# Design Document: Frontend Refactor

## Overview

本设计文档描述了前端代码重构的技术方案，目标是使现有代码符合 `coding-standards.md` 编码规范。重构涉及以下核心变更：

1. 将 Views 中的 Service 调用迁移到 Hooks
2. 将 Views 中的样式代码抽象为 Components
3. 将分散的类型定义集中到 `common/types.ts`
4. 修复 TypeScript 类型错误

## Architecture

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Views Layer                          │
│  - 页面布局和组件组合                                         │
│  - 禁止 className 样式                                       │
│  - 禁止直接调用 Services                                     │
│  - 禁止直接使用 fetch/axios                                  │
│  - 只能调用 Hooks 和 Components                              │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│      Components Layer       │ │        Hooks Layer          │
│  - UI 渲染和样式             │ │  - 状态管理和业务逻辑        │
│  - 允许 className 样式       │ │  - 禁止 interface 定义      │
│  - 禁止调用 Services         │ │  - 调用 Services 获取数据   │
│  - 禁止直接使用 fetch/axios  │ │  - 返回数据和方法           │
│  - 必须通过 Hooks 获取数据   │ └─────────────────────────────┘
└─────────────────────────────┘               │
              │                               ▼
              │               ┌─────────────────────────────┐
              │               │      Services Layer         │
              │               │  - API 调用和数据转换        │
              │               │  - 禁止 interface 定义      │
              │               │  - 使用 keysToCamel() 转换  │
              │               └─────────────────────────────┘
              │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Common Layer                          │
│  - types.ts: 所有类型定义                                    │
│  - enum.ts: 所有枚举和常量                                   │
│  - helper.ts: 所有工具函数                                   │
│  - stores.ts: 全局状态                                       │
└─────────────────────────────────────────────────────────────┘
```

### 依赖关系图

```
                    ┌──────────┐
                    │  Views   │
                    └────┬─────┘
                         │ 导入
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
    ┌────────────┐ ┌──────────┐ ┌──────────┐
    │ Components │ │  Hooks   │ │  Common  │
    └─────┬──────┘ └────┬─────┘ └──────────┘
          │             │              ▲
          │ 导入        │ 导入         │
          ▼             ▼              │
    ┌──────────┐  ┌──────────┐         │
    │  Hooks   │  │ Services │─────────┘
    └────┬─────┘  └────┬─────┘
         │             │
         │ 导入        │ 导入
         ▼             ▼
    ┌──────────┐  ┌──────────┐
    │ Services │  │  Common  │
    └────┬─────┘  └──────────┘
         │
         │ 导入
         ▼
    ┌──────────┐
    │  Common  │
    └──────────┘
```

### 导入规则

```
层级            可导入                              禁止导入
─────────────────────────────────────────────────────────────
common/         无依赖                              -
libs/           common/                             modules/
services/       common/, libs/                      hooks/, components/, views/
hooks/          common/, libs/, services/           components/, views/
components/     common/, libs/, hooks/              services/, views/
views/          common/, libs/, hooks/, components/ services/
```

**数据流向**:

```
Views ──调用──> Hooks ──调用──> Services ──调用──> API
  │               │
  │               └──返回数据──> Views
  │
  └──组合──> Components ──调用──> Hooks ──返回数据──> Components
```

**Components 导入规则详解**:

- ✅ 可以导入 `common/` (类型、枚举、工具函数)
- ✅ 可以导入 `libs/` (shadcn/ui 等)
- ✅ 必须导入同模块 `hooks/` (数据获取)
- ❌ 禁止导入 `services/` (API 调用应通过 hooks)
- ❌ 禁止直接使用 `fetch/axios`

**Views 导入规则详解**:

- ✅ 可以导入 `common/` (类型、枚举、工具函数)
- ✅ 可以导入 `libs/` (shadcn/ui 等)
- ✅ 可以导入同模块 `hooks/` (状态管理)
- ✅ 可以导入同模块 `components/` (UI 组件)
- ❌ 禁止导入 `services/` (API 调用应通过 hooks)
- ❌ 禁止直接使用 `fetch/axios`

## Components and Interfaces

### 新增 Hooks

#### useConversations Hook

```typescript
// frontend/src/modules/admin/hooks/useConversations.ts
import type { AdminConversation, ConversationListParams } from "@/common/types";

export function useConversations() {
  // 状态
  const [conversations, setConversations] = useState<AdminConversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<AdminConversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [total, setTotal] = useState(0);

  // 筛选状态
  const [userId, setUserId] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // 方法
  const fetchConversations = useCallback(async (page: number) => { ... }, []);
  const fetchConversationDetail = useCallback(async (id: string) => { ... }, []);
  const deleteConversation = useCallback(async (id: string) => { ... }, []);
  const resetFilters = useCallback(() => { ... }, []);

  return {
    conversations,
    selectedConversation,
    isLoading,
    total,
    userId,
    setUserId,
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    fetchConversations,
    fetchConversationDetail,
    deleteConversation,
    resetFilters,
  };
}
```

#### useDomains Hook (Member)

```typescript
// frontend/src/modules/member/hooks/useDomains.ts
import type { ProductLine, TopicCategory, Lang } from "@/common/types";

export function useDomains(lang: Lang) {
  const [productLines, setProductLines] = useState<ProductLine[]>([]);
  const [activeLineId, setActiveLineId] = useState<string | null>(null);
  const [categories, setCategories] = useState<TopicCategory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProductLines = useCallback(async () => { ... }, []);
  const fetchCategories = useCallback(async (productLineId: string) => { ... }, []);

  return {
    productLines,
    activeLineId,
    setActiveLineId,
    categories,
    isLoading,
    error,
    activeLine: productLines.find(p => p.id === activeLineId),
  };
}
```

### 新增 Components

#### Admin Module Components

```typescript
// frontend/src/modules/admin/components/AdminConversationTable.tsx
// 使用 useConversations hook 获取数据
export function AdminConversationTable({ lang }: { lang: Language }) {
  const { conversations, fetchConversationDetail, deleteConversation } =
    useConversations();
  // ... 渲染逻辑
}

// frontend/src/modules/admin/components/AdminConversationDetailDialog.tsx
// 使用 useConversations hook 获取选中的对话
export function AdminConversationDetailDialog({ lang }: { lang: Language }) {
  const { selectedConversation, showDetail, setShowDetail } =
    useConversations();
  // ... 渲染逻辑
}

// frontend/src/modules/admin/components/AdminConversationFilter.tsx
// 使用 useConversations hook 获取筛选状态
export function AdminConversationFilter({ lang }: { lang: Language }) {
  const {
    userId,
    setUserId,
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    resetFilters,
  } = useConversations();
  // ... 渲染逻辑
}
```

#### Member Module Components

```typescript
// frontend/src/modules/member/components/MemberHomeHeader.tsx
// 纯展示组件，通过 props 接收数据
interface MemberHomeHeaderProps {
  title: string;
  subtitle: string;
}

// frontend/src/modules/member/components/MemberProductLineSelector.tsx
// 使用 useDomains hook 获取数据
export function MemberProductLineSelector({ lang }: { lang: Language }) {
  const { productLines, activeLineId, setActiveLineId } = useDomains(lang);
  // ... 渲染逻辑
}

// frontend/src/modules/member/components/MemberTopicCategoryGrid.tsx
// 使用 useDomains hook 获取数据
interface MemberTopicCategoryGridProps {
  onTopicClick: (topic: Topic) => void;
}
export function MemberTopicCategoryGrid({
  onTopicClick,
}: MemberTopicCategoryGridProps) {
  const { categories } = useDomains();
  // ... 渲染逻辑
}
```

### 更新 usePrompts Hook

```typescript
// frontend/src/modules/admin/hooks/usePrompts.ts
export function usePrompts(lang: Language) {
  // 现有状态
  const [prompts, setPrompts] = useState<AdminPrompt[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // 新增状态 (满足 PromptsView 需求)
  const [stats, setStats] = useState<AdminPromptStats | null>(null);
  const [categoryLabels, setCategoryLabels] = useState<SkillLabel[]>([]);
  const [sourceLabels, setSourceLabels] = useState<SkillLabel[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("__all__");
  const [source, setSource] = useState("__all__");
  const [isSyncing, setIsSyncing] = useState(false);

  // 新增方法
  const getCategoryLabel = useCallback((code: string) => { ... }, [categoryLabels, lang]);
  const getSourceLabel = useCallback((code: string) => { ... }, [sourceLabels, lang]);
  const handleToggle = useCallback(async (id: string) => { ... }, []);
  const handleSync = useCallback(async () => { ... }, []);
  const handleReset = useCallback(() => { ... }, []);

  // loadMoreRef for infinite scroll
  const loadMoreRef = useRef<HTMLDivElement>(null);

  return {
    prompts,
    stats,
    categoryLabels,
    sourceLabels,
    isLoading,
    error,
    hasMore,
    total,
    loadMoreRef,
    search,
    setSearch,
    category,
    setCategory,
    source,
    setSource,
    getCategoryLabel,
    getSourceLabel,
    handleToggle,
    handleSync,
    handleReset,
    isSyncing,
  };
}
```

## Data Models

### 类型定义迁移

以下类型需要确保在 `common/types.ts` 中定义：

```typescript
// common/types.ts 新增/确认类型

// Hook Options 类型
export interface UseSkillsOptions {
  autoFetch?: boolean;
}

export interface UsePromptsOptions {
  autoFetch?: boolean;
}

export interface UseRetrievalOptions {
  autoFetch?: boolean;
}

export interface UseConversationsOptions {
  autoFetch?: boolean;
}

export interface UseDomainsOptions {
  lang: Lang;
  autoFetch?: boolean;
}
```

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

### Property 1: Views 不导入 Services

_For any_ View file in `modules/*/views/`, the file SHALL NOT contain import statements from `services/` directory.

**Validates: Requirements 1.1**

### Property 2: Views 不包含 className

_For any_ View file in `modules/*/views/`, the file SHALL NOT contain `className` attributes after refactoring.

**Validates: Requirements 2.1, 2.8**

### Property 3: Services 不导出类型

_For any_ Service file in `modules/*/services/`, the file SHALL NOT contain `export interface` or `export type` statements.

**Validates: Requirements 4.1, 4.3**

### Property 4: Hooks 不导出类型

_For any_ Hook file in `modules/*/hooks/`, the file SHALL NOT contain `export interface` or `export type` statements (except for internal non-exported interfaces).

**Validates: Requirements 5.1, 5.5**

### Property 5: Components 不导入 Services

_For any_ Component file in `modules/*/components/`, the file SHALL NOT contain import statements from `services/` directory.

**Validates: Requirements 6.2**

### Property 6: Views 和 Components 不直接使用 fetch/axios

_For any_ View or Component file, the file SHALL NOT contain direct `fetch()` or `axios` calls.

**Validates: Requirements 1.1, 6.1**

### Property 7: TypeScript 编译无错误

_For any_ TypeScript file in the frontend codebase, running `tsc --noEmit` SHALL produce zero errors.

**Validates: Requirements 7.1, 7.2, 7.3**

### Property 8: Hook 返回类型完整性

_For any_ Hook used by a View or Component, the Hook's return type SHALL include all properties that the View/Component destructures from it.

**Validates: Requirements 3.1, 3.2**

## Error Handling

### 重构过程中的错误处理

1. **类型错误**: 在迁移类型定义时，确保所有引用都更新为从 `common/types.ts` 导入
2. **导入错误**: 在移除 Service 导入时，确保对应的 Hook 已提供替代方法
3. **运行时错误**: 在抽取 Components 时，确保 props 传递正确

### 回滚策略

如果重构导致功能异常：

1. 使用 Git 回滚到重构前的状态
2. 分析失败原因
3. 采用更小粒度的重构步骤

## Testing Strategy

### 静态分析测试

使用 ESLint 规则或自定义脚本验证：

- Views 不导入 Services
- Views 不包含 className
- Services 不导出类型
- Hooks 不导出类型
- Components 不导入 Services

### TypeScript 编译测试

运行 `npm run type-check` 或 `tsc --noEmit` 确保：

- 所有类型定义正确
- 无隐式 any 类型
- Hook 返回类型与 View 使用匹配

### 功能回归测试

- 运行现有单元测试
- 手动验证关键页面功能：
  - Admin: Skills、Prompts、Conversations 页面
  - Member: Home 页面

### Property-Based Testing

由于本次重构主要涉及代码结构调整而非业务逻辑，属性测试将聚焦于静态代码分析：

1. **导入规则验证**: 使用 AST 分析验证导入路径符合规范
2. **类型导出验证**: 使用 AST 分析验证类型定义位置正确
3. **样式代码验证**: 使用 AST 分析验证 className 使用位置正确
