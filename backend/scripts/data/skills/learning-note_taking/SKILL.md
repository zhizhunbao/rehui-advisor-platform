---
name: learning-note_taking
description: Course note-taking and organization assistant. Use when (1) user needs to add notes to lecture materials, (2) organizing study notes from PDFs/slides, (3) creating bilingual study guides, (4) structuring learning content with examples and explanations.
---

# Learning Note-Taking Assistant

## Objectives

- Add comprehensive notes to extracted lecture materials
- Organize content with clear structure and examples
- Create bilingual (中英文) explanations for technical concepts
- Generate code examples and practical demonstrations
- Build study-friendly documentation

## Core Workflow

### 1. Analyze Existing Content

Before adding notes:

1. Read the entire document to understand scope
2. Identify key concepts, definitions, and examples
3. Note areas needing clarification or expansion
4. Check for existing note placeholders

### 2. Note-Taking Structure

**For each page/section:**

````markdown
## Page N

### [Original Content Title]

[Original extracted text...]

**📝 Notes / 笔记:**

**[Concept Name in Chinese]:**

- **定义/Definition:** Clear explanation
- **关键点/Key Points:** Bullet list of important aspects
- **示例/Example:** Practical code or real-world example
- **注意事项/Notes:** Common pitfalls or important considerations

**代码示例/Code Example:**

\```python

# Practical implementation

# With detailed comments

\```

**应用场景/Use Cases:**

- Scenario 1: When to use this
- Scenario 2: Common application
````

### 3. Content Enhancement Patterns

**Pattern A: Technical Concepts**

````markdown
**正则表达式 / Regular Expressions:**

**定义:** 用于匹配文本模式的形式化语言

**核心元字符:**

- `.` - 匹配任意单个字符
- `*` - 0次或多次
- `+` - 1次或多次

**代码示例:**
\```python
import re
text = "Email: user@example.com"
emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
\```

**应用:** 数据验证、文本清洗、信息提取
````

**Pattern B: Algorithms/Methods**

```markdown
**词干提取 / Stemming:**

**工作原理:**

1. 识别词缀模式
2. 应用规则移除词缀
3. 返回词干（可能不是真实单词）

**对比:**
| 原词 | Stemming | Lemmatization |
|------|----------|---------------|
| running | run | run |
| studies | studi | study |

**何时使用:**

- ✅ 信息检索（速度重要）
- ✅ 大规模文本处理
- ❌ 需要人类可读的结果
```

**Pattern C: Practical Examples**

````markdown
**实际应用示例:**

\```python

# 场景：清洗社交媒体文本

def clean_tweet(text): # 1. 移除URL
text = re.sub(r'http\S+', '', text) # 2. 移除@用户名
text = re.sub(r'@\w+', '', text) # 3. 转小写
text = text.lower()
return text

tweet = "Check this out! @john https://example.com"
clean = clean_tweet(tweet)

# 输出: "check this out!"

\```
````

### 4. Bilingual Best Practices

**Technical terms:**

- First mention: "主成分分析 (Principal Component Analysis, PCA)"
- Subsequent: "PCA" or "主成分分析"
- Keep English in parentheses for clarity

**Code comments:**

- Keep code in English
- Add Chinese explanations above code blocks
- Translate variable names in comments if helpful

**Formulas:**

- Keep mathematical notation in English
- Translate descriptions: "均值 (mean) = μ"

## Key Instructions

### 1. Content Organization

**Hierarchical structure:**

```
# Lecture Title
  ## Page N
    ### Section Title
      **📝 Notes / 笔记:**
        **Concept Name:**
          - Definition
          - Examples
          - Code
```

**Visual markers:**

- 📝 Notes section
- ✅ Correct usage
- ❌ Common mistakes
- ⚠️ Important warnings
- 💡 Tips and tricks

### 2. Code Examples

**Requirements:**

- Must be runnable and tested
- Include imports and setup
- Add output as comments
- Explain each step

**Template:**

```python
# 导入必要的库
import library

# 准备数据
data = "example"

# 执行操作
result = process(data)

# 输出结果
print(result)  # Expected output: ...
```

### 3. Comparison Tables

Use tables to compare concepts:

```markdown
| 特性     | Method A | Method B |
| -------- | -------- | -------- |
| 速度     | 快       | 慢       |
| 准确性   | 低       | 高       |
| 使用场景 | 大规模   | 精确分析 |
```

### 4. Progressive Complexity

Start simple, then add complexity:

1. **Basic concept** - Simple definition
2. **Example** - Minimal working example
3. **Advanced** - Edge cases and optimizations
4. **Practice** - Suggested exercises

## Validation

Before completing notes:

- [ ] All key concepts explained in both languages
- [ ] Code examples are tested and working
- [ ] Tables and lists are properly formatted
- [ ] Technical terms are consistent
- [ ] No placeholder text remains
- [ ] Structure is clear and navigable

## Common Patterns

### Pattern 1: Lecture Slides → Study Notes

```
1. Read extracted markdown
2. Identify main concepts per page
3. Add detailed explanations
4. Create code examples
5. Add comparison tables
6. Include practice suggestions
```

### Pattern 2: Technical Paper → Summary Notes

```
1. Extract key algorithms/methods
2. Explain in simple terms
3. Provide implementation examples
4. Compare with alternatives
5. Note practical applications
```

### Pattern 3: Quick Reference Creation

```
1. List all concepts covered
2. Create cheat sheet format
3. Add minimal but complete examples
4. Include common pitfalls
5. Link to detailed sections
```

## File Organization

**Recommended structure:**

```
course/
├── slides/
│   └── lecture1.pdf
├── notes/
│   ├── lecture1_notes.md      # With comprehensive notes
│   └── lecture1_notes_images/ # Extracted images
└── code/
    └── lecture1_examples.py   # Runnable examples
```

## Example Usage

**User request:** "来个笔记 skill" or "帮我整理这个lecture的笔记"

**Your workflow:**

1. Read the current lecture notes file
2. Identify sections needing notes (look for `> [Add your notes here]`)
3. For each section:
   - Add bilingual concept explanation
   - Create practical code examples
   - Add comparison tables if applicable
   - Include use cases and tips
4. Ensure all code is tested and runnable
5. Validate formatting and completeness

## Quick Reference

**Essential elements for each concept:**

1. **中文标题** - Clear Chinese heading
2. **定义** - Concise definition
3. **示例** - At least one example
4. **代码** - Runnable code (if applicable)
5. **应用** - Practical use cases

**Formatting shortcuts:**

- Bold for emphasis: `**重点**`
- Code inline: `` `code` ``
- Code block: ` ```python ... ``` `
- Lists: `- Item` or `1. Item`
- Tables: `| Col1 | Col2 |`
