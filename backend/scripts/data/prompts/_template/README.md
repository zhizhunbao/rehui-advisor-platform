# Prompt 模板使用指南

这是创建新 Prompt 的标准模板。

## 目录结构

```
category-name/
├── PROMPT.md       # Prompt 指令（核心）
├── metadata.json   # 元数据（分类、标签、变量）
└── README.md       # 说明文档（可选）
```

## PROMPT.md 格式

```markdown
---
name: prompt_name
description: 简短描述
---

I want you to act as a [角色]. I will provide you with [输入内容], and you will:

1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

## Constraints

- Only output [输出内容], no explanations
- If uncertain, [处理方式]
- Format: [格式要求]

## Example

Input: [示例输入]
Output: [示例输出]

## Variables

- {{variable_1}}: [变量说明]
- {{variable_2}}: [变量说明]
```

## metadata.json 格式

```json
{
  "name": "prompt_name",
  "description": "简短描述",
  "category": "text_processing|analysis|generation|format_conversion",
  "tags": ["tag1", "tag2"],
  "variables": [
    {
      "name": "variable_name",
      "type": "string",
      "required": true,
      "default": null,
      "description": "变量说明"
    }
  ],
  "is_public": true,
  "source": "custom",
  "created_at": "2026-01-15T00:00:00"
}
```

## 分类说明

### text_processing（文本处理）

- translate - 翻译
- proofread - 校对
- simplify - 简化
- summarize - 总结
- expand - 扩写

### analysis（分析）

- extract_key_points - 提取要点
- compare_options - 对比选项
- pros_cons - 优缺点分析
- sentiment_analysis - 情感分析
- plagiarism_check - 原创性检查

### generation（生成）

- generate_email - 生成邮件
- generate_checklist - 生成清单
- generate_questions - 生成问题
- generate_template - 生成模板

### format_conversion（格式转换）

- json_to_table - JSON 转表格
- extract_structured_data - 提取结构化数据
- markdown_to_plain - Markdown 转纯文本

## 命名规范

- 目录名：`category-name`（如 `text_processing-translate`）
- Prompt 名：`name`（如 `translate`）
- 使用 `-` 连接 category 和 name
- name 内部用 `_` 连接单词

## 创建步骤

1. 复制 `_template` 目录
2. 重命名为 `category-name`
3. 修改 `PROMPT.md` 的指令内容
4. 修改 `metadata.json` 的元数据
5. 测试 prompt 是否有效

## 最佳实践

1. **清晰的角色定义**：明确 AI 扮演什么角色
2. **结构化步骤**：列出清晰的执行步骤
3. **明确约束**：说明输出格式和限制
4. **提供示例**：给出输入输出示例
5. **变量标记**：用 `{{variable}}` 标记可替换部分
