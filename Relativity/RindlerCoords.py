import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Relativity.SpaceTimeObjects import *
from Relativity.CoordSystem import *
from Relativity.Worldlines import *
from Relativity.Canvas import *

ZERO_2D = array([0, 0])


cw = 1200
ch = 800
background_color = (0.8, 0.8, 0.8)

def roundedString(x: number, n: int):
    return str(round(x, n))

def draw_clock(t):
    glPushMatrix()
    glLoadIdentity()
    glTranslate(-1, 1, 0)
    glScale(2 / cw, 2 / ch, 1)
    glScale(1, -1, 1)

    glTranslate(cw * .9, ch * .10, 0)

    clock_radius = 50
    hand_length = 40

    angle = - pi / 2 + 2 * pi * t
    hand_vector = array([hand_length * cos(angle), hand_length * sin(angle)])

    glColor3f(1, 1, 1)
    glBall(ZERO_2D, clock_radius)
    glColor3f(0.4, 0.2, 0)
    glCircle(ZERO_2D, clock_radius, 4)

    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2fv(ZERO_2D)
    glVertex2fv(ZERO_2D + hand_vector)

    for sec in range(0, 10):
        sec_angle = - pi / 2 + 2 * pi * (sec / 10)
        sec_vector = array([cos(sec_angle),sin(sec_angle)])

        glVertex2fv(sec_vector * clock_radius)
        glVertex2fv(sec_vector * clock_radius * 0.8)

    glEnd()

    glPopMatrix()

def process_controls(keys, player, phi, d):
    acc = 1

    if keys[pygame.K_a]:
        phi -= d
        player.accelerate(-d * acc)
    if keys[pygame.K_d]:
        phi += d
        player.accelerate(d * acc)

    return phi

def draw(canvas, coord_system, player, npcs, worldlines, t, phi):
    glPushMatrix()

    lorentzTransform = array([[cosh(phi), -sinh(phi), 0, 0],
                              [-sinh(phi), cosh(phi), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

    r, g, b = background_color
    glClearColor(r, g, b, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glTranslate(-player.pos[0], -player.pos[1], 0)

    coord_system.draw()


    player.draw()

    for worldline in worldlines:
        worldline.draw()

    for npc in npcs:
        npc.draw([[1, 0], [0, 1]])  # lorentzTransform[:2, :2])


    # wenn Spieler wieder im Mittelpunkt stehen soll, Worldlines + NPCs nach Transformation zeichnen!
    glTranslate(player.pos[0], player.pos[1], 0)
    glMultMatrixf(lorentzTransform)
    glColor3f(1, 0, 0)
    #glCircle(ZERO_2D, 1, 3)


    glPopMatrix()

    #UI
    canvas.glText("Φ: " + roundedString(phi, 2), 20, 25, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("β:  " + roundedString(tanh(phi), 2), 20, 50, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("γ:  " + roundedString(cosh(phi), 2), 20, 75, (0, 0, 0.8), (1, 1, 1))
    draw_clock(player.proper_time)

    pygame.display.flip()



def loop(clock, canvas, coord_system, player, npcs, worldlines, phi):
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

    phi = process_controls(keys, player, phi, d)

    #move objects
    player.step(d)
    for npc in npcs:
        npc.step(d)

    worldlines[-1].addPoint(player.pos, player.proper_time)

    draw(canvas, coord_system, player, npcs, worldlines, t, phi)


    return (run, phi)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    win = pygame.display.set_mode((cw, ch), DOUBLEBUF | OPENGL)
    glScale(1, cw/ch, 1)
    scale = 0.1
    glScale(scale, scale, scale)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    canvas = Canvas((cw, ch), 25)

    player = Player(array([0, 0]), 0.3)
    coord_system = CoordSystem(-1000, 1000, 1, -1000, 1000, 1, (0, 0, 0), draw_light_lines=False)

    worldlines = []
    #for i in range(1, 5):
    #    worldlines.append(ConstAccelWorldline(1/i))

    npcs = [NPC(array([2, 0]), 0.5, (0.5, 0, 0.5), 0.2),
            NPC(array([3, 0]), 0.5, (0.5, 0, 0.5), 0.2),]

    for npc in npcs:
        worldlines.append(ConstVelWorldline(npc.pos, npc.beta))

    worldlines.append(HistoryWorldLine())

    phi = 0
    #coord_system_transformed = CoordSystem(-100, 100, 1, -100, 100, 1, (0, 0.4, 0), False)

    run = True
    while run:
        run, phi = loop(clock, canvas, coord_system, player, npcs, worldlines, phi)
    pygame.quit()

main()

