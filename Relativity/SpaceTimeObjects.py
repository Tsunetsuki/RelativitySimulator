import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

'''#object running in time
class STObject:

    def __init__(self):
        self.transformation = identity(4)

    def draw(self, color: array, ):
        pass
'''

class Player:
    def __init__(self, pos: array, beta: number, size: number):
        self.pos = pos.astype(float64)
        self.size = size
        self.beta = beta
        self.phi = arctanh(beta)
        self.gamma = cosh(self.phi)
        self.proper_time = 0

    def accelerate(self, d_phi: number):# d_phi = proper acceleration??
        self.set_phi(self.phi + d_phi)

    def reset_velocity(self):
        self.set_phi(0)

    def set_phi(self, phi):
        self.phi = phi
        self.beta = tanh(phi)
        self.gamma = cosh(phi)

    def get_basis_x(self):
        return self.gamma * array([1, self.beta])

    def get_basis_t(self):
        return self.gamma * array([self.beta, 1])

    def step(self, d):
        self.proper_time += d

        velocity = self.gamma * array([self.beta, 1])

        self.pos += velocity * d

    def draw(self):
        color = (floor(self.proper_time) % 2, 0.5, 0, 1)
        glColor4fv(color)
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2dv(self.pos)
        glEnd()

# beta/phi are measured from initial FoR, so they remain constant for zero acceleration.
class NPC:
    def __init__(self, pos: array, beta: number, color, size):
        self.pos = pos.astype(float64)
        self.size = size
        self.beta = beta
        self.phi = arctanh(beta)
        self.proper_time = 0
        self.color = color

    #d is from the stationary FoR!
    def step(self, d, player_phi):
        gamma = cosh(self.phi - player_phi)
        self.proper_time += d / gamma

        velocity = gamma * array([self.beta, 1])
        self.pos += velocity * d

    def draw(self):
        glColor3fv(self.color)
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2fv(self.pos)
        glEnd()

        if floor(self.proper_time) % 2 == 0:
            glColor3f(1, 1, 1)
            glPointSize(self.size / 2)
            glBegin(GL_POINTS)
            glVertex2fv(self.pos)
            glEnd()

class StaticObject:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def draw(self):
        color = (0, 0, 0)
        glColor3fv(color)
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2fv(self.pos)
        glEnd()
