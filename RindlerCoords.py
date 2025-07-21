from dataclasses import dataclass
from OpenGL.GL import (
    GL_BLEND,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_LINE_LOOP,
    GL_LINES,
    GL_POLYGON,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    glBegin,
    glBlendFunc,
    glClear,
    glClearColor,
    glColor3f,
    glEnable,
    glEnd,
    glLineWidth,
    glLoadIdentity,
    glPopMatrix,
    glPushMatrix,
    glTranslated,
    glTranslatef,
    glVertex2fv,
    glTranslate,
    glScale,
    glMultMatrixd,
)
import numpy as np
from numpy import arctanh, array, sinh, cosh, tanh, sin, cos, pi
from numpy.typing import NDArray
import pygame
from pygame.locals import DOUBLEBUF, GL_MULTISAMPLEBUFFERS, OPENGL

from Relativity import SpaceTimeObjects, Worldlines
from Relativity.Canvas import Canvas
from Relativity.CoordSystem import CoordSystem

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


@dataclass
class GameState:
    coord_system: CoordSystem
    player: SpaceTimeObjects.Player
    npcs: list[SpaceTimeObjects.NPC]
    static_objects: list[SpaceTimeObjects.StaticObject]
    worldlines: list[Worldlines.Worldline]


def glBall(pos: NDArray[np.float_], radius: float) -> None:
    sides = 32

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    glBegin(GL_POLYGON)

    for i in range(sides):
        vPos = radius * array([cos((i / sides) * 2 * pi), sin((i / sides) * 2 * pi)])

        glVertex2fv(vPos)

    glEnd()

    glPopMatrix()


def lorentz_transform(phi: float) -> NDArray[np.float_]:
    return array(
        [
            [cosh(phi), -sinh(phi), 0, 0],
            [-sinh(phi), cosh(phi), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def roundedString(x: float, n: int) -> str:
    return str(format(x, f".{n}f"))


def maprange(s: float, a: tuple[float, float], b: tuple[float, float]) -> float:
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def draw_clock(t: float, pos: tuple[float, float], clock_radius: float) -> None:
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


def glCircle(pos: NDArray[np.float_], radius: float, thickness: float) -> None:
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


def process_controls(player: SpaceTimeObjects.Player, d: float) -> bool:
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

    # mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if toggles["has_controller"]:
        axis0 = pygame.joystick.Joystick(0).get_axis(0)
        _ = pygame.joystick.Joystick(0).get_axis(1)
    else:
        axis0, _ = 0, 0

    if not toggles["paused"]:
        acc = 0.0
        MAX_ACC = 2.0
        deadzone = 0.3
        if abs(axis0) > deadzone:
            acc = maprange(axis0, (deadzone, 1.0), (0.0, MAX_ACC))
        elif keys[pygame.K_a] or axis0 < -0.5:
            acc = -MAX_ACC
        elif keys[pygame.K_d] or axis0 > 0.5:
            acc = MAX_ACC

        player.accelerate(d * acc)

    return run


def draw(
    canvas: Canvas,
    game_state: GameState,
    d: float,
) -> None:

    glPushMatrix()

    phi = game_state.player.phi

    lorentzTransform = lorentz_transform(phi)

    r, g, b = background_color
    glClearColor(r, g, b, 255)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type:ignore

    # wenn Spieler wieder im Mittelpunkt stehen soll, Worldlines + NPCs nach Transformation zeichnen!

    glPushMatrix()
    # glMultMatrixd(mat_inv(lorentzTransform))
    glTranslated(-game_state.player.pos[0], -game_state.player.pos[1], 0)
    glPopMatrix()

    if toggles["transform_coords"]:
        glMultMatrixd(lorentzTransform)

    glTranslated(
        -game_state.player.pos[0], -game_state.player.pos[1], 0
    )  # this is just to follow the player around

    game_state.coord_system.draw()

    for worldline in game_state.worldlines:
        worldline.draw()

    # for npc in npcs:
    #     npc.draw()

    for static_object in game_state.static_objects:
        static_object.draw()

    game_state.player.draw()

    glPopMatrix()

    # UI
    canvas.glText("FPS: " + roundedString(1 / d, 0), 20, 0, (0, 0, 0), (1, 1, 1))
    canvas.glText("Φ: " + roundedString(phi, 2), 20, 25, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("β: " + roundedString(tanh(phi), 8), 20, 50, (0, 0, 0.8), (1, 1, 1))
    canvas.glText("γ: " + roundedString(cosh(phi), 2), 20, 75, (0, 0, 0.8), (1, 1, 1))
    canvas.glText(
        "τ: " + roundedString(game_state.player.proper_time, 2),
        20,
        100,
        (0, 0, 0.8),
        (1, 1, 1),
    )
    canvas.glText(
        "Pos: " + str(game_state.player.pos.round(2)), 20, 125, (0, 0, 0.8), (1, 1, 1)
    )
    canvas.glText(
        "     " + str((lorentzTransform[:2, :2] @ game_state.player.pos).round(2)),
        20,
        150,
        (0, 0, 0.8),
        (1, 1, 1),
    )

    draw_clock(game_state.player.proper_time / 10, (cw * 0.9, ch * 0.1), 50)
    # draw_clock(player.proper_time * 10, (cw * 0.9, ch * 0.1), 30)

    pygame.display.flip()


def loop(clock: pygame.time.Clock, canvas: Canvas, game_state: GameState) -> bool:
    global toggles

    d = clock.tick() / 1000
    # t = pygame.time.get_ticks() / 1000

    run = process_controls(game_state.player, d)

    if not toggles["paused"]:

        # move objects
        game_state.player.step(d)
        # for npc in npcs:
        #    npc.step(d, player.phi)# * cosh(player.phi))

        history_worldline = game_state.worldlines[-1]
        assert isinstance(history_worldline, Worldlines.HistoryWorldLine)

        history_worldline.add_point(
            game_state.player.pos, game_state.player.proper_time
        )

    draw(canvas, game_state, d)

    return run


def init_game(
    scale: float,
) -> GameState:
    player = SpaceTimeObjects.Player(array([0, 0]), 0, 300 * scale)
    coord_system = CoordSystem(
        -1000, 1000, 10, -1000, 1000, 10, (0, 0, 0), draw_light_lines=False
    )

    # for i in range(1, 5):
    # worldlines.append(ConstAccelWorldline(1/i))

    npcs: list[SpaceTimeObjects.NPC] = []

    static_objects = [SpaceTimeObjects.StaticObject(array([0, 8]), 400 * scale)]

    worldlines: list[Worldlines.Worldline] = []

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

    return GameState(coord_system, player, npcs, static_objects, worldlines)


def main() -> None:
    pygame.init()
    pygame.joystick.init()

    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]

    toggles["has_controller"] = len(joysticks) > 0

    # pygame.joystick.Joystick(0)

    clock = pygame.time.Clock()

    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    _ = pygame.display.set_mode((cw, ch), DOUBLEBUF | OPENGL)
    glScale(1, cw / ch, 1)
    scale = 0.05
    glScale(scale, scale, scale)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    canvas = Canvas((cw, ch), 25)

    game_state: GameState = init_game(scale)

    run = True
    while run:
        if toggles["reset_game"]:
            game_state = init_game(scale)
            toggles["reset_game"] = False

        run = loop(clock, canvas, game_state)
    pygame.quit()


if __name__ == "__main__":
    main()
