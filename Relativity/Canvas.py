import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *

class Canvas:
    def __init__(self, canvas_size, font_size):
        pygame.font.init()
        self.font_renderer = pygame.font.Font("res/arial.ttf", font_size)
        self.cw, self.ch = canvas_size

    def glText(self, text, x, y, text_color, background_color):
        text_img = self.font_renderer.render(text, True, [255 * color for color in text_color],
                                        [255 * color for color in background_color])
        img_as_array = transpose(pygame.surfarray.array3d(text_img).astype(uint8), (1, 0, 2))

        iw = text_img.get_width()
        ih = text_img.get_height()

        texture = 0
        glGenTextures(1, texture)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, iw, ih, 0, GL_RGB, GL_UNSIGNED_BYTE, img_as_array)
        glGenerateMipmap(GL_TEXTURE_2D)

        # drawImage(text_img, 0, 0, text_img.get_width(), text_img.get_height(), 0)

        xx = x
        yy = y
        ww = iw
        hh = ih

        # scale = 0.1
        glPushMatrix()
        glLoadIdentity()
        glTranslate(-1, 1, 0)
        glScale(2 / self.cw, 2 / self.ch, 1)
        glScale(1, -1, 1)

        glColor3fv(background_color)

        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(xx, yy)
        glTexCoord2f(0, 1)
        glVertex2f(xx, yy + hh)
        glTexCoord2f(1, 1)
        glVertex2f(xx + ww, yy + hh)
        glTexCoord2f(1, 0)
        glVertex2f(xx + ww, yy)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glDeleteTextures(1, texture)