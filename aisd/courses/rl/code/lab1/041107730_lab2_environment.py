"""
Environment Implementation for Q-Learning
Based on: https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6

Student ID: 041107730
Renamed from medium_qlearning_env.py (no modifications)

A simple 10x10 grid environment where:
- Agent (O) starts at top-left corner (0, 0)
- Treasure (T) is at bottom-right corner (9, 9)
- Agent uses 4 actions: left (0), right (1), up (2), down (3)
- Reward: 1 if reaching treasure, 0 otherwise
"""

import abc


class Env(abc.ABC):
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
    def __init__(self, size: int):
        self.x = 0
        self.y = 0
        self.size = size
        self.end_x = size - 1
        self.end_y = size - 1
        self.done = False

    def actions(self) -> int:
        return 4

    def states(self) -> int:
        return self.size ** 2

    def step(self, action: int) -> tuple[int, int, bool]:
        if action == 0:  # left
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:  # right
            self.x = self.x + 1 if self.x < self.size - 1 else self.x
        if action == 2:  # up
            self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3:  # down
            self.y = self.y + 1 if self.y < self.size - 1 else self.y

        done = self.x == self.end_x and self.y == self.end_y
        next_state = self.size * self.y + self.x
        reward = 1 if done else 0
        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        self.x = 0
        self.y = 0
        self.done = False
        return 0, 0, False

    def render(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.y == i and self.x == j:
                    print("O", end='')
                elif self.end_y == i and self.end_x == j:
                    print("T", end='')
                else:
                    print(".", end='')
            print("")
