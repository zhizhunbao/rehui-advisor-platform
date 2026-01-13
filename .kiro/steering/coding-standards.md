# 编码规范

## 必须

### 导入

- `common/` → 无依赖，可被任何层导入
- `libs/` → 只导入 `common/`
- `modules/*/types/` → 只导入 `common/`
- `modules/*/services/` → 导入 `common/`, `libs/`, 同模块 `types/`
- `modules/*/hooks/` → 导入 `common/`, 同模块 `services/`, `types/`
- `modules/*/components/` → 导入 `common/`, `libs/`, 同模块 `types/`（禁止导入 hooks/services）
- `modules/*/views/` → 导入同模块 `hooks/`, `components/` + `common/` + `libs/`

### 导出

- `common/enum.ts` → 所有枚举和常量映射
- `common/helper.ts` → 所有工具函数
- `common/types.ts` → 所有类型定义（按模块分类）
- `common/stores.ts` → 所有全局状态（按模块分类）
- `common/components/` → 通用 UI 组件（无业务逻辑）
- `modules/*/components/` → 业务组件（可用同模块 hooks）

### 代码

- 数据从 API 获取
- 错误抛出异常，由 UI 层处理
- 使用 TypeScript 严格类型
- 函数/变量使用 camelCase，组件使用 PascalCase
- 文件名与默认导出一致
- 异步函数使用 async/await
- 条件渲染使用早返回
- 复杂逻辑抽取为自定义 hook
- 后端分页使用 `paginate()` 函数
- 前端 API 响应使用 `keysToCamel()` 转换 snake_case → camelCase
- 通用 UI 组件放 `common/components/`，业务组件放 `modules/*/components/`
- 优先用 `libs/shadcn/ui/` 基础组件

### 注释

- 只允许单行注释
- 解释 why，不解释 what
- 文件头部：模块用途说明
- TODO/FIXME：标注待处理事项

---

## 各层职责

### services/

- ✅ 只负责 API 调用和数据转换
- ✅ 从 `common/types` 导入类型
- ❌ 禁止 `interface` 定义
- ❌ 禁止 `const` 常量定义
- ❌ 禁止工具函数定义
- ❌ 禁止导入 `hooks/` 或 `components/`

### hooks/

- ✅ 只负责状态管理和业务逻辑
- ✅ 从 `common/types` 导入类型
- ✅ 返回类型由 TypeScript 自动推断
- ✅ Options 参数用内联类型或放 `common/types.ts`
- ❌ 禁止 `interface` 定义
- ❌ 禁止 `const` 常量定义
- ❌ 禁止工具函数定义
- ❌ 禁止导入 `components/` 或 `views/`

### components/

- ✅ 负责 UI 渲染和样式
- ✅ 从 `common/types` 导入类型
- ✅ 可以写 `className` 样式
- ✅ 只通过 Props 接收数据（纯展示组件）
- ❌ 禁止 `interface` 定义（Props 类型除外）
- ❌ 禁止 `const` 常量定义
- ❌ 禁止工具函数定义
- ❌ 禁止导入 `views/`
- ❌ 禁止导入 `hooks/`（数据通过 Props 传入）
- ❌ 禁止导入 `services/`

### views/

- ✅ 只负责页面布局和组合组件
- ✅ 从 `common/types` 导入类型
- ❌ 禁止 `interface` 定义（Props 类型除外）
- ❌ 禁止 `const` 常量定义
- ❌ 禁止工具函数定义
- ❌ 禁止 `className` 样式代码
- ❌ 禁止直接调用 `services/`（应通过 hooks）

---

## 禁止

### 导入

- ❌ `common/components/` 导入 `services/` 或 `hooks/`
- ❌ `modules/admin/` 与 `modules/member/` 互相导入
- ❌ 跨模块导入非 `common/` 内容
- ❌ 循环依赖

### 导出

- ❌ 模块内分散导出枚举/常量
- ❌ 模块内分散导出工具函数
- ❌ 使用 `index.ts` 文件（直接导入具体文件）

### 代码

- ❌ 硬编码 fallback 数据
- ❌ 组件内定义常量（应放 `enum.ts`）
- ❌ 模块内定义工具函数（应放 `helper.ts`）
- ❌ 模块内定义 `interface`（应放 `common/types.ts`）
- ❌ 使用 TypeScript `enum` 关键字（用 `const` + `type` 模式）
- ❌ 使用 `any` 类型
- ❌ 魔法字符串/数字
- ❌ 在 service 层 catch 异常后静默处理
- ❌ console.log 调试代码提交
- ❌ 注释掉的代码提交
- ❌ 重复代码超过 3 行
- ❌ 函数超过 50 行
- ❌ 文件超过 300 行
- ❌ 嵌套超过 3 层
- ❌ 直接修改 props 或 state
- ❌ 在组件内直接调用 fetch/axios（应通过 hooks/service）
- ❌ 中英文混合命名

### 注释

- ❌ 多行注释块
- ❌ 函数内部注释
- ❌ 解释 what 的注释（代码本身应自解释）
- ❌ 过时注释
- ❌ 注释掉的代码
