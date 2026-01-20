"""
Q-Learning Training Algorithm
Based on: https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6

Implements the Bellman equation: Q(s,a) = r + γ * max Q(s',a')
"""

import os
import medium_qlearning_env as env
import time
import random


def train(e: env.Env) -> list[list[float]]:
    qtable = [
        [random.random() for _ in range(e.actions())]
        for _ in range(e.states())
    ]

    # hyperparameters
    epochs = 50
    gamma = 0.1
    epsilon = 0.08
    decay = 0.5

    # training loop
    for i in range(epochs):
        state, reward, done = e.reset()
        steps = 0

        while not done:
            os.system('clear')
            print("epoch #", i+1, "/", epochs)
            e.render()
            time.sleep(0.01)

            # count steps to finish game
            steps += 1

            if random.random() < epsilon:
                # act randomly to allow exploration
                action = random.choice(range(e.actions()))
            else:
                # act greedy and select action with max probability
                action = qtable[state].index(max(qtable[state]))

            # take action
            next_state, reward, done = e.step(action)

            # update qtable value with Bellman equation
            qtable[state][action] = reward + gamma * max(qtable[next_state])

            # update state
            state = next_state

        # The more we learn, the less we take random actions
        epsilon -= decay * epsilon

        print("\nDone in", steps, "steps".format(steps))
        time.sleep(0.8)

    return qtable


grid = env.GridEnv(10)
train(grid)
