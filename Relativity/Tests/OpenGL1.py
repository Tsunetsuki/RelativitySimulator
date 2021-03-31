import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def loop(clock):
    d = clock.tick() / 1000
    t = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()


    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(10*t, 0, 0, 1)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glEnd()
    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(10)


    run = not keys[pygame.K_ESCAPE]
    return run

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    run = True
    while run:
        run = loop(clock)
    pygame.quit()
main()