# Lab 1 学习笔记 - Q-Learning 基础

> **实验目标**: 理解 Q-Learning 算法并实现 Cliff Walking 问题
>
> **参考资料**: [Math of Q-Learning — Python](../resources/math_of_q_learning_python_bilingual.md)

---

## 📋 目录

- **[Part 1: 快速入门](#part-1-快速入门)** - 核心概念速览
- **[Part 2: 代码实现 ⭐](#part-2-代码实现-)** - **先看这里！实践优先**
  - 2.1 实验任务说明
  - 2.2 完整代码实现
  - 2.3 关键代码解释
  - 2.4 预期结果
- **[Part 3: 数学基础](#part-3-数学基础)** - 核心公式速查
  - 3.1 核心符号
  - 3.2 核心公式
- **[Part 4: 背景知识](#part-4-背景知识)** - 理论补充
- **[Part 5: 实验检查](#part-5-实验检查)** - 提交前确认

---

## Part 1: 快速入门

### 核心概念速览

| 概念              | 定义                       | Cliff Walking 对应         |
| ----------------- | -------------------------- | -------------------------- |
| **状态 (State)**  | 智能体在环境中的位置或情况 | 网格坐标 (x, y)            |
| **动作 (Action)** | 智能体可以采取的行为       | LEFT, RIGHT, UP, DOWN      |
| **奖励 (Reward)** | 环境对行为的即时反馈       | 每步 -1，掉悬崖 -100       |
| **策略 (Policy)** | 在每个状态选择什么动作     | "在起点就向上走，避开悬崖" |
| **Q 值**          | 在某状态做某动作的长期价值 | Q((3,0), UP) = -7.2        |
| **探索 vs 利用**  | 尝试新路 vs 走已知最优路   | 10% 随机走 vs 90% 走最优   |
| **折扣因子 γ**    | 未来奖励的重要性           | γ=0.9，未来打9折           |

**Q-Learning 核心思想**：

- 维护一张 Q-Table，记录每个状态-动作对的价值
- 使用贝尔曼方程更新：`Q(s,a) = r + γ·max Q(s',a')`
- 用 ε-greedy 策略平衡探索与利用

---

## Part 2: 代码实现 ⭐

> 🎯 **快速预览**：完成训练后，智能体将学会用 **13 步**到达目标的最优路径（向上1步 → 向右11步 → 向下1步），完全避开悬崖区域。

### 2.1 实验任务说明

#### 环境设置

**Cliff Walking 网格布局 (4×12)**:

```
. . . . . . . . . . . .
. . . . . . . . . . . .
. . . . . . . . . . . .
S X X X X X X X X X X G
```

- S: 起点 (3,0) - 左下角
- G: 目标 (3,11) - 右下角
- X: 悬崖 (3,1) 到 (3,10) - 底部中间
- .: 安全格子

**奖励规则**:

- 每步移动: -1
- 掉下悬崖: -100 (并返回起点)
- 到达目标: 0 (结束)

**动作空间**: 4 个动作

> ⚠️ **注意**：代码中的动作编号顺序为：0=LEFT, 1=RIGHT, 2=UP, 3=DOWN

- 0: LEFT (左)
- 1: RIGHT (右)
- 2: UP (上)
- 3: DOWN (下)

---

### 2.2 完整代码实现

> **实际代码文件**：
>
> - 环境：`041107730_lab2_cliff_env.py`
> - 训练：`041107730_lab2_qlearning_agent.py`

#### 2.2.1 环境类 (Cliff Walking Environment)

**文件**: `041107730_lab2_cliff_env.py`

```python
"""
Cliff Walking Environment - Modified from Medium Article
4×12 grid world with cliff from (3,1) to (3,10)
"""
import abc


class Env(abc.ABC):
    """Abstract base class for environments"""
    @abc.abstractmethod
    def actions(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def states(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def step(self, action: int) -> tuple[int, int, bool]:
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self) -> tuple[int, int, bool]:
        raise NotImplementedError()

    @abc.abstractmethod
    def render(self):
        raise NotImplementedError()


class GridEnv(Env):
    """
    Cliff Walking Environment (4×12 grid)
    - Start: (3, 0) bottom-left
    - Goal: (3, 11) bottom-right
    - Cliff: (3, 1) to (3, 10)
    - Rewards: -1 per step, -100 for falling off cliff
    """
    def __init__(self, size: int):
        # Modified: 4×12 grid for Cliff Walking
        self.rows = 4
        self.cols = 12
        self.x = 0
        self.y = 3  # Start at bottom-left
        self.end_x = 11
        self.end_y = 3
        self.done = False
        self.cliff = False  # Added: track if agent fell off cliff

    def actions(self) -> int:
        return 4  # LEFT, RIGHT, UP, DOWN

    def states(self) -> int:
        return self.rows * self.cols  # 4 × 12 = 48 states

    def step(self, action: int) -> tuple[int, int, bool]:
        """
        Execute action and return (next_state, reward, done)
        Actions: 0=LEFT, 1=RIGHT, 2=UP, 3=DOWN
        """
        # Move agent
        if action == 0:  # LEFT
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:  # RIGHT
            self.x = self.x + 1 if self.x < self.cols - 1 else self.x
        if action == 2:  # UP
            self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3:  # DOWN
            self.y = self.y + 1 if self.y < self.rows - 1 else self.y

        # Modified: Check if fell off cliff
        if self.y == 3 and 1 <= self.x <= 10:
            reward = -100
            self.cliff = True
            # Reset to start position
            self.x = 0
            self.y = 3
            done = False  # Episode continues after falling
        else:
            reward = -1
            self.cliff = False
            # Check if reached goal
            done = self.x == self.end_x and self.y == self.end_y

        next_state = self.cols * self.y + self.x
        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        """Reset environment to start position"""
        self.x = 0
        self.y = 3
        self.done = False
        self.cliff = False
        return self.cols * self.y + self.x, 0, False

    def render(self):
        """
        Modified: Render grid with cliff marked as 'X'
        S = Start, G = Goal, X = Cliff, O = Agent
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.y == i and self.x == j:
                    print("O", end='')  # Agent position
                elif self.end_y == i and self.end_x == j:
                    print("G", end='')  # Goal
                elif i == 3 and 1 <= j <= 10:
                    print("X", end='')  # Cliff
                elif i == 3 and j == 0:
                    print("S", end='')  # Start
                else:
                    print(".", end='')
            print("")
```

---

#### 2.2.2 Q-Learning 训练算法

**文件**: `041107730_lab2_qlearning_agent.py`

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730

Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""

import os
import time
import random
import importlib

# Import the cliff walking environment module
env_module = importlib.import_module('041107730_lab2_cliff_env')


def train(env: env_module.Env, episodes: int = 50, gamma: float = 0.9,
          epsilon: float = 0.1, decay: float = 0.5, alpha: float = 1.0) -> list[list[float]]:
    """
    Train Q-Learning agent

    Args:
        episodes: Number of training episodes (default: 50)
        gamma: Discount factor
        epsilon: Initial exploration rate
        decay: Epsilon decay rate
        alpha: Step-size hyperparameter (for discussion only, not used in this implementation)

    Note:
        alpha=1.0 means complete replacement (non-incremental update).
        This implementation uses simplified Bellman equation with direct assignment.
    """
    # Initialize Q-table with random values
    qtable = [
        [random.random() for _ in range(env.actions())]
        for _ in range(env.states())
    ]

    # Training loop
    for episode in range(episodes):
        state, _, done = env.reset()
        steps = 0
        episode_reward = 0

        while not done:
            # Clear screen and show current state (matching original article)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("episode #", episode + 1, "/", episodes)
            print(f"Steps: {steps} | Total Reward: {episode_reward} | Epsilon: {epsilon:.4f}")
            env.render()
            time.sleep(0.05)  # Slow down to see the animation

            # Count steps to finish game
            steps += 1

            if random.random() < epsilon:
                # Act randomly to allow exploration
                action = random.choice(range(env.actions()))
            else:
                # Act greedy and select action with max probability
                action = qtable[state].index(max(qtable[state]))

            # Take action
            next_state, reward, done = env.step(action)
            episode_reward += reward

            # Update Q-table using Bellman equation
            qtable[state][action] = reward + gamma * max(qtable[next_state])

            # Update state
            state = next_state

            if steps > 1000:  # Prevent infinite loops
                break

        # The more we learn, the less we take random actions
        epsilon -= decay * epsilon

        # Print episode summary
        print(f"\nEpisode {episode + 1} finished: {steps} steps, Total Reward: {episode_reward}")
        time.sleep(0.5)  # Pause to see the summary

    return qtable


def main():
    """Main training and testing routine"""
    print("="*50)
    print("Lab 2: Q-Learning - Cliff Walking")
    print("Student ID: 041107730")
    print("="*50)

    # Create Cliff Walking environment
    env = env_module.GridEnv(size=12)

    # Hyperparameters
    EPISODES = 50  # Changed from EPOCHS (original: 50 episodes)
    GAMMA = 0.9          # Discount factor
    EPSILON = 0.1        # Initial exploration rate
    DECAY = 0.5          # Epsilon decay rate
    ALPHA = 1.0          # Step-size hyperparameter (for discussion, not used in code)

    print(f"\nHyperparameters:")
    print(f"  Episodes: {EPISODES}")
    print(f"  Gamma (γ): {GAMMA}")
    print(f"  Epsilon (ε): {EPSILON}")
    print(f"  Decay: {DECAY}")
    print(f"  Alpha (α): {ALPHA} (step-size, for discussion)")

    # Train agent with live visualization
    print("\nTraining agent...")
    qtable = train(
        env=env,
        episodes=EPISODES,  # Changed from epochs
        gamma=GAMMA,
        epsilon=EPSILON,
        decay=DECAY,
        alpha=ALPHA  # Added alpha parameter
    )
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
```

---

### 2.3 关键代码解释

#### 2.3.1 Q-Learning 更新公式

```python
qtable[state][action] = reward + gamma * max(qtable[next_state])
```

**这行代码做了什么？**

1. `reward` - 执行动作后立即得到的奖励
2. `max(qtable[next_state])` - 下一状态所有动作中的最大 Q 值
3. `gamma * max(...)` - 对未来奖励打折
4. `reward + gamma * ...` - 当前奖励 + 折扣后的未来最大价值
5. 赋值给 `qtable[state][action]` - 更新这个状态-动作对的价值

**为什么这样更新？**

- 如果下一步会掉悬崖，`max(qtable[next_state])` 会是很负的值
- 即使当前 reward 只是 -1，加上未来的 -100（打折后），总价值会很低
- 智能体会学会避开这个动作

---

#### 2.3.2 ε-greedy 策略

```python
if random.random() < epsilon:
    action = random.choice(range(env.actions()))  # 探索
else:
    action = qtable[state].index(max(qtable[state]))  # 利用
```

**为什么需要探索？**

- 如果只选最大 Q 值（利用），可能永远发现不了更好的路径
- 随机探索可以尝试新动作，发现意外的好策略
- 训练后期可以降低 epsilon，减少探索

**关于 alpha (学习率) 参数**：

本实验中 `alpha=1.0` 表示**完全替换更新**：

- 传统 Q-Learning 使用增量更新：`Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]`
- 当 α=1 时简化为：`Q(s,a) ← r + γ·max Q(s',a')`（直接赋值）
- 本实验使用简化版本，直接用贝尔曼方程赋值，不需要 alpha 参与计算
- alpha 参数保留在函数签名中仅供讨论和对比

---

### 2.4 预期结果

**训练过程输出**：

```
==================================================
Lab 2: Q-Learning - Cliff Walking
Student ID: 041107730
==================================================

Hyperparameters:
  Episodes: 50
  Gamma (γ): 0.9
  Epsilon (ε): 0.1
  Decay: 0.5
  Alpha (α): 1.0 (step-size, for discussion)

Training agent...

episode # 1 / 50
Steps: 393 | Total Reward: -1681 | Epsilon: 0.1000
............
............
............
SXXXXXXXXXXG

Episode 1 finished: 394 steps, Total Reward: -1681

episode # 50 / 50
Steps: 12 | Total Reward: -12 | Epsilon: 0.0000
............
............
...........O
SXXXXXXXXXXG

Episode 50 finished: 13 steps, Total Reward: -13

Training complete!
```

**学习曲线分析**：

| Episode 范围 | 平均步数 | 平均奖励     | Epsilon     | 学习阶段             |
| ------------ | -------- | ------------ | ----------- | -------------------- |
| 1-5          | 100-400  | -200 ~ -1700 | 0.1 → 0.006 | 大量探索，频繁掉悬崖 |
| 6-12         | 20-60    | -20 ~ -170   | 0.003 → 0.0 | 开始学会避开悬崖     |
| 13-25        | 13-28    | -14 ~ -28    | 0.0         | 找到安全路径         |
| 26-50        | 13-17    | -13 ~ -17    | 0.0         | 稳定在最优策略       |

**最优路径**（13步）：

```
起点(3,0) → UP(2,0) → RIGHT×11 → DOWN(3,11)终点
```

可视化：

```
. . . . . . . . . . . .
. . . . . . . . . . . .
O→→→→→→→→→→→↓
S X X X X X X X X X X G
```

---

## Part 3: 数学基础

### 3.1 核心符号

| 符号            | 含义         | 示例                         |
| --------------- | ------------ | ---------------------------- |
| **s**           | 状态         | s = (3, 5) 表示坐标位置      |
| **a**           | 动作         | a = RIGHT 表示向右移动       |
| **r**           | 即时奖励     | r = -1 表示这一步的惩罚      |
| **s'**          | 下一状态     | 执行动作后到达的新状态       |
| **γ** (gamma)   | 折扣因子     | γ = 0.9 表示未来奖励打 9 折  |
| **ε** (epsilon) | 探索率       | ε = 0.1 表示 10% 随机探索    |
| **π** (pi)      | 策略         | π(s) = a 表示在状态 s 选择 a |
| **Q(s,a)**      | 动作价值函数 | 在状态 s 采取动作 a 的价值   |
| **R_t**         | 累积回报     | 从时间 t 开始的总折扣奖励    |

**重要区分：Reward vs Return**

- **Reward (r)**：单步即时奖励，例如走一步得到 -1
- **Return (R_t)**：累积折扣奖励，例如走 3 步总共得到 -1 + 0.9×(-1) + 0.81×10 = 7.19

---

### 3.2 核心公式

#### 3.2.1 贝尔曼方程（Bellman Equation）

$Q(s,a) = r + \gamma \cdot \max_{a'} Q(s',a')$

**含义**：当前动作的价值 = 立即得到的奖励 + 折扣后的最优未来价值

**具体例子**：

```
当前位置 (2,5)，考虑向右走：
Q((2,5), RIGHT) = -1 + 0.9 × max[Q((2,6), UP), Q((2,6), DOWN),
                                  Q((2,6), LEFT), Q((2,6), RIGHT)]
                = -1 + 0.9 × 8.5 = 6.65
```

---

#### 3.2.2 累积奖励（Return）

$R_t = r_{t+1} + \gamma \cdot r_{t+2} + \gamma^2 \cdot r_{t+3} + \cdots$

**含义**：从当前时刻开始，所有未来奖励的折扣总和

**具体例子**：

```
走 4 步到达目标，γ=0.9：
R_0 = -1 + 0.9×(-1) + 0.81×(-1) + 0.729×(+10)
    = -1 - 0.9 - 0.81 + 7.29 = 4.58
```

---

#### 3.2.3 贪婪策略（Greedy Policy）

$\pi^*(s) = \arg\max_{a} Q(s,a)$

**含义**：在状态 s 选择 Q 值最大的那个动作

**具体例子**：

```
状态 (2,5) 的 Q 值：
Q((2,5), UP)    = 5.2
Q((2,5), DOWN)  = 3.1
Q((2,5), LEFT)  = 4.8
Q((2,5), RIGHT) = 6.5  ← 最大

π*((2,5)) = RIGHT
```

**注意**：训练时不能只用贪婪策略，需要 ε-greedy 来探索！

---

## Part 4: 背景知识

### 4.1 强化学习简介

强化学习通过让智能体与环境交互来学习最优策略。就像训练一只狗，做对了给零食（正奖励），做错了不给（负奖励），多次尝试后狗学会了正确行为。

**关键要素**:

- **智能体 (Agent)**: 执行动作的程序实体
- **环境 (Environment)**: 智能体所处的问题空间
- **状态 (State)**: 智能体在环境中的位置或情况
- **动作 (Action)**: 智能体可以采取的行为
- **奖励 (Reward)**: 环境对智能体行为的反馈

### 4.2 马尔可夫决策过程 (MDP)

MDP 定义了一个四元组 (S, A, P, R)：

- **状态空间 S**: 所有可能的状态集合（Cliff Walking 有 48 个状态）
- **动作空间 A**: 所有可能的动作集合（4 个动作：上下左右）
- **转移概率 P**: 在状态 s 采取动作 a 后到达状态 s' 的概率（本实验是确定性环境，P=1）
- **奖励函数 R**: 状态转移时获得的奖励（每步 -1，掉悬崖 -100）

### 4.3 折扣因子

智能体的目标是最大化累积奖励。折扣因子 γ 控制未来奖励的重要性：

- γ = 0: 只关注即时奖励（短视）
- γ = 1: 所有奖励同等重要
- 0 < γ < 1: 平衡即时和未来奖励（常用 0.9）

### 4.4 Q-Learning 算法

**核心思想**：

- 维护 Q-Table 记录每个状态-动作对的价值
- 使用贝尔曼方程更新：`Q(s,a) = r + γ·max Q(s',a')`
- 用 ε-greedy 策略平衡探索与利用

> 💡 **详细的公式推导和参数解释**请参考 [Part 3.2](#32-核心公式)

---

## Part 5: 实验检查

### 5.1 提交前确认

- [ ] 文件已正确重命名（包含学号 041107730）
- [ ] 网格大小为 4×12
- [ ] 添加了 `cliff` 属性
- [ ] 悬崖逻辑正确实现（-100 奖励，返回起点）
- [ ] 每步奖励为 -1
- [ ] 渲染方法显示 'X' 表示悬崖
- [ ] "epoch" 改为 "episode"
- [ ] 打印 Return (总累积奖励)
- [ ] 添加了 `alpha=1` 超参数
- [ ] 代码有注释说明修改内容
- [ ] 智能体能成功到达目标

### 5.2 演示准备

准备讨论的问题：

1. 贝尔曼方程的含义
2. α=1 表示什么？
3. 为什么需要探索（ε-greedy）？
4. γ 的作用是什么？
5. 你的智能体学到了什么策略？

### 5.3 调试技巧

**期望看到的现象**:

1. 初期: 智能体随机游走，经常掉悬崖
2. 中期: 开始避开悬崖，但路径不是最优
3. 后期: 找到最优路径（沿上边走）

**常见问题**:

| 问题             | 可能原因           | 解决方法              |
| ---------------- | ------------------ | --------------------- |
| 智能体一直掉悬崖 | ε 太大，探索过多   | 减小 ε 或增加训练轮数 |
| 学习很慢         | γ 太小，不考虑未来 | 增大 γ (如 0.9)       |
| Q 值不收敛       | 学习率问题         | 检查 α 值和更新公式   |
| 路径不是最优     | 训练不足           | 增加 episodes         |

---

## 📚 参考资源

- **原始教程**: [Math of Q-Learning — Python](https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6)
- **双语版本**: [../resources/math_of_q_learning_python_bilingual.md](../resources/math_of_q_learning_python_bilingual.md)
- **Sutton 教科书**: Reinforcement Learning: An Introduction, Page 132 - Cliff Walking Example
- **实验文档**: [../labs/CST8509_Lab1_CliffWalking.docx](../labs/CST8509_Lab1_CliffWalking.docx)

---

**最后更新**: 2025-01-20
