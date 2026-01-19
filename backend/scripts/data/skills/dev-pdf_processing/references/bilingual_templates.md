# Bilingual Documentation Templates

## Template 1: Side-by-Side Format

Best for: Concept explanations, definitions, short content

```markdown
# Title | 标题

## Section Name | 章节名称

**English:** Explanation in English...

**中文:** 中文解释...

### Key Terms | 关键术语

- **Term 1 (术语1):** Definition | 定义
- **Term 2 (术语2):** Definition | 定义
```

## Template 2: Separate Sections

Best for: Long documents, detailed explanations

```markdown
# Document Title

## English Version

### Section 1

Content in English...

### Section 2

More content...

---

## 中文版本

### 第一节

中文内容...

### 第二节

更多内容...
```

## Template 3: Inline Translation

Best for: Technical documents with mixed content

```markdown
# Principal Component Analysis (主成分分析)

## Overview | 概述

PCA is an unsupervised learning technique (PCA是一种无监督学习技术) that reduces dimensionality (降低维度) while preserving variance (同时保留方差).

## Key Concepts | 关键概念

### Eigenvalues (特征值)

Eigenvalues represent the variance along each principal component.
特征值表示沿每个主成分的方差。

### Eigenvectors (特征向量)

Eigenvectors define the direction of principal components.
特征向量定义主成分的方向。
```

## Template 4: Academic Paper Format

````markdown
# Paper Title

# 论文标题

**Authors:** [Names]
**作者:** [姓名]

## Abstract | 摘要

**EN:** English abstract...

**中文:** 中文摘要...

## 1. Introduction | 引言

### 1.1 Background | 背景

**EN:** Background information...

**中文:** 背景信息...

## 2. Methodology | 方法

### 2.1 Algorithm | 算法

```python
# Code remains in English
def pca_transform(X):
    # Implementation
    pass
```
````

**Explanation | 解释:**

- **EN:** The algorithm works by...
- **中文:** 该算法通过...工作

## References | 参考文献

[Same in both languages]

````

## Template 5: Course Notes Format

```markdown
# Lecture N: Topic Name
# 第N讲: 主题名称

**Date:** YYYY-MM-DD
**日期:** YYYY年MM月DD日

---

## Learning Objectives | 学习目标

1. Understand concept A | 理解概念A
2. Apply technique B | 应用技术B
3. Analyze problem C | 分析问题C

---

## Content | 内容

### Part 1: Introduction | 第一部分: 介绍

#### English

Detailed explanation in English...

#### 中文

详细的中文解释...

### Part 2: Examples | 第二部分: 示例

#### Example 1 | 示例1

**Problem | 问题:**
- EN: Given data...
- 中文: 给定数据...

**Solution | 解答:**
- EN: Step 1...
- 中文: 步骤1...

---

## Summary | 总结

### Key Takeaways | 关键要点

| English | 中文 |
|---------|------|
| Point 1 | 要点1 |
| Point 2 | 要点2 |

### Practice Questions | 练习题

1. **Q:** Question in English?
   **问:** 中文问题?

   **A:** Answer...
   **答:** 答案...
````

## Technical Term Glossary Template

```markdown
# Technical Glossary | 技术词汇表

## Machine Learning | 机器学习

| English                      | 中文       | Abbreviation | Notes                    |
| ---------------------------- | ---------- | ------------ | ------------------------ |
| Principal Component Analysis | 主成分分析 | PCA          | Dimensionality reduction |
| Eigenvalue                   | 特征值     | λ            | Variance measure         |
| Eigenvector                  | 特征向量   | e            | Direction vector         |
| Covariance Matrix            | 协方差矩阵 | C            | Relationship measure     |
| Standardization              | 标准化     | -            | Mean=0, Std=1            |

## Statistics | 统计学

| English            | 中文   | Symbol | Formula      |
| ------------------ | ------ | ------ | ------------ |
| Mean               | 平均值 | μ      | Σx/n         |
| Standard Deviation | 标准差 | σ      | √(Σ(x-μ)²/n) |
| Variance           | 方差   | σ²     | Σ(x-μ)²/n    |
```

## Formula Handling

```markdown
### Mathematical Formulas | 数学公式

**Standardization Formula | 标准化公式:**

$$z = \frac{x - \mu}{\sigma}$$

**Where | 其中:**

- $x$ = original value | 原始值
- $\mu$ = mean | 平均值
- $\sigma$ = standard deviation | 标准差
- $z$ = standardized value | 标准化值

**Explanation | 解释:**

- **EN:** This formula transforms data to have mean 0 and standard deviation 1.
- **中文:** 此公式将数据转换为均值为0、标准差为1的形式。
```

## Best Practices

### 1. Consistency

- Use the same translation for technical terms throughout
- Maintain parallel structure in both languages
- Keep formatting identical

### 2. Clarity

- Add English terms in parentheses after Chinese: "主成分分析 (PCA)"
- Use bold for emphasis in both languages
- Separate languages clearly with visual markers

### 3. Readability

- Don't over-translate: keep code, formulas, and citations in English
- Use tables for term comparisons
- Add section markers: `---` or `***`

### 4. Cultural Adaptation

- Adjust examples to be culturally relevant
- Use appropriate units (metric vs imperial)
- Consider different learning styles
