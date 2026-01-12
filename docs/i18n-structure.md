# 国际化结构（集中管理）

## 目录结构

```
src/locales/
├── zh.ts          # 中文翻译
├── en.ts          # 英文翻译
└── index.ts       # 统一导出
```

## 翻译文件格式

```typescript
// locales/zh.ts
export default {
  common: {
    loading: "加载中...",
    save: "保存",
    cancel: "取消",
  },
  admin: {
    title: "管理后台",
    users: "用户管理",
  },
  advisor: {
    title: "北美生活顾问",
  },
  auth: {
    email: "电子邮箱",
  },
};
```

## 使用方式

### 方式 1：使用 Hook（推荐）

```typescript
import { useI18n, type Language } from "@/locales";

function MyComponent({ lang }: { lang: Language }) {
  const t = useI18n(lang);

  return (
    <div>
      <span>{t.common.loading}</span>
      <span>{t.admin.title}</span>
    </div>
  );
}
```

### 方式 2：使用合并后的模块 locales（兼容旧代码）

```typescript
import { adminLocales } from "@/locales";
// 或
import { adminLocales } from "@/modules/admin/locales";

function AdminView({ lang }: { lang: Language }) {
  const t = adminLocales[lang]; // 已合并 common + admin

  return (
    <div>
      <span>{t.loading}</span> {/* common */}
      <span>{t.title}</span> {/* admin */}
    </div>
  );
}
```

## 命名空间

| 命名空间  | 用途                                         |
| --------- | -------------------------------------------- |
| `common`  | 通用操作（loading, save, cancel, delete...） |
| `admin`   | 管理后台                                     |
| `advisor` | 顾问模块                                     |
| `auth`    | 认证模块                                     |

## 硬编码规则

### 禁止的模式

```typescript
// ❌ 错误：三元表达式硬编码
{lang === "zh" ? "删除" : "Delete"}
{lang === "zh" ? "确认删除？" : "Confirm delete?"}

// ❌ 错误：直接写中文/英文
<label>电子邮箱</label>
<button>Submit</button>

// ❌ 错误：fallback 硬编码
{t.syncPrompts || "同步 Prompts"}
```

### 正确的模式

```typescript
// ✅ 正确：使用 locales
{t.delete}
{t.confirmDelete}
<label>{t.email}</label>
<button>{t.submit}</button>

// ✅ 正确：确保 locales 中有对应的 key
{t.syncPrompts}
```

### 例外情况

以下情况允许硬编码：

1. **语言切换按钮**：显示目标语言名称

   ```typescript
   {
     lang === "zh" ? "EN" : "中文";
   }
   ```

2. **数据映射对象**：用于下拉选项等

   ```typescript
   const CATEGORY_OPTIONS = [
     { value: "tools", label: { zh: "工具", en: "Tools" } },
   ];
   ```

3. **代码注释**：注释中的中文是允许的

4. **占位符/示例**：如 email placeholder
   ```typescript
   placeholder = "name@example.com";
   ```

## 规则

1. **所有翻译集中在 `src/locales/`**
2. 翻译文件必须同时包含 `zh` 和 `en`
3. 新增翻译按命名空间分类
4. **禁止在组件中硬编码用户可见文本**
5. 模块的 `locales/index.ts` 只做重新导出
6. 新增功能时先在 locales 中添加翻译 key
