# Hybrid Activity 1: Q-Learning Implementation

基于文章 [Math of Q-Learning — Python](https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6) 的代码实现。

这是 **Hybrid Activity 1** 的源代码，用于 Lab 2 的基础。

## 环境说明

- **10x10 网格世界**
- 智能体 (O) 从左上角 (0,0) 开始
- 宝藏 (T) 在右下角 (9,9)
- 4 个动作：left (0), right (1), up (2), down (3)
- 奖励：到达宝藏 +1，其他 0

## 文件结构

```
lab1/
├── medium_qlearning_env.py  # 环境实现（抽象基类 + GridEnv）
├── medium_qlearning_rl.py   # Q-Learning 训练算法
└── README.md                # 本文件
```

## 运行方式

```bash
cd aisd/courses/rl/code/lab1
python medium_qlearning_rl.py
```

## Lab 2 准备工作

根据 Lab 2 要求，你需要：

1. **复制并重命名文件：**
   - `medium_qlearning_rl.py` → `<your_algonquin_id>_lab2_qlearning_agent.py`
   - `medium_qlearning_env.py` → `<your_algonquin_id>_lab2_environment.py`

2. **修改 import 语句：**
   在 `<your_algonquin_id>_lab2_qlearning_agent.py` 中：

   ```python
   import <your_algonquin_id>_lab2_environment as env
   ```

3. **修改环境为 Cliff Walking：**
   - 改为 4×12 网格
   - 添加悬崖区域
   - 修改奖励机制（每步 -1，掉悬崖 -100）

## 核心算法

**贝尔曼方程（Bellman Equation）：**

```
Q(s,a) = r + γ * max Q(s',a')
```

其中：

- `Q(s,a)` - 在状态 s 采取动作 a 的价值
- `r` - 即时奖励
- `γ` - 折扣因子（gamma = 0.1）
- `max Q(s',a')` - 下一状态的最大 Q 值

## 超参数

- `epochs = 50` - 训练轮数
- `gamma = 0.1` - 折扣因子
- `epsilon = 0.08` - 探索率（初始值）
- `decay = 0.5` - epsilon 衰减率

## 预期结果

在第 40 轮左右，智能体应该学会使用最短路径（8 步）到达宝藏。

## 学习要点

1. **Q-table** - 维护一个 states × actions 的表格
2. **ε-greedy 策略** - 平衡探索与利用
3. **贝尔曼方程** - 更新 Q 值的核心公式
4. **epsilon 衰减** - 随着训练减少随机探索
