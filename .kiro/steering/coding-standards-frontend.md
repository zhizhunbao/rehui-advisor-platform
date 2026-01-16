---
inclusion: fileMatch
fileMatchPattern: "**/frontend/**"
---

# 前端编码规范

## 导入规则

- `common/` → 无依赖，可被任何层导入
- `libs/` → 只导入 `common/`
- `modules/*/types/` → 只导入 `common/`
- `modules/*/services/` → 导入 `common/`, `libs/`, 同模块 `types/`
- `modules/*/hooks/` → 导入 `common/`, 同模块 `services/`, `types/`
- `modules/*/components/` → 导入 `common/`, `libs/`, 同模块 `types/`（禁止导入 hooks/services）
- `modules/*/views/` → 导入同模块 `hooks/`, `components/` + `common/` + `libs/`
- `App.tsx` → 只导入 `common/` + 同模块 `hooks/` + `views/`

## 导出规则

- `common/enum.ts` → 枚举和常量
- `common/helper.ts` → 工具函数
- `common/types.ts` → 类型定义
- `common/stores.ts` → 全局状态
- 直接从具体文件导入，禁止 `index.ts` 集中导出

## 代码规范

- TypeScript 严格类型，禁止 `any`
- 函数/变量 camelCase，组件 PascalCase
- API 响应用 `keysToCamel()` 转换
- 优先用 `libs/shadcn/ui/` 组件

## 分层职责

- **services**: API 调用，禁止导入 hooks/components
- **hooks**: 状态管理，禁止导入 components/views
- **components**: UI 渲染，数据通过 Props 传入，禁止导入 hooks/services
- **views**: 页面布局，通过 hooks 获取数据

## 禁止

- 组件内定义常量（放 `enum.ts`）
- 模块内定义工具函数（放 `helper.ts`）
- 模块内定义 interface（放 `common/types.ts`）
- 使用 TypeScript `enum` 关键字
- 跨模块导入非 `common/` 内容
- console.log / 注释掉的代码提交
- 函数超过 50 行 / 文件超过 300 行
