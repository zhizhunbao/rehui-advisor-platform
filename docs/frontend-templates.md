---
inclusion: always
---

# 前端代码模板

## 目录结构

```
frontend/src/
├── common/                            # 公共模块
│   ├── components/                    # 公共组件 (ErrorBoundary)
│   ├── context/                       # 公共 Context (ToastContext)
│   ├── errors/                        # 错误类型 (ApiError)
│   ├── hooks/                         # 公共 Hooks (useErrorHandler)
│   ├── http/                          # HTTP 客户端
│   ├── i18n/                          # 国际化 (common, Language, mergeTranslations)
│   ├── logger/                        # 日志工具
│   └── index.ts
├── modules/                           # 业务模块
│   ├── admin/                         # 管理后台模块
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── locales/
│   │   ├── services/
│   │   ├── types/
│   │   └── index.ts
│   ├── advisor/                       # 顾问模块
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── locales/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   └── index.ts
│   └── auth/                          # 认证模块
│       ├── components/
│       ├── hooks/
│       ├── locales/
│       ├── services/
│       ├── store/
│       ├── types/
│       └── index.ts
├── views/                             # 页面视图
│   ├── admin/                         # 管理后台页面
│   ├── locales/
│   └── *.tsx
├── AdminApp.tsx                       # 管理后台入口
├── App.tsx                            # 主应用入口
└── main.tsx
```

## React 组件

```tsx
// modules/{module}/components/{ComponentName}.tsx
import type { Language } from '@/common/i18n';
import { {module}Locales } from '../locales';

interface {ComponentName}Props {
  lang: Language;
  className?: string;
}

const {ComponentName}: React.FC<{ComponentName}Props> = ({ lang, className }) => {
  const t = {module}Locales[lang];

  return (
    <div className={className}>
      {/* JSX */}
    </div>
  );
};

export default {ComponentName};
```

## 带状态的组件

```tsx
// modules/{module}/components/{ComponentName}.tsx
import { useState, useCallback } from 'react';
import type { Language } from '@/common/i18n';
import { {module}Locales } from '../locales';

interface {ComponentName}Props {
  lang: Language;
  onSubmit?: (data: FormData) => void;
}

const {ComponentName}: React.FC<{ComponentName}Props> = ({ lang, onSubmit }) => {
  const t = {module}Locales[lang];
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await onSubmit?.({});
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [onSubmit]);

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="text-red-500">{error}</div>}
      <button type="submit" disabled={isLoading}>
        {isLoading ? t.loading : t.submit}
      </button>
    </form>
  );
};

export default {ComponentName};
```

## 自定义 Hook

```typescript
// modules/{module}/hooks/use{HookName}.ts
import { useState, useEffect, useCallback } from 'react';

interface Use{HookName}Options {
  autoFetch?: boolean;
}

export function use{HookName}<T>(options: Use{HookName}Options = {}) {
  const { autoFetch = true } = options;
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // const result = await apiCall();
      // setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) fetch();
  }, [autoFetch, fetch]);

  return { data, isLoading, error, refetch: fetch };
}
```

## API Service

```typescript
// modules/{module}/services/{module}.service.ts
import { http } from '@/common/http';
import type { {Module}, Create{Module}Dto, Update{Module}Dto } from '../types/{module}.types';

export const {module}Service = {
  getAll(params?: Record<string, string>) {
    const query = params ? `?${new URLSearchParams(params)}` : '';
    return http.get<{Module}[]>(`/{modules}${query}`);
  },

  getById(id: string) {
    return http.get<{Module}>(`/{modules}/${id}`);
  },

  create(data: Create{Module}Dto) {
    return http.post<{Module}>('/{modules}', data);
  },

  update(id: string, data: Update{Module}Dto) {
    return http.put<{Module}>(`/{modules}/${id}`, data);
  },

  delete(id: string) {
    return http.delete<void>(`/{modules}/${id}`);
  },
};
```

## Context/Provider

```tsx
// modules/{module}/context/{Name}Context.tsx
import { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface {Name}State {
  // 状态字段
}

interface {Name}ContextValue extends {Name}State {
  updateState: (partial: Partial<{Name}State>) => void;
  reset: () => void;
}

const initial{Name}State: {Name}State = {};

const {Name}Context = createContext<{Name}ContextValue | null>(null);

export function {Name}Provider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<{Name}State>(initial{Name}State);

  const updateState = useCallback((partial: Partial<{Name}State>) => {
    setState(prev => ({ ...prev, ...partial }));
  }, []);

  const reset = useCallback(() => setState(initial{Name}State), []);

  return (
    <{Name}Context.Provider value={{ ...state, updateState, reset }}>
      {children}
    </{Name}Context.Provider>
  );
}

export function use{Name}() {
  const context = useContext({Name}Context);
  if (!context) throw new Error('use{Name} must be used within {Name}Provider');
  return context;
}
```

## View/Page 组件结构规范

View 组件内部代码必须按以下顺序组织：

```tsx
// views/admin/{Name}View.tsx
import { useState, useEffect, useCallback } from 'react';
import { adminLocales, type Language } from '@/locales';
// ... 其他 imports

// ============ 类型定义 ============
interface {Name}ViewProps {
  lang: Language;
}

// ============ 常量 ============
const API_BASE = import.meta.env.VITE_API_URL || '/api';
const getHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('admin_token') || ''}`,
});

// ============ 主组件 ============
export default function {Name}View({ lang }: {Name}ViewProps) {
  // 1️⃣ 国际化
  const t = adminLocales[lang];

  // 2️⃣ 状态 - 按用途分组
  // UI 状态
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // 数据状态
  const [data, setData] = useState<Item[]>([]);
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);

  // 筛选状态
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('');

  // 3️⃣ 数据获取函数 (useCallback)
  const fetchData = useCallback(async () => {
    // ...
  }, [dependencies]);

  // 4️⃣ 副作用 (useEffect)
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // 5️⃣ 事件处理函数 - handle 前缀
  const handleCreate = async () => { /* ... */ };
  const handleEdit = (item: Item) => { /* ... */ };
  const handleDelete = async (id: string) => { /* ... */ };
  const handleSearch = () => { /* ... */ };

  // 6️⃣ 渲染辅助函数（可选）
  const renderFilters = () => { /* ... */ };

  // 7️⃣ 条件渲染 - 加载/空状态
  if (isLoading && data.length === 0) {
    return <LoadingState lang={lang} />;
  }

  // 8️⃣ 主渲染
  return (
    <PageContainer>
      {/* 页面头部 */}
      <PageHeader title={t.title} actions={<Button>...</Button>} />

      {/* 统计卡片（可选） */}
      <StatsGrid>...</StatsGrid>

      {/* 筛选栏（可选） */}
      <FilterBar>...</FilterBar>

      {/* 主内容区 */}
      <DataTable ... /> 或 <CardGrid ... />

      {/* 弹窗（可选） */}
      {showModal && <Modal ... />}
    </PageContainer>
  );
}

// ============ 子组件（同文件内） ============
// 只有该 View 专用的小组件才放这里
// 通用组件应提取到 components/ 目录

function ItemModal({ ... }: ItemModalProps) {
  // ...
}
```

## View 组件代码顺序速查

| 顺序 | 内容     | 示例                            |
| ---- | -------- | ------------------------------- |
| 1    | 国际化   | `const t = adminLocales[lang]`  |
| 2    | 状态声明 | `useState` - UI/数据/筛选分组   |
| 3    | 数据获取 | `useCallback` 包裹的 fetch 函数 |
| 4    | 副作用   | `useEffect`                     |
| 5    | 事件处理 | `handle*` 函数                  |
| 6    | 渲染辅助 | `render*` 函数（可选）          |
| 7    | 条件渲染 | 加载/空状态的 early return      |
| 8    | 主渲染   | `return <PageContainer>...`     |

## 状态命名规范

```tsx
// ✅ 正确
const [isLoading, setIsLoading] = useState(false); // 布尔: is/has/can/should
const [showModal, setShowModal] = useState(false); // 显示控制: show
const [users, setUsers] = useState<User[]>([]); // 列表: 复数
const [selectedUser, setSelectedUser] = useState(null); // 选中项: selected
const [search, setSearch] = useState(""); // 筛选: 字段名
const [statusFilter, setStatusFilter] = useState(""); // 筛选: xxxFilter

// ❌ 错误
const [loading, setLoading] = useState(false); // 缺少 is 前缀
const [modal, setModal] = useState(false); // 不清晰
const [user, setUser] = useState([]); // 列表应用复数
```

## Locales

```typescript
// modules/{module}/locales/index.ts
export const {module}Locales = {
  zh: {
    title: '标题',
    loading: '加载中...',
    submit: '提交',
    cancel: '取消',
    // 业务文案...
  },
  en: {
    title: 'Title',
    loading: 'Loading...',
    submit: 'Submit',
    cancel: 'Cancel',
    // 业务文案...
  },
};
```

## Types

**规则：所有字段必填，不使用可选类型**

```typescript
// modules/{module}/types/{module}.types.ts

// ✅ 正确：所有字段必填
export interface {Module} {
  id: string;
  name: string;
  description: string;
  category: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Create{Module}Dto {
  name: string;
  description: string;
  category: string;
}

export interface Update{Module}Dto {
  name: string;
  description: string;
  category: string;
  is_active: boolean;
}

// ❌ 错误：使用可选字段
export interface {Module} {
  id: string;
  name: string;
  description: string | null;  // 禁止
  category?: string;           // 禁止
}
```

## 模块导出

```typescript
// modules/{module}/index.ts
export * from './types/{module}.types';
export * from './services/{module}.service';
export * from './hooks/use{Module}';
export { {module}Locales } from './locales';
```

---

## shadcn/ui 组件使用规范

**规则：优先使用 shadcn/ui 组件，禁止重复造轮子**

### 组件对照表

| 场景        | 使用组件                                | 导入路径                    |
| ----------- | --------------------------------------- | --------------------------- |
| 弹窗/对话框 | `Dialog`                                | `@/shadcn/ui/dialog`        |
| 确认弹窗    | `AlertDialog`                           | `@/shadcn/ui/alert-dialog`  |
| 侧边抽屉    | `Sheet`                                 | `@/shadcn/ui/sheet`         |
| 底部抽屉    | `Drawer`                                | `@/shadcn/ui/drawer`        |
| 表单        | `Form` + `Input/Select/Checkbox/Switch` | `@/shadcn/ui/form`          |
| 表格        | `Table`                                 | `@/shadcn/ui/table`         |
| 下拉选择    | `Select`                                | `@/shadcn/ui/select`        |
| 下拉菜单    | `DropdownMenu`                          | `@/shadcn/ui/dropdown-menu` |
| 提示        | `Tooltip`                               | `@/shadcn/ui/tooltip`       |
| 弹出卡片    | `Popover`                               | `@/shadcn/ui/popover`       |
| 加载骨架    | `Skeleton`                              | `@/shadcn/ui/skeleton`      |
| 加载动画    | `Spinner`                               | `@/shadcn/ui/spinner`       |
| 标签页      | `Tabs`                                  | `@/shadcn/ui/tabs`          |
| 分页        | `Pagination`                            | `@/shadcn/ui/pagination`    |
| 命令面板    | `Command`                               | `@/shadcn/ui/command`       |
| 日历        | `Calendar`                              | `@/shadcn/ui/calendar`      |
| 侧边栏      | `Sidebar`                               | `@/shadcn/ui/sidebar`       |
| 开关        | `Switch`                                | `@/shadcn/ui/switch`        |
| 复选框      | `Checkbox`                              | `@/shadcn/ui/checkbox`      |
| 单选组      | `RadioGroup`                            | `@/shadcn/ui/radio-group`   |
| 滑块        | `Slider`                                | `@/shadcn/ui/slider`        |
| 文本域      | `Textarea`                              | `@/shadcn/ui/textarea`      |
| 徽章        | `Badge`                                 | `@/shadcn/ui/badge`         |
| 卡片        | `Card`                                  | `@/shadcn/ui/card`          |
| 按钮        | `Button`                                | `@/shadcn/ui/button`        |
| 头像        | `Avatar`                                | `@/shadcn/ui/avatar`        |
| 进度条      | `Progress`                              | `@/shadcn/ui/progress`      |
| 分隔线      | `Separator`                             | `@/shadcn/ui/separator`     |
| 滚动区域    | `ScrollArea`                            | `@/shadcn/ui/scroll-area`   |
| 折叠面板    | `Accordion` / `Collapsible`             | `@/shadcn/ui/accordion`     |

### 使用示例

```tsx
// ✅ 正确：使用 shadcn/ui Dialog
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/shadcn/ui/dialog";

<Dialog open={showModal} onOpenChange={setShowModal}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>{t.editTitle}</DialogTitle>
    </DialogHeader>
    {/* 表单内容 */}
    <DialogFooter>
      <Button variant="outline" onClick={() => setShowModal(false)}>{t.cancel}</Button>
      <Button onClick={handleSave}>{t.save}</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>

// ❌ 错误：自己写 Modal 组件
function CustomModal({ open, onClose, children }) { ... }
```

### 禁止的模式

```tsx
// ❌ 禁止：自己实现已有的 UI 组件
function MyDialog() { ... }
function MyDropdown() { ... }
function MyTooltip() { ... }
function MyTabs() { ... }

// ❌ 禁止：使用其他 UI 库的同类组件
import { Modal } from 'antd';
import { Dialog } from '@headlessui/react';
```

---

## 通用规则

1. 组件 props 必须定义 interface，以 `Props` 结尾
2. 事件处理函数用 `handle` 前缀
3. 布尔状态用 `is/has/can/should` 前缀
4. 异步操作必须有 loading 和 error 状态
5. 所有用户可见文本必须走 i18n
6. 使用 `useCallback` 包裹传递给子组件的函数
7. 避免在 render 中创建新对象/数组
8. **类型字段必填** - 所有 interface 字段都必须是必填的，禁止使用 `| null`、`| undefined` 或 `?`
9. **渲染时不判空** - 数据字段都有值，直接使用 `{item.name}` 而不是 `{item.name || "-"}`
10. **优先 shadcn/ui** - UI 组件优先使用 shadcn/ui，禁止重复造轮子
