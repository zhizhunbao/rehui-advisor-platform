# PCA 课堂示例 | PCA In-Class Example

**PCA = Principal Component Analysis | 主成分分析**

**来源:** `PCA_ExampleInClass.pdf`

---

## 符号表 | Symbol Table

| 符号 Symbol | 读音 Pronunciation | 含义 Meaning                     | 用途 Usage             | 为什么需要 Why                                                                                       |
| ----------- | ------------------ | -------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| μ           | mu                 | 均值 Mean                        | Step 1: 减去均值       | 中心化数据,让数据围绕原点分布 \| Center data around origin                                           |
| σ           | sigma              | 标准差 Std Dev                   | Step 1: 除以标准差     | 统一尺度,避免大数值特征主导 \| Equalize scales, prevent large-value features from dominating         |
| σ²          | sigma squared      | 方差 Variance                    | 衡量信息量             | 方差大=信息多=重要 \| Large variance = more information = important                                  |
| Σ           | sigma (capital)    | 求和 Summation                   | 把所有数加起来         | 计算统计量的基础操作 \| Basic operation for calculating statistics                                   |
| λ           | lambda             | 特征值 Eigenvalue                | Step 3: 表示方差大小   | 决定主成分重要性,选择保留哪些 \| Determine PC importance, decide which to keep                       |
| C           | -                  | 协方差矩阵 Cov Matrix            | Step 2: 特征之间的关系 | 包含所有方差和相关性信息 \| Contains all variance and correlation information                        |
| v, e        | -                  | 向量/特征向量 Vector/Eigenvector | Step 4-5: 主成分的方向 | 定义新坐标系的轴,数据变化最大的方向 \| Define new coordinate axes, directions of max variation       |
| ᵀ           | T                  | 转置 Transpose                   | 把行列互换             | 矩阵运算需要,调整维度匹配 \| Required for matrix operations, adjust dimension matching               |
| ·           | dot                | 点积 Dot product                 | Step 6: 计算投影       | 计算数据在新轴上的坐标 \| Calculate data coordinates on new axes                                     |
| \|\|v\|\|   | -                  | 向量长度 Vector length           | Step 5: 归一化用       | 让特征向量长度为1,投影值才有意义 \| Make eigenvector length = 1, so projection values are meaningful |
| PC          | -                  | 主成分 Principal Component       | 降维后的新特征         | 用更少维度表示数据,保留最多信息 \| Represent data with fewer dimensions, retain maximum information  |

---

## 基础知识 | Prerequisites

### 统计基础 | Statistics Basics

**均值 Mean (μ):**

```
μ = Σx / n
```

数据的中心位置 | Center of data

**方差 Variance (σ²):**

```
σ² = Σ(x - μ)² / n
```

数据的分散程度 | Spread of data

**标准差 Standard Deviation (σ):**

```
σ = √(σ²)
```

方差的平方根,与数据同单位 | Square root of variance, same unit as data

**协方差 Covariance:**

```
Cov(X,Y) = Σ(Xi - μx)(Yi - μy) / (n-1)
```

两个变量的关系 | Relationship between two variables

- 正值:同向变化 | Positive: vary together
- 负值:反向变化 | Negative: vary oppositely
- 零:无线性关系 | Zero: no linear relationship

**协方差矩阵 Covariance Matrix:**

```
C = [Var(X)    Cov(X,Y)]
    [Cov(Y,X)  Var(Y)  ]
```

描述所有变量之间的关系 | Describes relationships between all variables

### 线性代数基础 | Linear Algebra Basics

**向量 Vector:**

```
v = [v₁, v₂]ᵀ
```

有方向和大小的量 | Quantity with direction and magnitude

**向量长度 Vector Length:**

```
||v|| = √(v₁² + v₂²)
```

**单位向量 Unit Vector:**

```
长度为1的向量 | Vector with length = 1
v̂ = v / ||v||
```

**点积 Dot Product:**

```
v · w = v₁w₁ + v₂w₂
```

投影的数学表示 | Mathematical representation of projection

**特征值 Eigenvalue (λ):**

```
Cv = λv
```

矩阵C在方向v上的"拉伸倍数" | "Stretching factor" of matrix C in direction v

**特征向量 Eigenvector (v):**

```
Cv = λv
```

矩阵C的"特殊方向",只被拉伸不改变方向 | "Special direction" of matrix C, only stretched not rotated

### 几何直观 | Geometric Intuition

**坐标系旋转:**

```
原坐标系: (x, y)
新坐标系: (PC1, PC2)
```

PCA = 找到最佳的新坐标系 | PCA = find the best new coordinate system

**投影 Projection:**

```
数据点在新轴上的坐标 = 数据点 · 新轴方向
```

把高维数据"压"到低维空间 | "Compress" high-D data to low-D space

**方差最大化:**

```
沿PC1方向,数据最分散(方差最大)
沿PC2方向,数据次分散(方差次大)
```

Along PC1, data is most spread (max variance)
Along PC2, data is second most spread (2nd max variance)

---

## 研究背景 | Research Background

**发明者:** Karl Pearson (1901)

**研究问题:** 生物测量学 - 分析生物体的多个测量数据(身高、体重、头围等),找出主要变化模式。

Biometrics - analyze multiple biological measurements (height, weight, head size, etc.), find main variation patterns.

**之前的方法及问题:**

- 逐个分析 → 看不到整体 | Analyze one by one → miss overall pattern
- 相关性分析 → 只能看两两关系 | Correlation → only pairwise relationships
- 简单平均 → 丢失方向信息 | Simple average → lose directional information

**Pearson的创新:**
用线性代数找"最大方差方向" = 主成分 = 最能体现差异的综合指标。

Use linear algebra to find "max variance direction" = principal component = best indicator of variation.

**例子:** 10个身体测量 → 2-3个主成分就能概括主要特征。

Example: 10 body measurements → 2-3 principal components capture main features.

---

## 基础知识 | Prerequisites

### 统计基础 | Statistics Basics

**均值 Mean (μ):**

```
μ = Σx / n
```

数据的中心位置 | Center of data

**方差 Variance (σ²):**

```
σ² = Σ(x - μ)² / n
```

数据的分散程度 | Spread of data

**标准差 Standard Deviation (σ):**

```
σ = √(σ²)
```

方差的平方根,与数据同单位 | Square root of variance, same unit as data

**协方差 Covariance:**

```
Cov(X,Y) = Σ(Xi - μx)(Yi - μy) / (n-1)
```

两个变量的关系 | Relationship between two variables

- 正值:同向变化 | Positive: vary together
- 负值:反向变化 | Negative: vary oppositely
- 零:无线性关系 | Zero: no linear relationship

**协方差矩阵 Covariance Matrix:**

```
C = [Var(X)    Cov(X,Y)]
    [Cov(Y,X)  Var(Y)  ]
```

描述所有变量之间的关系 | Describes relationships between all variables

### 线性代数基础 | Linear Algebra Basics

**向量 Vector:**

```
v = [v₁, v₂]ᵀ
```

有方向和大小的量 | Quantity with direction and magnitude

**向量长度 Vector Length:**

```
||v|| = √(v₁² + v₂²)
```

**单位向量 Unit Vector:**

```
长度为1的向量 | Vector with length = 1
v̂ = v / ||v||
```

**点积 Dot Product:**

```
v · w = v₁w₁ + v₂w₂
```

投影的数学表示 | Mathematical representation of projection

**特征值 Eigenvalue (λ):**

```
Cv = λv
```

矩阵C在方向v上的"拉伸倍数" | "Stretching factor" of matrix C in direction v

**特征向量 Eigenvector (v):**

```
Cv = λv
```

矩阵C的"特殊方向",只被拉伸不改变方向 | "Special direction" of matrix C, only stretched not rotated

### 几何直观 | Geometric Intuition

**坐标系旋转:**

```
原坐标系: (x, y)
新坐标系: (PC1, PC2)
```

PCA = 找到最佳的新坐标系 | PCA = find the best new coordinate system

**投影 Projection:**

```
数据点在新轴上的坐标 = 数据点 · 新轴方向
```

把高维数据"压"到低维空间 | "Compress" high-D data to low-D space

**方差最大化:**

```
沿PC1方向,数据最分散(方差最大)
沿PC2方向,数据次分散(方差次大)
```

Along PC1, data is most spread (max variance)
Along PC2, data is second most spread (2nd max variance)

---

## 核心目标 | Core Goal

**降维:用更少的特征表示数据,同时保留最多信息。**

**Dimensionality reduction: represent data with fewer features while retaining maximum information.**

---

## Q&A

**Q1: 为什么需要降维? | Why reduce dimensions?**

高维问题:难可视化、计算慢、易过拟合。

High-D problems: hard to visualize, slow computation, overfitting.

**Q2: 能直接删掉一些特征吗? | Can we just drop some features?**

不行,会丢失重要信息。

No, will lose important information.

**Q3: 那怎么办? | Then what?**

找"最重要"的方向,用新方向代替原始特征。

Find "most important" directions, replace original features with new directions.

**Q4: 什么是"最重要"的方向? | What is "most important"?**

数据变化最大的方向 = 方差最大的方向 = 信息最多。

Direction of maximum variance = most information.

**Q5: 怎么找这个方向? | How to find it?**

线性代数:协方差矩阵的特征向量。

Linear algebra: eigenvectors of covariance matrix.

**Q6: 为什么先要标准化? | Why standardize first?**

特征尺度不同,大数值会主导。标准化让特征平等。

Different scales, large values dominate. Standardization equalizes features.

**Q7: 找到方向后怎么用? | How to use the directions?**

投影:数据 × 特征向量 = 新坐标(降维后的数据)。

Projection: data × eigenvectors = new coordinates (reduced data).

**Q8: 这就是PCA? | This is PCA?**

是的。Principal Component Analysis = 分析主要成分(方差最大的方向)。

Yes. Principal Component Analysis = analyze principal components (max variance directions).

---

## 基础知识 | Prerequisites

### 统计基础 | Statistics Basics

**均值 Mean (μ):**

```
μ = Σx / n
```

数据的中心位置 | Center of data

**方差 Variance (σ²):**

```
σ² = Σ(x - μ)² / n
```

数据的分散程度 | Spread of data

**标准差 Standard Deviation (σ):**

```
σ = √(σ²)
```

方差的平方根,与数据同单位 | Square root of variance, same unit as data

**协方差 Covariance:**

```
Cov(X,Y) = Σ(Xi - μx)(Yi - μy) / (n-1)
```

两个变量的关系 | Relationship between two variables

- 正值:同向变化 | Positive: vary together
- 负值:反向变化 | Negative: vary oppositely
- 零:无线性关系 | Zero: no linear relationship

**协方差矩阵 Covariance Matrix:**

```
C = [Var(X)    Cov(X,Y)]
    [Cov(Y,X)  Var(Y)  ]
```

描述所有变量之间的关系 | Describes relationships between all variables

### 线性代数基础 | Linear Algebra Basics

**向量 Vector:**

```
v = [v₁, v₂]ᵀ
```

有方向和大小的量 | Quantity with direction and magnitude

**向量长度 Vector Length:**

```
||v|| = √(v₁² + v₂²)
```

**单位向量 Unit Vector:**

```
长度为1的向量 | Vector with length = 1
v̂ = v / ||v||
```

**点积 Dot Product:**

```
v · w = v₁w₁ + v₂w₂
```

投影的数学表示 | Mathematical representation of projection

**特征值 Eigenvalue (λ):**

```
Cv = λv
```

矩阵C在方向v上的"拉伸倍数" | "Stretching factor" of matrix C in direction v

**特征向量 Eigenvector (v):**

```
Cv = λv
```

矩阵C的"特殊方向",只被拉伸不改变方向 | "Special direction" of matrix C, only stretched not rotated

### 几何直观 | Geometric Intuition

**坐标系旋转:**

```
原坐标系: (x, y)
新坐标系: (PC1, PC2)
```

PCA = 找到最佳的新坐标系 | PCA = find the best new coordinate system

**投影 Projection:**

```
数据点在新轴上的坐标 = 数据点 · 新轴方向
```

把高维数据"压"到低维空间 | "Compress" high-D data to low-D space

**方差最大化:**

```
沿PC1方向,数据最分散(方差最大)
沿PC2方向,数据次分散(方差次大)
```

Along PC1, data is most spread (max variance)
Along PC2, data is second most spread (2nd max variance)

---

## 步骤概览 | Steps Overview

1. **标准化数据** | Standardize data
2. **计算协方差矩阵 C** | Calculate covariance matrix C
3. **求特征值 λ** | Find eigenvalues λ using |C - λI| = 0
4. **求特征向量** | Find eigenvectors for each λ
5. **归一化特征向量** | Normalize eigenvectors
6. **投影数据** | Project data onto principal components

---

## 给定数据 | Given Data

| Length | Width |
| ------ | ----- |
| 4      | 11    |
| 8      | 4     |
| 13     | 5     |
| 7      | 14    |

**统计量 | Statistics:**

- 平均值 | Average: Length = 8, Width = 8.5
- 标准差 | SD (Sample): Length = 3.74, Width = 4.80

---

## Step 1: 标准化数据 | Standardize Data

**为什么需要这一步? | Why this step?**

PCA对特征的尺度敏感。如果不标准化,数值大的特征会主导分析结果。标准化使所有特征在同一量级上,确保每个特征对PCA的贡献是基于其变化模式而非数值大小。

PCA is sensitive to feature scales. Without standardization, features with larger values would dominate the analysis. Standardization puts all features on the same scale, ensuring each feature's contribution to PCA is based on its variation pattern, not its magnitude.

**公式 | Formula:**

```
z = (x - μ) / σ
```

**原始数据 → 标准化数据 | Original → Standardized:**

| Length | Width | →   | Length | Width |
| ------ | ----- | --- | ------ | ----- |
| 4      | 11    | →   | -1.07  | 0.52  |
| 8      | 4     | →   | 0.00   | -0.94 |
| 13     | 5     | →   | 1.34   | -0.73 |
| 7      | 14    | →   | -0.27  | 1.15  |

**计算示例 | Example:**

```
第一个值: (4 - 8) / 3.74 = -1.07
First value: (4 - 8) / 3.74 = -1.07
```

---

## Step 2: 计算协方差矩阵 | Calculate Covariance Matrix

**为什么需要这一步? | Why this step?**

协方差矩阵描述了特征之间的关系和各自的方差。它是PCA的核心,因为主成分就是从这个矩阵中提取出来的。协方差矩阵告诉我们数据在哪些方向上变化最大,以及特征之间如何相互关联。

The covariance matrix describes relationships between features and their variances. It's the core of PCA because principal components are extracted from this matrix. It tells us in which directions data varies most and how features correlate with each other.

**公式 | Formula:**

```
Cov(X,Y) = Σ(Xi × Yi) / (n-1)
```

由于数据已标准化,均值为0,公式简化为上式。
Since data is standardized (mean = 0), formula simplifies.

**计算过程 | Calculation:**

| Length       | Width | Length × Width |
| ------------ | ----- | -------------- |
| -1.07        | 0.52  | -0.56          |
| 0.00         | -0.94 | 0.00           |
| 1.34         | -0.73 | -0.98          |
| -0.27        | 1.15  | -0.31          |
| **总和 Sum** |       | **-1.84**      |

```
Cov(Length, Width) = -1.84 / (4-1) = -0.61
```

**协方差矩阵 | Covariance Matrix:**

|        | Length | Width |
| ------ | ------ | ----- |
| Length | 1.00   | -0.61 |
| Width  | -0.61  | 1.00  |

**解读 | Interpretation:**

- 对角线为1.00(标准化数据的方差)
- -0.61表示负相关:Length增加时Width减少
- Diagonal = 1.00 (variance of standardized data)
- -0.61 indicates negative correlation

---

## Step 3: 求特征值 | Find Eigenvalues

**为什么需要这一步? | Why this step?**

特征值表示数据在对应主成分方向上的方差大小。特征值越大,说明数据在该方向上的变化越大,该方向越重要。通过特征值,我们可以判断应该保留哪些主成分,以及每个主成分能解释多少方差。

Eigenvalues represent the variance of data along corresponding principal component directions. Larger eigenvalues indicate greater variation in that direction, making it more important. Through eigenvalues, we can determine which principal components to keep and how much variance each explains.

**特征方程 | Characteristic Equation:**

```
|C - λI| = 0

|1-λ    -0.61|
|-0.61  1-λ  | = 0
```

**展开 | Expand:**

```
(1-λ)(1-λ) - (-0.61)(-0.61) = 0
(1-λ)² - 0.61² = 0
(1-λ+0.61)(1-λ-0.61) = 0
```

**解 | Solution:**

```
λ₁ = 1.61
λ₂ = 0.39
```

**意义 | Meaning:**

- λ₁ = 1.61 是最大特征值,对应第一主成分
- λ₂ = 0.39 是第二特征值,对应第二主成分
- λ₁ + λ₂ = 2.00 = 总方差
- λ₁ = 1.61 is the largest eigenvalue → PC1
- λ₂ = 0.39 is the second eigenvalue → PC2
- Sum = 2.00 = total variance

**方差解释比例 | Variance Explained:**

- PC1: 1.61/2.00 = **80.5%**
- PC2: 0.39/2.00 = **19.5%**

---

## Step 4: 求特征向量 | Find Eigenvectors

**为什么需要这一步? | Why this step?**

特征向量定义了主成分的方向。每个特征向量指向数据变化的一个方向,对应的特征值表示该方向上的方差大小。特征向量本质上是新坐标系的轴,我们将用它们来转换原始数据。

Eigenvectors define the directions of principal components. Each eigenvector points to a direction of data variation, with its eigenvalue indicating the variance in that direction. Eigenvectors essentially form the axes of a new coordinate system used to transform the original data.

**对于 λ₁ = 1.61 | For λ₁ = 1.61:**

```
(C - λ₁I)u₁ = 0

|1-1.61  -0.61| |u₁|   |0|
|-0.61   1-1.61| |u₂| = |0|

|-0.61  -0.61| |u₁|   |0|
|-0.61  -0.61| |u₂| = |0|
```

**第一个方程 | First equation:**

```
-0.61u₁ - 0.61u₂ = 0
u₁ = -u₂
```

**设 t=1 | Let t=1:**

```
u₁ = 0.61
u₂ = -0.61
```

**特征向量 | Eigenvector:**

```
e₁ = [0.61, -0.61]ᵀ
```

---

## Step 5: 归一化特征向量 | Normalize Eigenvectors

**为什么需要这一步? | Why this step?**

归一化使特征向量的长度为1,这样在投影数据时,投影值直接反映数据在该方向上的坐标,而不受向量长度影响。归一化后的特征向量也更容易解释和比较,且保证了数学运算的一致性。

Normalization makes eigenvectors unit length (length = 1), so when projecting data, the projection values directly reflect coordinates in that direction without being affected by vector length. Normalized eigenvectors are also easier to interpret and compare, ensuring mathematical consistency.

**计算长度 | Calculate length:**

```
||e₁|| = √(0.61² + (-0.61)²)
      = √(0.3721 + 0.3721)
      = √0.7442
      = 0.8627
```

**归一化 | Normalize:**

```
e₁_normalized = [0.61/0.8627, -0.61/0.8627]ᵀ
              = [0.7071, -0.7071]ᵀ
```

**同理 | Similarly:**

```
e₂_normalized = [0.7071, 0.7071]ᵀ
```

**验证 | Verification:**

- 长度为1 | Length = 1: √(0.7071² + 0.7071²) = 1.0
- 相互垂直 | Orthogonal: e₁ · e₂ = 0

---

## Step 6: 投影到主成分 | Project onto Principal Components

**为什么需要这一步? | Why this step?**

投影是降维的实际操作。通过将原始数据投影到主成分方向上,我们得到了降维后的新数据表示。这一步将高维数据转换到低维空间,同时保留了最重要的信息(最大方差方向)。投影后的值就是数据在新坐标系中的坐标。

Projection is the actual dimensionality reduction operation. By projecting original data onto principal component directions, we obtain a new lower-dimensional representation. This step transforms high-dimensional data into a lower-dimensional space while preserving the most important information (directions of maximum variance). The projected values are the coordinates in the new coordinate system.

**投影公式 | Projection Formula:**

```
PC = eᵀ × X
```

**计算 | Calculation:**

```
P₁₁ = [0.7071, -0.7071] × [-1.07, 0.52]ᵀ
    = 0.7071×(-1.07) + (-0.7071)×0.52
    = -0.7566 - 0.3677
    = -1.1243

P₁₂ = [0.7071, -0.7071] × [0, -0.94]ᵀ
    = 0 + 0.6647
    = 0.6646

P₁₃ = [0.7071, -0.7071] × [1.34, -0.73]ᵀ
    = 1.4637

P₁₄ = [0.7071, -0.7071] × [-0.27, 1.15]ᵀ
    = -1.0
```

**结果 | Result:**

**标准化数据 | Standardized Data:**

| Length | Width |
| ------ | ----- |
| -1.07  | 0.52  |
| 0.00   | -0.94 |
| 1.34   | -0.73 |
| -0.27  | 1.15  |

**投影到PC1 | Projected onto PC1:**

| PC1     |
| ------- |
| -1.1243 |
| 0.6646  |
| 1.4637  |
| -1.0    |
