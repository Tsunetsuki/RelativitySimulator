import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import freetype

cw = 1200
ch = 800


def draw():
    pygame.display.flip()


def loop(clock):
    d = clock.tick() / 1000
    t = pygame.time.get_ticks() / 1000
    run = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    draw()

    return run


def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    win = pygame.display.set_mode((cw, ch), DOUBLEBUF | OPENGL)
    glScale(1, cw / ch, 1)
    scale = 0.1
    glScale(scale, scale, scale)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    pygame.event.pump()

    run = True
    while run:
        run = loop(clock)

        face = freetype.Face("./arial.ttf")
        face.set_char_size(48 * 64)
        face.load_char("S")
        bitmap = face.glyph.bitmap
        bitmap.buffer
    pygame.quit()


main()
