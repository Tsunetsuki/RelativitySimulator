import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class CoordSystem:
    def __init__(self, min_x, max_x, x_spacing, min_y, max_y, y_spacing, color=(0, 0, 0), draw_light_lines=False):#, b1: array, b2: array):
        self.min_x = min_x
        self.max_x = max_x
        self.x_spacing = x_spacing

        self.min_y = min_y
        self.max_y = max_y
        self.y_spacing = y_spacing

        self.color = color
        self.draw_light_lines = draw_light_lines

    def draw(self):
        #grid
        r, g, b = self.color
        glColor4f(r, g, b, 0.5)
        glLineWidth(1)
        glLineStipple(1, 0xF0F0)
        glEnable(GL_LINE_STIPPLE)

        glBegin(GL_LINES)
        for x in range(self.min_x, self.max_x + self.x_spacing, self.x_spacing):
            glVertex2f(x, self.min_y)
            glVertex2f(x, self.max_y)

        for y in range(self.min_y, self.max_y + self.y_spacing, self.y_spacing):
            glVertex2f(self.min_x, y)
            glVertex2f(self.max_x, y)
        glEnd()

        glDisable(GL_LINE_STIPPLE)

        #axes
        glColor4f(r, g, b, 1)
        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex2f(0, self.min_y)
        glVertex2f(0, self.max_y)
        glVertex2f(self.min_x, 0)
        glVertex2f(self.max_x, 0)
        glEnd()

        #light lines
        if self.draw_light_lines:
            glColor4f(1, 1, 0, 1)
            glLineWidth(2)
            glBegin(GL_LINES)
            glVertex2f(self.min_x, self.min_y)
            glVertex2f(self.max_x, self.max_y)
            glVertex2f(self.min_x, self.max_y)
            glVertex2f(self.max_x, self.min_y)
            glEnd()