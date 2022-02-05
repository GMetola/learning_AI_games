import pyglet
import pyglet.gl as gl
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
from ShapeObjects import *
from PygameAdditionalMethods import *
import PygameAdditionalMethods as pgam

frameRate = 30.0
os.chdir(r'C:\git\Car-QLearning_v2')

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
        trackImg = pyglet.image.load('images/track.png')
        self.trackSprite = pyglet.sprite.Sprite(trackImg, x=0, y=0)
        # load background image
        self.game = Game()
        self.car = self.game.car
        #self.ai = QLearning(self.game)

    """
    called when a key is hit
    """
    """
    called when a key is released
    """    
    
    def on_key_press(self, symbol, modifiers):
        # GMF: inherited from pyglet.window.Window class, I suppose
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
        # GMF: inherited from pyglet.window.Window class, I suppose
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


    def on_draw(self):
        
        gl.glPushMatrix()
        
        gl.glTranslatef(-1, -1, 0)
        gl.glScalef(1 / (displayWidth / 2), 1 / (displayHeight / 2), 1)
        
        #self.clear()

        label_score = pyglet.text.Label("Score: " + str(self.car.score),
                                    font_name='Times New Roman',
                                    font_size=24,
                                    x=window.width//20*17, y=window.height//20*19,
                                    anchor_x='left', anchor_y='center')
        label_max_score = pyglet.text.Label("Max Score: " + str(self.car.max_score),
                                    font_name='Times New Roman',
                                    font_size=24,
                                    x=window.width//20*17, y=window.height//20*18,
                                    anchor_x='left', anchor_y='center')                                    
        

        self.trackSprite.draw()
        label_score.draw()
        label_max_score.draw()
        self.car.show()
        """    
        for w in self.walls:
            w.draw()
        # for g in self.gates:
        #     g.draw()
        vision = self.car.getState()
        
        for i in range(len(vision)):
        
            label = pyglet.text.Label("{}:  {}".format(i,vision[i]),
                                        font_name='Times New Roman',
                                        font_size=24,
                                        x=10, y=50*i+250,
                                        anchor_x='left', anchor_y='center')
            label.draw()
        """
        gl.glPopMatrix()
        

    """
    called when window resized
    """

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)

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
        pass


if __name__ == "__main__":
    window = MyWindow(displayWidth, displayHeight, "Gabriel Learns to Drive", resizable=False)
    pyglet.clock.schedule_interval(window.update, 1 / frameRate)
    pyglet.app.run()
