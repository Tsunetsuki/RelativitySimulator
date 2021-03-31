import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def glBall(pos: array, radius):
    sides = 32

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    glBegin(GL_POLYGON)

    for i in range(sides):
        vPos = radius * array([cos((i / sides) * 2 * pi ), sin((i / sides) * 2 * pi)])

        glVertex2fv(vPos)

    glEnd()

    glPopMatrix()

def glCircle(pos: array, radius, thickness):
    sides = 32

    glLineWidth(thickness)

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    glBegin(GL_LINE_LOOP)

    for i in range(sides):
        vPos = radius * array([cos((i / sides) * 2 * pi ), sin((i / sides) * 2 * pi)])

        glVertex2fv(vPos)

    glEnd()

    glPopMatrix()

'''#object running in time
class STObject:

    def __init__(self):
        self.transformation = identity(4)

    def draw(self, color: array, ):
        pass
'''

class Player:
    def __init__(self, pos: array, size):
        self.pos = pos.astype(float)
        self.size = size
        self.phi = 0
        self.proper_time = 0

    def accelerate(self, d_phi: number):# d_phi = proper acceleration??
        self.phi += d_phi

    def step(self, d):
        gamma = cosh(self.phi)
        beta = tanh(self.phi)
        self.proper_time += d / gamma

        velocity = array([beta, 1])
        self.pos += velocity * d

    def draw(self):
        color = (floor(self.proper_time) % 2, 0.5, 0, 1)
        glColor4fv(color)
        glBall(self.pos, self.size)

# beta/phi are measured from initial FoR, so they remain constant for zero acceleration.
class NPC:
    def __init__(self, pos: array, beta: number, color, size):
        self.pos = pos.astype(float)
        self.size = size
        self.beta = beta
        self.phi = arctanh(beta)
        self.proper_time = 0
        self.color = color

    #d is from the stationary FoR!
    def step(self, d):
        gamma = cosh(self.phi)
        self.proper_time += d / gamma

        velocity = array([self.beta, 1])
        self.pos += velocity * d

    #transformation is only dependent on the player's speed, NOT the nps's speed.
    def draw(self, transformation):
        glColor3fv(self.color)
        glBall(transformation @ self.pos, self.size)

        if floor(self.proper_time) % 2 == 0:
            glColor3f(1, 1, 1)
            glBall(transformation @ self.pos, self.size / 2)