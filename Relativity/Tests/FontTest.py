import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.font.init()

font_renderer = pygame.font.SysFont("arial", 20)

cw = 1200
ch = 800


def drawImage(filename, xx, yy, ww, hh, angle):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, filename)

    glLoadIdentity()
    glTranslatef(xx, yy, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    glTranslatef(-xx, -yy, 0.0)

    # Draw a textured quad
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(xx, yy)
    glTexCoord2f(0, 1)
    glVertex2f(xx, yy + hh)
    glTexCoord2f(1, 1)
    glVertex2f(xx + ww, yy + hh)
    glTexCoord2f(1, 0)
    glVertex2f(xx + ww, yy)

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glEnd()


def glText(text, x, y, text_color, background_color):
    text_img = font_renderer.render(
        text,
        True,
        [255 * color for color in text_color],
        [255 * color for color in background_color],
    )
    img_as_array = np.transpose(
        pygame.surfarray.array3d(text_img).astype(np.uint8), (1, 0, 2)
    )

    iw = text_img.get_width()
    ih = text_img.get_height()

    # print(img_as_array.shape)
    # print(type(img_as_array[0, 0, 0].astype(byte)))

    texture = 0
    glGenTextures(1, texture)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, iw, ih, 0, GL_RGB, GL_UNSIGNED_BYTE, img_as_array
    )
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
    glScale(2 / cw, 2 / ch, 1)
    glScale(1, -1, 1)
    # glTranslate(-9, sin(t), 0)

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


def loop(clock):
    d = clock.tick() / 1000
    t = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    glClearColor(0.8, 0.8, 0.8, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(10 * t, 0, 0, 1)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glEnd()
    glPopMatrix()

    # Text Rendering
    glText("Yolo: 500000 FPS", 10, 10, (0, 0, 0), (0.8, 0.8, 0.8))

    pygame.display.flip()

    run = not keys[pygame.K_ESCAPE]
    return run


def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = (cw, ch)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL, 32)

    glScale(1, cw / ch, 1)
    scale = 0.1
    glScale(scale, scale, scale)

    run = True
    while run:
        run = loop(clock)
    pygame.quit()


main()
