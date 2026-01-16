---
inclusion: fileMatch
fileMatchPattern: "**/backend/**"
---

# 后端编码规范

## 导入规则

- `common/` → 无依赖，可被任何层导入
- `modules/*/dto.py` → 只导入 `pydantic`
- `modules/*/service.py` → 导入 `common/`
- `modules/*/router.py` → 导入 `common/`, 同模块 `dto`, `service`

## 导出规则

- `common/enum.py` → 枚举和常量
- `common/helper.py` → 工具函数
- `common/errors.py` → 错误类型
- `common/response.py` → 统一响应格式
- 直接从具体文件导入，禁止 `__init__.py` 集中导出

## 代码规范

- FastAPI + Pydantic
- uv 管理依赖
- 函数/变量 snake_case，类名 PascalCase
- Python 3.10+ 类型注解（`list[str]` 非 `List[str]`）
- 分页用 `paginate()`，响应用 `success_response()`
- 错误抛出 `AppError`

## 分层职责

- **router**: 路由定义，调用 service，禁止业务逻辑
- **service**: 业务逻辑，禁止返回 HTTP 响应
- **dto**: 数据结构定义，禁止业务逻辑

## 禁止

- 硬编码配置值（放 `common/config.py`）
- 使用 pip/conda（必须用 uv）
- service 层静默 catch 异常
- print 调试代码提交
- 函数超过 50 行 / 文件超过 500 行
- 直接返回数据库原始数据
- 魔法数字硬编码
