# Deep Reinforcement Learning
## Project: Train AI to upgrade some mines in the most efficient order
The goal of this project is to develop an AI Bot able to learn how to upgrade several mines. Mine upgrades are investments that will pay over time.
In order to do it, I implemented a Deep Reinforcement Learning algorithm. This approach consists in giving the system parameters related to its state, and a positive or negative reward based on its actions. No rules about the game are given, and initially the Bot has no information on what it needs to do. The goal for the system is to figure it out and elaborate a strategy to maximize the score - or the reward. \

## Install
This project requires Python 3.6 with the pygame library installed, as well as Pytorch. If you encounter any error with `torch=1.7.1`, you might need to install Visual C++ 2015-2019 (or simply downgrade your pytorch version, it should be fine). \
The full list of requirements is in `requirements.txt`. 