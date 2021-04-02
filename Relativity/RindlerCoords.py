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
from typing import List, Tuple

'''
ESC: Quit
SPACE: Pause
WASD: Move
Arrows: Change Player Velocity (Phi) instantaneously:
    Up: Phi = 0
    Left/Right: Phi = some constant value

'''


ZERO_2D = array([0, 0])

cw = 1200
ch = 800
background_color = (0.8, 0.8, 0.8)
instant_velocity = 0.968

paused = False

#multiply a 3x2 matrix with 2-Vector to get another 2-Vector
def matMulHom(matrix: array, pos: array):
    pos2 = array([pos[0], pos[1], 1])
    return array([pos[0], pos[1], 1])

def roundedString(x: number, n: int):
    return str(format(x, f".{n}f"))

def draw_clock(t, pos: array, clock_radius: number):
    glPushMatrix()
    glLoadIdentity()
    glTranslate(-1, 1, 0)
    glScale(2 / cw, 2 / ch, 1)
    glScale(1, -1, 1)

    xt, yt = pos
    glTranslate(xt, yt, 0)

    hand_length = clock_radius * 0.8

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

def process_controls(player, d, paused):
    run = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                player.reset_velocity()
            elif event.key == pygame.K_LEFT:
                player.set_phi(arctanh(-instant_velocity))
            elif event.key == pygame.K_RIGHT:
                player.set_phi(arctanh(instant_velocity))




    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    if not paused:
        acc = 1

        if keys[pygame.K_a]:
            player.accelerate(-d * acc)
        if keys[pygame.K_d]:
            player.accelerate(d * acc)

    return run, paused

def draw(canvas: Canvas, coord_system: CoordSystem, player: Player, npcs: List[NPC], static_objects: List[StaticObject], worldlines: List[Worldline], t, d):
    glPushMatrix()

    phi = player.phi

    lorentzTransform = array([[cosh(phi), -sinh(phi), 0, 0],
                              [-sinh(phi), cosh(phi), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

    r, g, b = background_color
    glClearColor(r, g, b, 255)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    # wenn Spieler wieder im Mittelpunkt stehen soll, Worldlines + NPCs nach Transformation zeichnen!

    glPushMatrix()
    glMultMatrixd(lorentzTransform)
    glTranslated(-player.pos[0], -player.pos[1], 0)
    glPopMatrix()


    #glMultMatrixd(lorentzTransform)
    glTranslated(-player.pos[0], -player.pos[1], 0)#this is just to follow the player around


    coord_system.draw()
    player.draw()

    for worldline in worldlines:
        worldline.draw()

    for npc in npcs:
        pass#npc.draw()

    for static_object in static_objects:
        static_object.draw()

    glPopMatrix()

    #UI
    canvas.glText("FPS: " + roundedString(1 / d, 0), 20, 0, (0, 0, 0), (1, 1, 1))
    canvas.glText("Φ: " + roundedString(phi, 2), 20, 25, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("β: " + roundedString(tanh(phi), 2), 20, 50, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("γ: " + roundedString(cosh(phi), 2), 20, 75, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("τ: " + roundedString(player.proper_time, 2), 20, 100, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("Pos: " + str(player.pos.round(2)), 20, 125, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("     " + str((lorentzTransform[:2, :2] @ player.pos).round(2)), 20, 150, (0, 0, 0.8), (1, 1, 1))


    draw_clock(player.proper_time, (cw * 0.9, ch * 0.1), 50)
    #draw_clock(player.proper_time * 10, (cw * 0.9, ch * 0.1), 30)

    pygame.display.flip()



def loop(clock, canvas, coord_system, player, npcs, static_objects, worldlines):
    global paused

    d = clock.tick() / 1000
    t = pygame.time.get_ticks() / 1000

    run, paused = process_controls(player, d, paused)

    if not paused:

        #move objects
        player.step(d)
        for npc in npcs:
            npc.step(d, player.phi)# * cosh(player.phi))

        #print(f"{npcs[0].phi} - {player.phi} = {npcs[0].phi - player.phi} => γ = {cosh(npcs[0].phi - player.phi)}")

        worldlines[-1].add_point(player.pos, player.proper_time)

    draw(canvas, coord_system, player, npcs, static_objects, worldlines, t, d)

    return (run)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    win = pygame.display.set_mode((cw, ch), DOUBLEBUF | OPENGL)
    glScale(1, cw/ch, 1)
    scale = 0.05
    glScale(scale, scale, scale)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    canvas = Canvas((cw, ch), 25)

    player = Player(array([0, 0]),00, 300 * scale)
    coord_system = CoordSystem(-1000, 1000, 1, -1000, 1000, 1, (0, 0, 0), draw_light_lines=True)

    #for i in range(1, 5):
        #worldlines.append(ConstAccelWorldline(1/i))

    npcs = [NPC(array([0, 0]), 0, (0.5, 0, 0.5), 300 * scale)]
        #NPC(array([2, 0]), 0.5, (0.5, 0, 0.5), 200 * scale),
            #NPC(array([3, 0]), 0.5, (0.5, 0, 0.5), 200 * scale),
            #NPC(array([6, 0]), 0, (0, 0, 0.5), 200 * scale)]

    static_objects = [StaticObject(array([0, 8]), 400 * scale)]


    worldlines = []
    for npc in npcs:
        worldlines.append(ConstVelWorldline(npc.pos.copy(), npc.beta))

    worldlines.append(HistoryWorldLine())

    #coord_system_transformed = CoordSystem(-100, 100, 1, -100, 100, 1, (0, 0.4, 0), False)

    run = True
    while run:
        run = loop(clock, canvas, coord_system, player, npcs, static_objects, worldlines)
    pygame.quit()

main()

