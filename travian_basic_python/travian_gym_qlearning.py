import random
import time

import cv2
import gym
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image

from gym import Env, spaces


class Village(Env):
    """Creates a Village where we will build mines"""
    points = 0
    def __init__(self, num_resources) -> None:
        # inhereting from gym Env
        super(Village, self).__init__()

        self.num_resources = num_resources
        # Define observation space
        # The 3 comes from (storage, production, mine_level)
        self.observation_shape = (self.num_resources, 3)
        self.observation_space = spaces.Box(low=np.zeros(self.observation_shape),
                                            high=1e6*np.ones(self.observation_shape),
                                            dtype=np.float16)

        # Define action space
        # your actions are just to level up mines or economize (save resources)
        self.action_space = spaces.Discrete(self.num_resources + 1,)

        # Define elements present inside the environment
        self.resources = np.zeros(self.num_resources)
        self.production = np.ones(self.num_resources)
        self.mine_level = np.ones(self.num_resources)

        # TODO Define mine costs and productions

        # Limitations
        self.max_fuel = 1000
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]

    def reset(self):
        """Start new game"""
        self.resources = np.zeros(self.num_resources)
        self.production = np.ones(self.num_resources)
        self.mine_level = np.ones(self.num_resources)

        self.points = np.sum(self.resources)

    def step(self):
        """Each of the turns"""
        # TODO
        pass
