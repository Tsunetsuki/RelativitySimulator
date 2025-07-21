import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Relativity import SpaceTimeObjects, Worldlines, CoordSystem, Canvas


from typing import List, Tuple

from Relativity import SpaceTimeObjects

"""
ESC: Quit
SPACE: Pause
WASD: Move
Arrows: Change Player Velocity (Phi) instantaneously:
    Up: Phi = 0
    Left/Right: Phi = some constant value

"""


ZERO_2D = array([0, 0])

cw = 1600
ch = 900
background_color = (0.8, 0.8, 0.8)
instant_velocity = 0.999

toggles = {
    "paused": False,
    "transform_coords": False,
    "has_controller": False,
    "reset_game": False,
}


def glBall(pos: array, radius):
    sides = 32

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    glBegin(GL_POLYGON)

    for i in range(sides):
        vPos = radius * array([cos((i / sides) * 2 * pi), sin((i / sides) * 2 * pi)])

        glVertex2fv(vPos)

    glEnd()

    glPopMatrix()


def lorentz_transform(phi):
    return array(
        [
            [cosh(phi), -sinh(phi), 0, 0],
            [-sinh(phi), cosh(phi), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def roundedString(x: number, n: int):
    return str(format(x, f".{n}f"))


def maprange(s, a, b):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def draw_clock(t, pos: array, clock_radius: number):
    glPushMatrix()
    glLoadIdentity()
    glTranslate(-1, 1, 0)
    glScale(2 / cw, 2 / ch, 1)
    glScale(1, -1, 1)

    xt, yt = pos
    glTranslate(xt, yt, 0)

    hand_length = clock_radius * 0.8

    angle = -pi / 2 + 2 * pi * t
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
        sec_angle = -pi / 2 + 2 * pi * (sec / 10)
        sec_vector = array([cos(sec_angle), sin(sec_angle)])

        glVertex2fv(sec_vector * clock_radius)
        glVertex2fv(sec_vector * clock_radius * 0.8)

    glEnd()

    glPopMatrix()


def glCircle(pos: array, radius, thickness):
    sides = 32

    glLineWidth(thickness)

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    glBegin(GL_LINE_LOOP)

    for i in range(sides):
        vPos = radius * array([cos((i / sides) * 2 * pi), sin((i / sides) * 2 * pi)])

        glVertex2fv(vPos)

    glEnd()

    glPopMatrix()


def process_controls(player, d):
    run = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggles["paused"] = not toggles["paused"]
            elif event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_t:
                toggles["transform_coords"] = not toggles["transform_coords"]
            elif event.key == pygame.K_r:
                toggles["reset_game"] = True
            elif not toggles["paused"]:
                if event.key == pygame.K_UP:
                    player.reset_velocity()
                elif event.key == pygame.K_LEFT:
                    player.set_phi(arctanh(-instant_velocity))
                elif event.key == pygame.K_RIGHT:
                    player.set_phi(arctanh(instant_velocity))

        elif event.type == pygame.JOYBUTTONDOWN:
            # print(event)
            if event.button == 8:
                toggles["transform_coords"] = not toggles["transform_coords"]
            elif event.button == 5:
                run = False
            elif event.button == 4:
                toggles["reset_game"] = True
            elif event.button == 7:
                toggles["paused"] = not toggles["paused"]

            # elif not toggles["paused"]:
            #    if event.button ==
        elif event.type == pygame.JOYHATMOTION:
            if event.value == (0, 1):
                player.reset_velocity()
            elif event.value == (-1, 0):
                player.set_phi(arctanh(-instant_velocity))
            elif event.value == (1, 0):
                player.set_phi(arctanh(instant_velocity))
        elif event.type == pygame.JOYAXISMOTION:
            pass

    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if toggles["has_controller"]:
        axis0 = pygame.joystick.Joystick(0).get_axis(0)
        axis1 = pygame.joystick.Joystick(0).get_axis(1)
    else:
        axis0, axis1 = 0, 0

    if not toggles["paused"]:
        acc = 0
        MAX_ACC = 2
        deadzone = 0.3
        if abs(axis0) > deadzone:
            acc = maprange(axis0, (deadzone, 1), (0, MAX_ACC))
        elif keys[pygame.K_a] or axis0 < -0.5:
            acc = -MAX_ACC
        elif keys[pygame.K_d] or axis0 > 0.5:
            acc = MAX_ACC

        player.accelerate(d * acc)

    return run


def draw(
    canvas: Canvas,
    coord_system: CoordSystem,
    player,
    npcs,
    static_objects,
    worldlines,
    d,
):

    glPushMatrix()

    phi = player.phi

    lorentzTransform = lorentz_transform(phi)

    r, g, b = background_color
    glClearColor(r, g, b, 255)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # wenn Spieler wieder im Mittelpunkt stehen soll, Worldlines + NPCs nach Transformation zeichnen!

    glPushMatrix()
    # glMultMatrixd(mat_inv(lorentzTransform))
    glTranslated(-player.pos[0], -player.pos[1], 0)
    glPopMatrix()

    if toggles["transform_coords"]:
        glMultMatrixd(lorentzTransform)

    glTranslated(
        -player.pos[0], -player.pos[1], 0
    )  # this is just to follow the player around

    coord_system.draw()

    for worldline in worldlines:
        worldline.draw()

    for npc in npcs:
        pass  # npc.draw()

    for static_object in static_objects:
        static_object.draw()

    player.draw()

    glPopMatrix()

    # UI
    canvas.glText("FPS: " + roundedString(1 / d, 0), 20, 0, (0, 0, 0), (1, 1, 1))
    canvas.glText("Φ: " + roundedString(phi, 2), 20, 25, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("β: " + roundedString(tanh(phi), 8), 20, 50, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("γ: " + roundedString(cosh(phi), 2), 20, 75, (0, 0, 0.8), (1, 1, 1))
    canvas.glText(
        "τ: " + roundedString(player.proper_time, 2), 20, 100, (0, 0, 0.8), (1, 1, 1)
    )
    canvas.glText("Pos: " + str(player.pos.round(2)), 20, 125, (0, 0, 0.8), (1, 1, 1))
    canvas.glText(
        "     " + str((lorentzTransform[:2, :2] @ player.pos).round(2)),
        20,
        150,
        (0, 0, 0.8),
        (1, 1, 1),
    )

    draw_clock(player.proper_time / 10, (cw * 0.9, ch * 0.1), 50)
    # draw_clock(player.proper_time * 10, (cw * 0.9, ch * 0.1), 30)

    pygame.display.flip()


def loop(clock, canvas, coord_system, player, npcs, static_objects, worldlines):
    global toggles

    d = clock.tick() / 1000
    t = pygame.time.get_ticks() / 1000

    run = process_controls(player, d)

    if not toggles["paused"]:

        # move objects
        player.step(d)
        # for npc in npcs:
        #    npc.step(d, player.phi)# * cosh(player.phi))

        # print(f"{npcs[0].phi} - {player.phi} = {npcs[0].phi - player.phi} => γ = {cosh(npcs[0].phi - player.phi)}")

        worldlines[-1].add_point(player.pos, player.proper_time)

    draw(canvas, coord_system, player, npcs, static_objects, worldlines, d)

    return run


def init_game(scale):
    player = SpaceTimeObjects.Player(array([0, 0]), 0, 300 * scale)
    coord_system = CoordSystem.CoordSystem(
        -1000, 1000, 10, -1000, 1000, 10, (0, 0, 0), draw_light_lines=False
    )

    # for i in range(1, 5):
    # worldlines.append(ConstAccelWorldline(1/i))

    npcs = []

    static_objects = [SpaceTimeObjects.StaticObject(array([0, 8]), 400 * scale)]

    worldlines = []

    # for phi in linspace(-5, 5, 2):
    worldlines.append(
        Worldlines.ConstVel1DObjWorldline(array([0, 0]), 0.1, player, 0.5)
    )
    worldlines.append(
        Worldlines.ConstVel1DObjWorldline(array([0, 0]), -0.97, player, 0.5)
    )

    # worldlines.append(Worldlines.ConstVelWorldline(array([-0.5, 0]), beta, player))

    # worldlines.append(ConstVel1DObjWorldline(array([1, 0]), 0.9, player, 2))

    worldlines.append(Worldlines.HistoryWorldLine())

    return coord_system, player, npcs, static_objects, worldlines


def main():
    pygame.init()
    pygame.joystick.init()

    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]

    toggles["has_controller"] = len(joysticks) > 0

    # pygame.joystick.Joystick(0)

    clock = pygame.time.Clock()

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    win = pygame.display.set_mode((cw, ch), DOUBLEBUF | OPENGL)
    glScale(1, cw / ch, 1)
    scale = 0.05
    glScale(scale, scale, scale)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    canvas = Canvas.Canvas((cw, ch), 25)

    coord_system, player, npcs, static_objects, worldlines = init_game(scale)

    run = True
    while run:
        if toggles["reset_game"]:
            coord_system, player, npcs, static_objects, worldlines = init_game(scale)
            toggles["reset_game"] = False

        run = loop(
            clock, canvas, coord_system, player, npcs, static_objects, worldlines
        )
    pygame.quit()


main()
