import random
import time

import cv2
import gym
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image

from gym import Env, spaces, ObservationWrapper, RewardWrapper
from travian_classes import Dorf


class Village(Env, Dorf):
    """Creates a Village where we will build mines"""
    metadata = {"render_modes": [None], "render_fps": 1}

    def __init__(self) -> None:
        # inhereting from gym Env
        super(Village, self).__init__()  # TODO Am I sure this needs to be here?

        # Define observation space
        self.observation_space = spaces.Dict(
            {
            "wood_storage":spaces.Box(low=0,high=1e6,dtype=int),
            "wood_level":spaces.Discrete(20),
            "clay_storage":spaces.Box(low=0,high=1e6,dtype=int),
            "clay_level":spaces.Discrete(20),
            "iron_storage":spaces.Box(low=0,high=1e6,dtype=int),
            "iron_level":spaces.Discrete(20),
            "wheat_storage":spaces.Box(low=0,high=1e6,dtype=int),
            "wheat_level":spaces.Discrete(20)
            }
        )

        # Define action space
        # your actions are just to level up mines or economize (save resources)
        self.action_space = spaces.Discrete(self.num_resources + 1)

        # Limitations
        self.turn_number = 0
        self.points = 0
        self.game_turns = 20
        self.turns_left = 20

        # Define basic elements of a new game
        self.reset()


    def reset(self, seed=None, options=None):
        """
        Resets the environment to an initial state and returns the initial observation.
        This method can reset the environment's random number generator(s) if seed is an integer or if the environment
            has not yet initialized a random number generator.
            If the environment already has a random number generator and reset() is called with seed=None,
            the RNG should not be reset. Moreover, reset() should (in the typical use case) be called with
            an integer seed right after initialization and then never again.

        PARAMETERS:
            - seed (optional int) - The seed that is used to initialize the environment's PRNG.
                If the environment does not already have a PRNG and seed=None (the default option) is passed,
                a seed will be chosen from some source of entropy (e.g. timestamp or /dev/urandom).
                However, if the environment already has a PRNG and seed=None is passed, the PRNG will not be reset.
                If you pass an integer, the PRNG will be reset even if it already exists.
                Usually, you want to pass an integer right after the environment has been initialized and then never again.
                Please refer to the minimal example above to see this paradigm in action.
            - options (optional dict) - Additional information to specify how the environment is reset (optional,
                depending on the specific environment)
        RETURNS:
            - observation (object) - Observation of the initial state.
                This will be an element of observation_space (typically a numpy array) and is analogous to
                the observation returned by step().
            - info (dictionary) - This dictionary contains auxiliary information complementing observation.
                It should be analogous to the info returned by step().
        """
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        info = {
                "function":"reset",
                "turn":self.turn_number,
                "seed":None,
                "options":None
                }

        # Reset buildings and resources
        self.reset_dorf()
        observation = self._get_obs()

        # Reset game state
        self.points = np.sum(self.resources).astype(int)
        self.turn_number = 0

        return observation, info


    def get_action_meanings(self):
        """Meaning of actions"""
        return {0:"Do nothing",
                1:"Build mine of resource 1",
                2:"Build mine of resource 2",
                3:"Build mine of resource 3",
                4:"Build mine of resource 4"}


    def step(self, action):
        """
        PARAMETERS:
            - action (ActType) - an action provided by the agent
        RETURNS:
            - observation (ObsType object) - this will be an element of the environment's observation_space.
            - reward (float) - The amount of reward returned as a result of taking the action.
            - terminated (bool) - whether a terminal state (as defined under the MDP of the task) is reached.
                In this case further step() calls could return undefined results.
            - truncated (bool) - whether a truncation condition outside the scope of the MDP is satisfied.
                Typically a timelimit, but could also be used to indicate agent physically going out of bounds.
                Can be used to end the episode prematurely before a terminal state is reached.
            - info (dictionary) - info contains auxiliary diagnostic information (helpful for debugging)
                This might, for instance, contain:
                    > metrics that describe the agent's performance state
                    > variables that are hidden from observations
                    > or individual reward terms that are combined to produce the total reward.
                It also can contain information that distinguishes truncation and termination,
                 however this is deprecated in favour of returning two booleans, and will be removed in a future version.
            - (deprecated)
            - done (bool) - A boolean value for if the episode has ended,
                in which case further step() calls will return undefined results.
                A 'done' signal may be emitted for different reasons:
                    > Maybe the task underlying the environment was solved successfully
                    > a certain timelimit was exceeded
                    > or the physics simulation has entered an invalid state.
        """
        # Parameters needed by gym (not used right now)
        terminated = False
        truncated = False
        info = {
                "function":"step",
                "turn":self.turn_number,
                "action":action,
                "aux_info_here":None,
                "more_info":None
                }
        done = False

        # Tests
        assert self.action_space.contains(action), "Invalid Action"
        self.general_tests()

        self.purchase_improvement(action)

        # Points and rewards
        reward = self._calculate_reward(action)
        self.points = np.sum(self.resources).astype(int)

        # Game updates
        observation = self._get_obs()
        self.turn_number += 1
        self.harvest()
        if self.turn_number > self.game_turns:
            done = True
        return observation, reward, done, info


    def general_tests(self):
        """Check that nothing has been broken"""
        # TODO
        self.check_positive_storage()


    def _calculate_reward(self, action):
        """
        Calculate reward of certain action.
        It shall take into account future turns.
        """
        self.turns_left = self.game_turns - self.turn_number
        build_option = self.buildings[action-1]
        next_level_prod = build_option.production/build_option.level*(build_option.level+1)
        prod_increase = next_level_prod - build_option.production
        reward = np.sum(prod_increase * self.turns_left).astype(float)
        # TODO some resources should have more value than others for reward. Do a weighted sum!
        return reward

    def _get_obs(self):
        return {
            "wood_stored":self.resources[0],
            "wood_level":self.building_levels[0],
            "clay_stored":self.resources[1],
            "clay_level":self.building_levels[1],
            "iron_stored":self.resources[2],
            "iron_level":self.building_levels[2],
            "wheat_stored":self.resources[3],
            "wheat_level":self.building_levels[3]
        }


if __name__ == '__main__':
    env = Village()
    env.reset()
    for i in range(10):
        myaction = env.action_space.sample()
        env.step(myaction)
        print(f"Turn {i} - Points: {env.points}")
    env.print_buildings()
