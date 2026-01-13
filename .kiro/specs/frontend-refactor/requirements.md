# Requirements Document

## Introduction

本文档定义了前端代码重构的需求，旨在使现有代码符合 `coding-standards.md` 编码规范。通过分析现有代码库，发现了多处违反规范的问题，包括：Views 层直接调用 Services、Views 层包含 className 样式代码、Services 层导出类型定义、Hooks 返回值与 Views 使用不匹配等。

## Glossary

- **View**: 页面视图组件，负责页面布局和组合组件
- **Hook**: 自定义 React Hook，负责状态管理和业务逻辑
- **Service**: API 服务层，负责 API 调用和数据转换
- **Component**: UI 组件，负责 UI 渲染和样式
- **Coding_Standards**: 项目编码规范文档 `.kiro/steering/coding-standards.md`

## Requirements

### Requirement 1: Views 层禁止直接调用 Services

**User Story:** As a developer, I want Views to only call Hooks for data operations, so that the code follows the layered architecture and is easier to maintain.

#### Acceptance Criteria

1. WHEN a View needs to fetch or mutate data, THE View SHALL call methods from Hooks instead of Services directly
2. WHEN refactoring `SkillsView.tsx`, THE Refactor_Tool SHALL move `skillService.getList()` and `skillService.toggle()` calls into `useSkills` hook
3. WHEN refactoring `ConversationsView.tsx`, THE Refactor_Tool SHALL create a `useConversations` hook to encapsulate all `fetch()` API calls
4. WHEN refactoring `HomeView.tsx`, THE Refactor_Tool SHALL create or use existing hook to encapsulate `domainService` calls

### Requirement 2: Views 层禁止 className 样式代码，抽象为 Components

**User Story:** As a developer, I want Views to focus on layout composition without inline styles, so that styling concerns are separated into Components.

#### Acceptance Criteria

1. WHEN a View contains `className` attributes, THE Refactor_Tool SHALL extract styled elements into Component files
2. WHEN refactoring `ConversationsView.tsx`, THE Refactor_Tool SHALL create `AdminConversationTable.tsx` component for table rendering with styles
3. WHEN refactoring `ConversationsView.tsx`, THE Refactor_Tool SHALL create `AdminConversationDetailDialog.tsx` component for dialog rendering with styles
4. WHEN refactoring `ConversationsView.tsx`, THE Refactor_Tool SHALL create `AdminConversationFilter.tsx` component for filter form with styles
5. WHEN refactoring `HomeView.tsx`, THE Refactor_Tool SHALL create `MemberHomeHeader.tsx` component for header section with styles
6. WHEN refactoring `HomeView.tsx`, THE Refactor_Tool SHALL create `MemberProductLineSelector.tsx` component for product line buttons with styles
7. WHEN refactoring `HomeView.tsx`, THE Refactor_Tool SHALL create `MemberTopicCategoryGrid.tsx` component for category grid with styles
8. THE View files SHALL only contain component composition and layout logic without `className` attributes
9. THE extracted Components SHALL receive data via props and handle only UI rendering with styles

### Requirement 3: Hooks 返回值与 Views 使用保持一致

**User Story:** As a developer, I want Hooks to provide all necessary data and methods that Views need, so that there are no type mismatches.

#### Acceptance Criteria

1. WHEN `PromptsView.tsx` uses properties from `usePrompts`, THE `usePrompts` hook SHALL export all required properties (stats, categoryLabels, sourceLabels, hasMore, total, loadMoreRef, search, setSearch, category, setCategory, source, setSource, getCategoryLabel, getSourceLabel, handleToggle, handleSync, handleReset, isSyncing)
2. WHEN a View expects a specific return type from a Hook, THE Hook SHALL provide that exact type
3. IF a Hook's return type changes, THEN THE View using that Hook SHALL be updated accordingly

### Requirement 4: Services 层禁止导出类型定义

**User Story:** As a developer, I want all type definitions centralized in `common/types.ts`, so that types are consistent across the codebase.

#### Acceptance Criteria

1. WHEN a Service file contains `interface` or `type` exports, THE Refactor_Tool SHALL move them to `common/types.ts`
2. WHEN `domain.service.ts` (member) exports `TopicCategory` and `ProductLine` types, THE Refactor_Tool SHALL ensure these types are imported from `common/types.ts` instead
3. THE Service files SHALL only contain API call functions and data transformation logic

### Requirement 5: Hooks 层禁止导出类型定义

**User Story:** As a developer, I want Hooks to focus on state management and business logic without defining types, so that types remain centralized.

#### Acceptance Criteria

1. WHEN a Hook file contains `interface` or `type` definitions, THE Refactor_Tool SHALL move them to `common/types.ts`
2. WHEN `useSkills.ts` contains `UseSkillsOptions` interface, THE Refactor_Tool SHALL move it to `common/types.ts`
3. WHEN `usePrompts.ts` contains `UsePromptsOptions` interface, THE Refactor_Tool SHALL move it to `common/types.ts`
4. WHEN `useRetrieval.ts` contains `UseRetrievalOptions` interface, THE Refactor_Tool SHALL move it to `common/types.ts`
5. THE Hook files SHALL only contain state management logic and import types from `common/types.ts`

### Requirement 6: Components 层可以包含 className 但禁止调用 Services

**User Story:** As a developer, I want Components to handle UI rendering with styles but not data fetching, so that concerns are properly separated.

#### Acceptance Criteria

1. WHEN a Component needs data, THE Component SHALL receive it via props from parent Views or Hooks
2. THE Component files SHALL NOT import from `services/` directory
3. THE Component files MAY contain `className` attributes for styling

### Requirement 7: 修复 TypeScript 类型错误

**User Story:** As a developer, I want all TypeScript errors resolved, so that the codebase compiles without errors.

#### Acceptance Criteria

1. WHEN `PromptsView.tsx` has type mismatches with `usePrompts` hook, THE Refactor_Tool SHALL fix the hook to match View expectations or update View to match hook return type
2. WHEN `AdminPrompt` type is missing properties (template, source, repo), THE Refactor_Tool SHALL ensure type definitions are complete in `common/types.ts`
3. WHEN implicit `any` types exist (e.g., parameter `c` in filter callbacks), THE Refactor_Tool SHALL add explicit type annotations

### Requirement 8: 确保重构后功能不变

**User Story:** As a developer, I want the refactored code to maintain the same functionality, so that users are not affected by the changes.

#### Acceptance Criteria

1. WHEN refactoring any file, THE Refactor_Tool SHALL preserve all existing functionality
2. WHEN moving code between layers, THE Refactor_Tool SHALL ensure data flow remains correct
3. IF a test exists for refactored code, THEN THE test SHALL continue to pass after refactoring
