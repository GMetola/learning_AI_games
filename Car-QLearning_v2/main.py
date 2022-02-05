import pyglet
from pyglet.gl import *
import pygame
import math
from pyglet.window import key
from Drawer import Drawer
# from PygameAdditionalMethods import *
from ShapeObjects import Line
#import tensorflow as tf  # Deep Learning library
import numpy as np  # Handle matrices
from collections import deque
import random
import os
from Globals import displayHeight, displayWidth
from Game import Game

frameRate = 30.0
os.chdir(r'C:\git\metola_car')

vec2 = pygame.math.Vector2

"""
a line which the car object cannot touch
"""


class Memory:
    def __init__(self, maxSize):
        self.buffer = deque(maxlen=maxSize)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batchSize):
        buffer_size = len(self.buffer)
        index = np.random.choice(np.arange(buffer_size),
                                 size=batchSize,
                                 replace=False)
        return [self.buffer[i] for i in index]

"""

a class inheriting from the pyglet window class which controls the game window and acts as the main class of the program
"""


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

        # set background color
        backgroundColor = [0, 0, 0, 255]
        backgroundColor = [i / 255 for i in backgroundColor]
        glClearColor(*backgroundColor)
        # load background image
        self.game = Game()
        self.car = self.game.car
        #self.ai = QLearning(self.game)

    """
    called when a key is hit
    """

    def on_key_press(self, symbol, modifiers):
        #pass  # <-- when AI is active
        if symbol == key.RIGHT:
            self.car.turningRight = True
        
        if symbol == key.LEFT:
            self.car.turningLeft = True
        
        if symbol == key.UP:
            self.car.accelerating = True
        
        if symbol == key.DOWN:
            self.car.reversing = True

    """
    called when a key is released
    """

    def on_close(self):
        print("close AI deactivated")
        pass
        #self.ai.sess.close()

    def on_key_release(self, symbol, modifiers):
        #pass  # <-- when AI is active
        if symbol == key.RIGHT:
            self.car.turningRight = False
        
        if symbol == key.LEFT:
            self.car.turningLeft = False
        
        if symbol == key.UP:
            self.car.accelerating = False
        
        if symbol == key.DOWN:
            self.car.reversing = False
        
        #if symbol == key.SPACE:
        #    self.ai.training = not self.ai.training

    def on_mouse_press(self, x, y, button, modifiers):
        #pass  # <-- when AI is active
        print(x,y)
        if self.firstClick:
            self.clickPos = [x, y]
        else:
            print("self.walls.append(Wall({}, {}, {}, {}))".format(self.clickPos[0],
                                                                    displayHeight - self.clickPos[1],
                                                                    x, displayHeight - y))
        
            #self.gates.append(RewardGate(self.clickPos[0], self.clickPos[1], x, y))
        
        self.firstClick = not self.firstClick

    """
    called every frame
    """

    def on_draw(self):
        self.game.render()
        #
        # glPushMatrix()
        #
        # glTranslatef(-1, -1, 0)
        # glScalef(1 / (displayWidth / 2), 1 / (displayHeight / 2), 1)
        #
        # self.clear()
        # self.trackSprite.draw()
        # self.car.show()
        #
        # for w in self.walls:
        #     w.draw()
        # # for g in self.gates:
        # #     g.draw()
        # vision = self.car.getState()
        #
        # for i in range(len(vision)):
        #
        #     label = pyglet.text.Label("{}:  {}".format(i,vision[i]),
        #                               font_name='Times New Roman',
        #                               font_size=24,
        #                               x=10, y=50*i+250,
        #                               anchor_x='left', anchor_y='center')
        #     label.draw()
        # glPopMatrix()

    """
    called when window resized
    """

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    """
    called every frame
    """

    def update(self, dt):
        # for i in range(5):

        #     if self.ai.training:
        #         self.ai.train()
        #     else:
        #         self.ai.test()
        #         return
        self.car.update()


if __name__ == "__main__":
    window = MyWindow(displayWidth, displayHeight, "Gabriel Learns to Drive", resizable=False)
    pyglet.clock.schedule_interval(window.update, 1 / frameRate)
    pyglet.app.run()
