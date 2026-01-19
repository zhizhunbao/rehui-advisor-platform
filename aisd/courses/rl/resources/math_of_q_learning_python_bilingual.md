# Math of Q-Learning — Python (中英对照)

> **原文链接:** https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6

---

An archive of data science, data analytics, data engineering, machine learning, and artificial intelligence writing from the former Towards Data Science Medium publication.

[待翻译]

---


## Derive the Bellman equation from scratch

Q-Learning is a type of Reinforcement Learning which is a type of Machine Learning. Reinforcement learning has been used lately to teach AIs to play games (Google DeepMind Atari, etc). Our goal is to understand a simple version of reinforcement learning called Q-Learning, and write a program that will learn how to play a simple game. Let’s dive in!

[待翻译]

---

In Q-Learning, we call the program trying to solve the problem the agent. The agent is going to navigate an environment, that is the problem being solved. The environment is modeled mathematically by a Markov Decision Process, which is a graph where each node is a state the agent may be in (think state in a game, e.g. position of the user, coins collected, etc.), and where the edges between those nodes are actions the agent can take to transition from one state to another (think commands in a game, e.g. right, left, jump, run, etc.). The goal of Q-Learning is to learn a so called Q-function, which tells the agent what action to take in a given state in order to maximize a reward function that we will define.

[待翻译]

---

A Markov chain is a mathematical model that experiences transition of states with probabilistic rules.

[待翻译]

---

Here we have two states E and A, and the probabilities of going from one state to another, e.g. there is 70% chance of going to state A starting from state E. In this model, you start from a node of the graph, and simply experience the transition probabilities.

[待翻译]

---

A Markov Decision Process (MDP) is an extension of the Markov chain and it is used to model more complex environments. In this extension, we add the possibility to make a choice at every state which is called an action. We also add a reward which is a feedback from the environment for going from one state to another through an action.

[待翻译]

---

In the image above, we are in the initial state don’t understand, where we have two possible actions, study and don’t study. For the study action, we may end up in different states according to a probabilistic rule. This is what we call a stochastic environment (random), in the sense that for one same action taken in the same state, we might have different results (understand and don’t understand).

[待翻译]

---

In reinforcement learning, this is how we model a game or environment, and our goal will be to maximize the reward we get from that environment.

[待翻译]

---

The reward is the feedback from the environment that tells us how good we are doing. It can be the number of coins you grab in a game for example. Our goal is to maximize the total reward.

[待翻译]

---

We write Rt to denote the total reward we can get starting at some point t in time, as the sum of all the subsequent rewards earned at each time step.

[待翻译]

---

For example, if we use the MDP presented above. We’re initially in the state don’t understand, we take the study action which takes us randomly to don’t understand. Therefore we experienced the reward r(t+1)=-1. Now we can decide to take another action which will give r(t+2) and so on. The total reward is the sum of all the immediate rewards we get for taking actions in the environment.

[待翻译]

---


## Defining the reward this way leads to two major problems :

One way to fix up these problems is to use a decreasing factor for future rewards.

[待翻译]

---

Setting γ=1 takes us back to the first expression where every reward is equally important. Setting γ=0 results in only looking for the immediate reward (always acting for the optimal next step). Setting γ between 0 and 1 is a compromise to look more for immediate reward but still account for future rewards.

[待翻译]

---

We can rewrite that expression in a recursive manner, that will come handy later on.

[待翻译]

---

A policy is a function that tells what action to take in a certain state. This function is usually denoted π(s,a) and yields the probability of taking action a in state s. We want to find the policy that maximizes the reward function.

[待翻译]

---

If we get back to the previous MDP for example, the policy can tell you the probability of taking action study when you’re in the state don’t understand.

[待翻译]

---


## Get Omar Aflak’s stories in your inbox

Join Medium for free to get updates from this writer.

[待翻译]

---

Moreover, because this is a probability distribution, the sum over all the possible actions in a given state must be equal to 1.

[待翻译]

---

We are going to start playing around with some equations, and for that we need to introduce new notations.

[待翻译]

---

This is the expected immediate reward r(t+1) for going from state s to state s’ through action a.

[待翻译]

---

This is the transition probability of going from state s to state s’ through action a. In other words, the probability of ending up in state s’ by taking action a in state s.

[待翻译]

---

Two so-called “value functions” exist. The state value function, and the action value function. These functions are a way to measure the “value”, or how good some state is, or how good some action is, by looking at the reward obtained for being in a given state or taking a certain action.

[待翻译]

---

The value of a state is the expected total reward we can get starting from that state. It depends on the policy π which dictates the actions to take.

[待翻译]

---

The value of an action taken in some state is the expected total reward we can get starting from that state and taking that action. It also depends on the policy π.

[待翻译]

---


## Bellman Equation for Q-Learning

Now that we are settled with notations we can finally start playing around with the math! Looking at the following diagram during the calculation can help you understand.

[待翻译]

---

We will start by expanding the state value function. The expected operator is linear.

[待翻译]

---

Next, we can expand the action value function.

[待翻译]

---

This form of the Q-Value is very generic. It handles stochastic environments, but we could write it down in a deterministic one. Meaning, whenever you take an action you always end up in the same next state and receive the same reward. In that case, we simply do not need to make a weighted sum with probabilities, and the equation becomes:

[待翻译]

---

Where s’ is the state you end up in for taking action a in state s. Written, more explicitly, this is:

[待翻译]

---

You can read that as the value of (the goodness of) taking action a in state s(t), is the immediate reward obtained for taking action a in state s(t) plus the value of being in state s(t+1) (the expected future rewards for being in state s(t+1)…).

[待翻译]

---

You probably already came across greedy policy reading on the internet. A greedy policy is a policy where you always choose the optimal next step.

[待翻译]

---

In a greedy policy context, we can write a relation between the state value and the action value functions.

[待翻译]

---

Therefore, plugging this into the previous equation, we get the Q-Value of a (state, action) pair in a deterministic environment, following a greedy policy.

[待翻译]

---

And this is the Bellman equation in the Q-Learning context ! It says that the value of an action a in some state s is the immediate reward you get for taking that action, plus the maximum expected future rewards you can get in the next state.

[待翻译]

---

It actually makes sense when you think about it.

[待翻译]

---

Here, if you only look at the immediate reward, you surely choose to go left. Unfortunately, the game ends after and you cannot get more points.

[待翻译]

---

If you add the maximum expected reward of the next state, then you will most probably go to the right since the maximum expected reward of S1 is equal to zero and the maximum expected reward of S2 is probably higher than 10–5=5.

[待翻译]

---

You can also tweak γ to specify how important are the next rewards.

[待翻译]

---

Here is a simple environment which consists of a 5-by-5 grid. A treasure (T) is placed at the bottom right corner of the grid. The agent (O) starts at the top left corner of the grid.

[待翻译]

---

The agent needs to get to the treasure using the 4 available actions : left, right, up, down.

[待翻译]

---

If the agent takes an action that leads him directly to T, he gets a reward of 1, otherwise a reward of 0.

[待翻译]

---

The code is well commented and it is simply what we just discussed. Now the interesting part, the Q-Learning algorithm !

[待翻译]

---

I almost commented every single line of this code, so hopefully, it will be easy to understand!

[待翻译]

---


## Put both of the above files in the same directory, and run :

Around the epoch number 40, the agent should have learned to get to the treasure using one of the shortest paths (8 steps).

[待翻译]

---

We have seen how to derive statistical formulas to find the Bellman equation and used it to teach an AI how to play a simple game. Notice that in this game, the number of possible states is finite (the number of different cells you might end up in), which is why building a Q-Table (a table of values that approaches the real value of the Q function for discrete values) is still manageable. What about a graphical game, such as Flappy Bird, Mario Bros, or Call Of Duty ? Every frame displayed by the game can be considered as a different state. In that case it’s impossible to build a Q-Table, and what we do instead is use a neural network who’s goal will be to learn the Q function. That neural network will typically take as input the current state of the game, and output the best possible action to take in that state. This is known as Deep Q Learning and is exactly how AIs such as Deep Blue or Alpha Go managed to beat world champions at Chess or Go.

[待翻译]

---


## I hope you enjoyed this article! Stay around for more! 😎

An archive of data science, data analytics, data engineering, machine learning, and artificial intelligence writing from the former Towards Data Science Medium publication.

[待翻译]

---

good writing ! can I translate it into chinese and publish it? Of course I will put the origin url.

[待翻译]

---

Hi, great writing, I got confused on the Bellman equation section, why we compute max(q[next_state]) value if there is no Q value of the next state, because to get that value we actually need the bellman equation indeed?

[待翻译]

---

As for the immediate reward notation you took an expected value. Can I get different reward while my state s and next s' and action a is fixed? Thanks in advance

[待翻译]

---


## More from Omar Aflak and TDS Archive


## Ray Tracing From Scratch in Python

Create a computer-generated image using the Ray Tracing algorithm coded from scratch in Python.

[待翻译]

---

Napoleon was the Best General Ever, and the Math Proves it.

[待翻译]

---


## Ranking Every* General in the History of Warfare


## Understanding LLMs from Scratch Using Middle School Math

In this article, we talk about how LLMs work, from scratch — assuming only that you know how to add and multiply two numbers. The article…

[待翻译]

---


## Neural Network from scratch in Python

Make your own machine learning library.

[待翻译]

---


## How Math Makes Machine Learning Easy


## Intuitive examples of how numbers power AI models

A Complete Taxonomy of Reinforcement Learning Algorithms: From Basics to Cutting-Edge

[待翻译]

---


## XGBoost Finally Explained: The Simple Breakdown That Most Tutorials Skip


## How Large Language Models (LLMs) Actually Work


## Making Sense of the Brains Behind Gen AI In Simple Terms


## The AI Bubble Is About To Burst, But The Next Bubble Is Already Growing

Techbros are preparing their latest bandwagon.

[待翻译]

---


## The Complete Guide to Exploratory Data Analysis (EDA) with Python

Exploratory Data Analysis (EDA) serves as the foundation of data science, providing crucial insights that guide decision-making and model…

[待翻译]

---


## 学习建议

根据 RL skill 的指导，现在你可以：

1. **理解核心概念** - 仔细阅读原文和翻译
2. **做笔记** - 标记重点和疑问
3. **实践** - 如果有代码示例，动手实现
4. **提问** - 对不理解的部分提问

需要我帮你：
- 翻译某个段落？
- 解释某个概念？
- 实现相关代码？
