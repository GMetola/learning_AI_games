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

### 2022-12-13 | Finishing Official OpenAI tutorial
Registering the env with https://www.gymlibrary.dev/content/environment_creation/#registering-envs

### 2022-12-24 | Learning to create package
First I created a checker that detected some errors.
```
    from gym.utils.env_checker import check_env
    env.check_env()
```
I modified reset to return just observation, deleting info
It also informed that Discrete spaces must contain ints, but mine contained array.int32. I dismissed this error and went to the next step.
I modified setup.py and installed it with pip (see snippets_log.md)
Note to self: before installing something you have created, clone the actual working virtualenv...
I just realized that my changes at 'C:\git\learning_AI_games\gym' (gym version 0.26.0) won't be as impactfull as I thought, because the gym version that conda uses is at 'C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym' (gym version 0.21.0)

### 2023-01-01 | Creating package and saving results
I installed gym 0.26.2 in conda envs 'base' and 'tf_gpu_mygames'
To make it work, I modified:
- C:\Users\metol\.conda\envs\tf_gpu_mygames\Lib\site-packages\gym\envs\classic_control\myenv.py
- C:\Users\metol\.conda\envs\tf_gpu_mygames\Lib\site-packages\gym\envs\classic_control\__init__.py
- C:\Users\metol\.conda\envs\tf_gpu_mygames\Lib\site-packages\gym\envs\__init__.py
I managed to successfully use
```
env = gym.make("MyEnv-v0")
```
I started to save results at "learning_AI_games\travian_basic_python\hall of fame - travian gym.csv". Now choices are random, so points should be lower now than when I get to apply Q-learning.

### 2023-01-12 | Reading Markov processes and abandoning GYM
For a process to be markovian, the probabilities of the future must depend only on the present, not on the past. Thus, we should include in the present every attribute of the game that past decisions have altered.

It cannot incorporate new attributes, the number of attributes must be the same thoughout the game. For example, if a player may choose a particular perk/race/upgrade once per game, that choice must be within the attributes of the Markov Decision Process (MDP) all game long; until the player makes the decision that attribute could be marked as False, but must exist.
Reading about MDPs, I conclude that this method will only be of use in the future, when I have several players. From the point of view of the machine the decisions of those players will be slightly stochastic, between the most profitable options those players have. Why should we supose an array of stochastic adversary moves instead of the 'best one'? Because humans won't always choose the "best one" or maybe there is a factor the machine is not taking into account.
Also, my current game isn't stochastic at all, and has a mathematical solution, consistent and deterministic.
On future games where a deck of cards modifies the state of the game each turn we'll face randomness, maybe Markov will come handly then, but I bet there'll be a more efficient method.
