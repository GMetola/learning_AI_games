import random
import time

import cv2
import gym
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image

from gym import Env, spaces
from travian_classes import Dorf


class Village(Env, Dorf):
    """Creates a Village where we will build mines"""
    def __init__(self) -> None:
        # inhereting from gym Env
        super(Village, self).__init__()

        # Define observation space
        # Observation_shape has 3 layers: storage, production, mine_level
        self.observation_shape = (self.num_resources, 3)
        self.observation_space = spaces.Box(low=np.zeros(self.observation_shape),
                                            high=1e6*np.ones(self.observation_shape),
                                            dtype=np.float16)

        # Define action space
        # your actions are just to level up mines or economize (save resources)
        self.action_space = spaces.Discrete(self.num_resources + 1,)

        # Define basic elements of a new game
        self.reset()

        # Limitations
        self.max_fuel = 1000
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]

    def reset(self):
        """Start new game"""
        # Reset buildings and resources
        self.reset_dorf()

        # Reset game state
        self.points = np.sum(self.resources).astype(int)
        self.turn_number = 0

    def get_action_meanings(self):
        """Meaning of actions"""
        return {0:"Do nothing",
                1:"Build mine of resource 1",
                2:"Build mine of resource 2",
                3:"Build mine of resource 3",
                4:"Build mine of resource 4"}

    def step(self, action):
        """Each of the turns"""

        assert self.action_space.contains(action), "Invalid Action"
        self.general_tests()

        self.turn_number += 1
        self.purchase_improvement(action)
        self.points = np.sum(self.resources).astype(int)
        self.harvest()
        return

    def general_tests(self):
        """Check that nothing has been broken"""
        # TODO
        self.check_positive_storage()


if __name__ == '__main__':
    env = Village()
    env.reset()
    for i in range(10):
        action = env.action_space.sample()
        env.step(action)
        print(f"Turn {i} - Points: {env.points}")
    env.print_buildings()