---
inclusion: fileMatch
fileMatchPattern: "**/SKILL.md"
---

# Claude Code Skill 规范

创建或编辑 SKILL.md 时必须遵循此规范。

## 结构

```
skill-name/
├── SKILL.md (必需)
└── references/ (可选，详细文档)
```

## SKILL.md 格式

### Frontmatter (必需)

```yaml
---
name: skill-name
description: 描述 skill 功能 + 触发条件。Use when (1) ..., (2) ..., (3) ...
---
```

- `name`: skill 名称
- `description`: 必须包含功能描述和触发条件（when to use）

### Body (必需)

给 Claude 的指令，要求：

- 简洁，避免冗余解释
- 使用祈使句
- 引用 references/ 中的详细文档

## 核心原则

### 简洁优先

Context window 是公共资源。只添加 Claude 不知道的信息。

### 渐进式披露

1. Metadata (name + description) - 始终加载 (~100 words)
2. SKILL.md body - 触发后加载 (<5k words)
3. references/ - 按需加载

### SKILL.md 保持精简

- 控制在 500 行以内
- 详细内容放 references/
- 引用时说明何时读取

## 禁止

- 创建 README.md、CHANGELOG.md 等多余文件
- 在 body 中写 "When to Use"（应放 description）
- 冗长解释（Claude 已经很聪明）
- 重复信息（SKILL.md 和 references 不要重复）

## references/ 使用

```markdown
**For detailed guide:** See `references/xxx.md`
```

文件超过 100 行时，顶部加目录。
