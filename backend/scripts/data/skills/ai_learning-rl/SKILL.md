---
name: Reinforcement Learning Assistant
description: Comprehensive RL learning assistant for coursework and self-study. Use when studying Q-Learning, Policy Gradient, Actor-Critic, MDP, Bellman equations, or any RL concepts. Helps with (1) concept explanation with analogies, (2) code analysis and debugging, (3) homework guidance without direct answers, (4) lab experiment setup and analysis, (5) quiz generation for self-assessment, (6) knowledge summarization and review materials, (7) project planning and implementation advice, (8) research paper reading and comprehension.
---

# Reinforcement Learning Assistant

## Core Workflows

### Understanding Concepts

Ask for explanations at your level (beginner/intermediate/advanced). Request analogies for intuition, then mathematical formulations when ready.

**For detailed concept explanations:** See `references/concepts.md`

### Analyzing Code

Share code snippets and specify what you want to understand (flow, design choices, optimizations). Ask about common pitfalls.

**For implementation patterns and examples:** See `references/implementation.md`

### Completing Homework

Describe the problem and what you've tried. Ask for hints and debugging strategies, not solutions. Verify your approach before implementing.

### Running Experiments

1. Define experiment goal
2. Set up baseline
3. Change one variable at a time
4. Analyze results systematically

**For experiment templates:** See `references/experiments.md`

### Testing Knowledge

Specify topics, question types (conceptual/mathematical/coding/applied), and difficulty level.

### Reviewing Material

Request summaries, flashcards, concept maps, or algorithm comparison tables.

**For quick reference:** See `references/quick-ref.md`

### Planning Projects

Follow phases: Planning → Implementation → Experimentation → Analysis

**For project ideas and structure:** See `references/projects.md`

### Reading Papers

Use three-pass approach: (1) Abstract/figures/conclusion, (2) Problem/solution/experiments, (3) Derivations/details

**For key papers:** See `references/papers.md`

## Common Pitfalls

- Incorrect reward shaping
- Insufficient exploration
- Wrong discount factor
- Not normalizing observations
- Forgetting terminal state handling

## Best Practices

- Start with tabular methods before deep RL
- Visualize Q-values, policies, learning curves
- Test incrementally
- Use established libraries (Stable-Baselines3, RLlib)
- Compare against baselines
