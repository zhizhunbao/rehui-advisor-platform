"""
Lab 2: Cliff Walking Environment
Student ID: 041107730

Modified from Hybrid Activity 1 to implement the Cliff Walking problem
from Sutton & Barto's Reinforcement Learning textbook (Page 132)

Grid Layout (4 rows × 12 columns):
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    S X X X X X X X X X X G

Where:
    S = Start (bottom-left)
    G = Goal (bottom-right)
    X = Cliff (10 grey squares in the bottom row)
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
        # Changed: Initialize for Cliff Walking world (4 rows × 12 columns)
        # Original was a square grid (size × size)
        self.x = 0
        self.y = 3  # Start at bottom-left (row 3, col 0)
        self.height = 4  # 4 rows for Cliff Walking
        self.width = 12  # 12 columns for Cliff Walking
        self.end_x = 11  # Goal at bottom-right (row 3, col 11)
        self.end_y = 3
        self.done = False
        
        # Added: cliff attribute to track if agent fell off cliff
        self.cliff = False

    def actions(self) -> int:
        return 4

    def states(self) -> int:
        # Changed: Total states for 4×12 grid = 48
        return self.height * self.width

    def step(self, action: int) -> tuple[int, int, bool]:
        # Move agent based on action
        if action == 0:  # left
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:  # right
            self.x = self.x + 1 if self.x < self.width - 1 else self.x
        if action == 2:  # up
            self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3:  # down
            self.y = self.y + 1 if self.y < self.height - 1 else self.y

        # Changed: Check if agent fell off cliff (bottom row, columns 1-10)
        # If so, set cliff attribute to True and return agent to start
        if self.y == 3 and 1 <= self.x <= 10:
            self.cliff = True
            reward = -100  # Large negative reward for falling off cliff
            self.x = 0  # Return to start position
            self.y = 3
            done = False  # Episode continues
        else:
            self.cliff = False
            # Changed: Reward is -1 for each step (encourages shortest path)
            reward = -1
            # Check if reached goal
            done = self.x == self.end_x and self.y == self.end_y

        # Calculate next state index
        next_state = self.y * self.width + self.x
        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        # Reset to start position (bottom-left)
        self.x = 0
        self.y = 3
        self.done = False
        self.cliff = False
        return self.y * self.width + self.x, 0, False

    def render(self):
        # Changed: Render method to show cliff as X's
        for i in range(self.height):
            for j in range(self.width):
                if self.y == i and self.x == j:
                    print("O", end='')  # Agent position
                elif i == self.end_y and j == self.end_x:
                    print("G", end='')  # Goal
                elif i == 3 and 1 <= j <= 10:
                    print("X", end='')  # Cliff (10 grey squares)
                elif i == 3 and j == 0:
                    print("S", end='')  # Start position
                else:
                    print(".", end='')  # Empty cell
            print("")
