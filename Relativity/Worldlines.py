import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class ConstAccelWorldline:
    def __init__(self, proper_acc):
        self.proper_acc = proper_acc

    def draw(self):

        glColor4f(1, 0, 0, 1)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)

        for proper_time in linspace(-5, 5, 100):
            x = (1 / self.proper_acc) * cosh(self.proper_acc * proper_time)
            t = (1 / self.proper_acc) * sinh(self.proper_acc * proper_time)
            glVertex2f(x, t)
        glEnd()

class ConstVelWorldline:
    def __init__(self, start_pos: array, beta):
        self.start_pos = start_pos
        self.beta = beta
        self.phi = arctanh(beta)

    def draw(self):
        velocity = array([self.beta, 1])

        glColor4f(0, 0.8, 0, 1)
        glLineWidth(2)
        glBegin(GL_LINES)

        glVertex2fv(self.start_pos - velocity * 100)
        glVertex2fv(self.start_pos + velocity * 100)

        glEnd()

class HistoryWorldLine:
    def __init__(self):
        self.points = []

    def addPoint(self, point: array, proper_time):
        self.points.append((copy(point), proper_time))

        last_index = 0
        for i, point in enumerate(self.points):
            if point[1] > proper_time - 3:
                last_index = i
                break

        del self.points[:last_index]

    def draw(self):

        glLineWidth(3)

        glBegin(GL_LINE_STRIP)
        for pos, proper_time in self.points:
            glColor4f(floor(proper_time) % 2, 0.5, 0, 1)
            glVertex2fv(pos)
        glEnd()