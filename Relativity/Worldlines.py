import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

ZERO_2D = array([0, 0])

def intersecc(a, u, b, v):
    row1 = array([u[0], -v[0]])
    row2 = array([u[1], -v[1]])
    consts = array([-a[0] + b[0], -a[1] + b[1]])

    myMat = array([row1, row2])

    t1, t2 = linalg.solve(myMat, consts)

    return t1, t2

class Worldline:
    pass

class ConstAccelWorldline(Worldline):
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

class ConstVelWorldline(Worldline):
    def __init__(self, start_pos: array, beta, player):
        self.start_pos = start_pos
        self.beta = beta
        self.phi = arctanh(beta)
        self.gamma = cosh(self.phi)
        self.velocity = self.gamma * array([self.beta, 1])
        self.player = player


    def draw(self):
        glColor4f(0, 0.4, 0.8, 1)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2fv(self.start_pos - self.velocity * 100)
        glVertex2fv(self.start_pos + self.velocity * 100)
        glEnd()

        glColor3f(1, 0, 0)
        glPointSize(7)
        glBegin(GL_POINTS)
        for marker in range(-100, 100):
            glVertex2fv(self.start_pos + self.velocity * marker)
        glEnd()

        #draw NPC on appropriate position on worldline
        self.draw_npc()

        #self.draw_lightlines()

    def draw_npc(self):
        size = 20
        color = (0.8, 0, 1)

        player_angle = arctan2(self.player.pos[1 - self.start_pos[1]], self.player.pos[0] - self.start_pos[0])
        worldline_angle = arctan2(self.velocity[1], self.velocity[0])

        #player_past_direction = self.player.get_basis_x()
        player_past_direction = array([1, 1]) if player_angle < worldline_angle else array([-1, 1])

        proper_time, t2 = intersecc(self.start_pos, self.velocity, self.player.pos, player_past_direction)

        pos = self.start_pos + self.velocity * proper_time

        #self.draw_clock(proper_time, pos, 50)

        glColor3fv(color)
        glPointSize(size)

        glBegin(GL_POINTS)
        glVertex2fv(pos)
        glEnd()

        if floor(proper_time) % 2 == 0:
            glColor3f(1, 1, 1)
            glPointSize(size / 2)
            glBegin(GL_POINTS)
            glVertex2fv(pos)
            glEnd()


    def draw_lightlines(self):
        velocityLightLeft = array([-1, 1])
        velocityLightRight = array([1, 1])

        glColor3f(1, 1, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        for lightbeam in range(-100, 100):
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(self.start_pos + self.velocity * lightbeam + velocityLightLeft * 100)
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(self.start_pos + self.velocity * lightbeam + velocityLightRight * 100)
        glEnd()

    def draw_clock(self, t, pos: array, clock_radius: number):
        glPushMatrix()

        xt, yt = pos
        glTranslate(xt, yt, 0)

        hand_length = clock_radius * 0.01

        angle = - pi / 2 + 2 * pi * t
        hand_vector = array([hand_length * cos(angle), -hand_length * sin(angle)])



        glColor3f(0.4, 0.2, 0)
        glPointSize(clock_radius)
        glBegin(GL_POINTS)
        glVertex2fv(ZERO_2D)
        glEnd()

        glColor3f(1, 1, 1)
        glPointSize(clock_radius * 0.9)
        glBegin(GL_POINTS)
        glVertex2fv(ZERO_2D)
        glEnd()


        glColor3f(0, 0, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2fv(ZERO_2D)
        glVertex2fv(ZERO_2D + hand_vector)

        for sec in range(0, 10):
            sec_angle = - pi / 2 + 2 * pi * (sec / 10)
            sec_vector = array([cos(sec_angle), sin(sec_angle)])

            glVertex2fv(sec_vector * hand_length * 1.1)
            glVertex2fv(sec_vector * hand_length * 0.9)


        glEnd()

        glPopMatrix()






class HistoryWorldLine(Worldline):
    def __init__(self):
        self.points = []

    def add_point(self, point: array, proper_time):
        self.points.append((copy(point), proper_time))

        last_index = 0
        for i, point in enumerate(self.points):
            if point[1] > proper_time - 5:
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