# Log of the steps followed

## Enumerating possible paths to build the game
Gym, a library from OpenAI (https://github.com/openai/gym/issues) creates games in gym-environments where Q-learning algorithms can be executed.

How to create a basic game OpenAI style:
- https://www.c-sharpcorner.com/article/q-learning-using-python-and-openai-gym/
- https://hub.packtpub.com/create-your-first-openai-gym-environment-tutorial/
How to create a custom game in gym:
- Short: https://stackoverflow.com/questions/45068568/how-to-create-a-new-gym-environment-in-openai
- Example of custom game: https://github.com/MartinThoma/banana-gym
- Detailed: https://blog.paperspace.com/creating-custom-environments-openai-gym/ . Here its first step: https://blog.paperspace.com/getting-started-with-openai-gym/

## Managing legality of actions
Some actions are illegal along the game (due to lack of resources). Should the action space change each turn? When should the purchase-power-check be made?

Post that defends replacing the action space by a legal action space: https://stats.stackexchange.com/questions/378008/how-to-handle-a-changing-action-space-in-reinforcement-learning
Post that explains AlphaGo's choice in this matter (also replacing action space by legal action space): https://stats.stackexchange.com/questions/328835/enforcing-game-rules-in-alpha-go-zero

### How should the legal action space be implemented?
...

## Daily steps
### 2022-11-06 | Starting with Gym
I start following https://blog.paperspace.com/getting-started-with-openai-gym/

While installing "baselines" I deleted a couple packages and I almost deleted OpenCV 😱
See "1.- Error" at snippets_log.md

### 2022-12-02 | Reset & Step
I keep following https://blog.paperspace.com/creating-custom-environments-openai-gym/
Legality of actions

### 2022-12-06 | Unify classes.
turn functions was moved into travian_classes' Dorf
Village class from travian_gym_qlearning was made child of Dorf
log cleanned, by moving snippets to another file
tests passed

### 2022-12-12 | Finished first tutorial.
Little cleanning.
Main executes a 10-turn game with random choices succesfullly.
### 2022-12-12 | Start Official OpenAI tutorial
I just found OpenAI's official tutorial
https://www.gymlibrary.dev/content/environment_creation/
gym core documentation: https://www.gymlibrary.dev/api/core/
In this documentation finally appear the parameters that step and reset need.
I will start updating my functions to follow the official ones.
There are wrappers for observation, reward and actions, but I won't need them because I am building the game from scratch.
Seems that the observations should be made close to the end of step and reset functions.
I finish the day having done https://www.gymlibrary.dev/content/environment_creation/#constructing-observations-from-environment-states
Next is https://www.gymlibrary.dev/content/environment_creation/#reset
Not test made after I started the official tutorial.
