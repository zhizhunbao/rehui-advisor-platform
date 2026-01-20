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
          epsilon: float = 0.1, decay: float = 0.5, alpha: float = 1.0,
          render_training: bool = False) -> list[list[float]]:
    """
    Train Q-Learning agent
    
    Args:
        episodes: Number of training episodes
        gamma: Discount factor
        epsilon: Initial exploration rate
        decay: Epsilon decay rate
        alpha: Step-size hyperparameter (for discussion)
        render_training: Show live visualization
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


def test(env: env_module.Env, qtable: list[list[float]], 
         num_episodes: int = 1, render: bool = True) -> None:
    """Test trained agent"""
    print("\n" + "="*50)
    print("Testing Trained Agent")
    print("="*50)

    for episode in range(num_episodes):
        state, _, done = env.reset()
        steps = 0
        total_reward = 0

        if render:
            print(f"\nTest Episode {episode + 1}")
            print("-" * 30)
            env.render()
            print()

        while not done and steps < 100:
            action = qtable[state].index(max(qtable[state]))  # Greedy policy
            
            state, reward, done = env.step(action)
            total_reward += reward
            steps += 1

            if render:
                action_names = ['LEFT', 'RIGHT', 'UP', 'DOWN']
                print(f"Step {steps}: {action_names[action]} | Reward: {reward}")
                env.render()
                print()
                time.sleep(0.3)

        print(f"\nEpisode {episode + 1} finished:")
        print(f"  Steps: {steps}")
        print(f"  Return (Total Reward): {total_reward}")
        print(f"  Success: {'Yes' if done else 'No'}")


def analyze_qtable(qtable: list[list[float]], env: env_module.Env) -> None:
    """
    Analyze Q-table values at key positions
    
    Args:
        qtable: Trained Q-table
        env: Environment instance
    """
    print("\n" + "="*50)
    print("Q-Table Analysis")
    print("="*50)

    action_names = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    
    # For Cliff Walking environment (4×12 grid)
    # Start position is at (3, 0) -> state = 3 * 12 + 0 = 36
    start_state = 36
    print(f"\nStart Position (3, 0):")
    for i, action in enumerate(action_names):
        print(f"  {action:6s}: {qtable[start_state][i]:8.2f}")
    
    # Position above cliff at (2, 1) -> state = 2 * 12 + 1 = 25
    cliff_above = 25
    print(f"\nAbove Cliff (2, 1):")
    for i, action in enumerate(action_names):
        print(f"  {action:6s}: {qtable[cliff_above][i]:8.2f}")


def main():
    """Main training and testing routine"""
    print("="*50)
    print("Lab 2: Q-Learning - Cliff Walking")
    print("Student ID: 041107730")
    print("="*50)

    # Create Cliff Walking environment
    env = env_module.GridEnv(size=12)  # Size parameter not used, but kept for compatibility
    
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
