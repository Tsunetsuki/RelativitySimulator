import numpy as np
from numpy import (
    arctan2,
    arctanh,
    array,
    linalg,
    linspace,
    sinh,
    cosh,
    sin,
    cos,
    pi,
    floor,
)
from numpy.linalg import inv as mat_inv
from numpy.typing import NDArray
from OpenGL.GL import (
    GL_LINE_STRIP,
    GL_LINES,
    GL_POINTS,
    glBegin,
    glColor3f,
    glColor3fv,
    glColor4f,
    glEnd,
    glLineWidth,
    glPointSize,
    glPopMatrix,
    glPushMatrix,
    glVertex2f,
    glVertex2fv,
    glTranslate,
    glMultMatrixd,
)

from Relativity.SpaceTimeObjects import Player


ZERO_2D = array([0, 0])


def intersecc(
    a: NDArray[np.float_],
    u: NDArray[np.float_],
    b: NDArray[np.float_],
    v: NDArray[np.float_],
) -> tuple[float, float]:
    row1 = array([u[0], -v[0]])
    row2 = array([u[1], -v[1]])
    consts = array([-a[0] + b[0], -a[1] + b[1]])

    myMat = array([row1, row2])

    t1, t2 = linalg.solve(myMat, consts)

    return t1, t2


def lorentz_transform(phi: float) -> NDArray[np.float_]:
    return array(
        [
            [cosh(phi), -sinh(phi), 0, 0],
            [-sinh(phi), cosh(phi), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def draw_clock(t: float, pos: NDArray[np.float_], clock_radius: float) -> None:
    glPushMatrix()

    xt, yt = pos
    glTranslate(xt, yt, 0)

    hand_length = clock_radius * 0.01
    angle = -pi / 2 + 2 * pi * t
    hand_vector = array([hand_length * cos(angle), -hand_length * sin(angle)])

    # outer circle
    glColor3f(0.4, 0.2, 0)
    glPointSize(clock_radius)
    glBegin(GL_POINTS)
    glVertex2fv(ZERO_2D)
    glEnd()

    # inner circle
    glColor3f(1, 1, 1)
    glPointSize(clock_radius * 0.9)
    glBegin(GL_POINTS)
    glVertex2fv(ZERO_2D)
    glEnd()

    # hand
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2fv(ZERO_2D)
    glVertex2fv(ZERO_2D + hand_vector)
    glEnd()

    # ticks around clock

    # glMultMatrixd(lorentz_transform(self.player.phi))
    glBegin(GL_LINES)
    for sec in range(0, 10):
        sec_angle = -pi / 2 + 2 * pi * (sec / 10)
        sec_vector = array([cos(sec_angle), sin(sec_angle)])

        glVertex2fv(sec_vector * hand_length * 1.1)
        glVertex2fv(sec_vector * hand_length * 0.9)

    glEnd()

    glPopMatrix()


class Worldline:
    def draw(self) -> None:
        pass


class ConstAccelWorldline(Worldline):
    def __init__(self, proper_acc: float) -> None:
        self.proper_acc = proper_acc

    def draw(self) -> None:
        glColor4f(1, 0, 0, 1)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)

        for proper_time in linspace(-5, 5, 100):
            x = (1 / self.proper_acc) * cosh(self.proper_acc * proper_time)
            t = (1 / self.proper_acc) * sinh(self.proper_acc * proper_time)
            glVertex2f(x, t)
        glEnd()


class ConstVelWorldline(Worldline):
    def __init__(
        self, start_pos: NDArray[np.float_], beta: float, player: Player
    ) -> None:
        self.start_pos = start_pos
        self.beta = beta
        self.phi = arctanh(beta)
        self.gamma = cosh(self.phi)
        self.velocity = self.gamma * array([self.beta, 1])
        self.player = player

    def draw(self) -> None:
        self.draw_line()
        # draw NPC on appropriate position on worldline
        self.draw_npc()
        # self.draw_lightlines()

    def draw_line(self) -> None:
        glColor4f(0, 0.4, 0.8, 1)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2fv(self.start_pos - self.velocity * 100)
        glVertex2fv(self.start_pos + self.velocity * 100)
        glEnd()

        glColor3f(1, 0, 0)
        glPointSize(7)
        glBegin(GL_POINTS)
        # for marker in range(-100, 100):
        #    glVertex2fv(self.start_pos + self.velocity * marker)
        glEnd()

    def draw_npc(self) -> None:
        size = 20
        color = (0.8, 0, 1)

        # player_angle = arctan2(
        #     self.player.pos[1 - self.start_pos[1]],
        #     self.player.pos[0] - self.start_pos[0],
        # )
        # worldline_angle = arctan2(self.velocity[1], self.velocity[0])

        player_past_direction = self.player.get_basis_x()
        # player_past_direction = array([1, 1]) if player_angle < worldline_angle else array([-1, 1])

        proper_time, t2 = intersecc(
            self.start_pos, self.velocity, self.player.pos, player_past_direction
        )

        pos = self.start_pos + self.velocity * proper_time

        # self.draw_clock(proper_time, pos, 50)

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

    def draw_lightlines(self) -> None:
        velocityLightLeft = array([-1, 1])
        velocityLightRight = array([1, 1])

        glColor3f(1, 1, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        for lightbeam in range(-100, 100):
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(
                self.start_pos + self.velocity * lightbeam + velocityLightLeft * 100
            )
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(
                self.start_pos + self.velocity * lightbeam + velocityLightRight * 100
            )
        glEnd()


class ConstVel1DObjWorldline(Worldline):
    def __init__(
        self,
        start_pos: NDArray[np.float_],
        beta: float,
        player: Player,
        proper_length: float,
    ) -> None:
        self.start_pos = start_pos
        self.beta = beta
        self.phi = arctanh(beta)
        self.gamma = cosh(self.phi)
        self.velocity = self.gamma * array([self.beta, 1])
        self.player = player
        self.length = proper_length  # from initial rest frame

    def draw(self) -> None:
        self.draw_lines()
        self.draw_obj(draw_along_lightbeams=False)

    def draw_lines(self) -> None:
        for tip_start_pos in [self.start_pos, self.start_pos + array([self.length, 0])]:
            glColor4f(0, 0.4, 0.8, 1)
            glLineWidth(2)
            glBegin(GL_LINES)
            glVertex2fv(tip_start_pos - self.velocity * 100)
            glVertex2fv(tip_start_pos + self.velocity * 100)
            glEnd()

            # glColor3f(1, 0, 0)
            # glPointSize(7)
            # glBegin(GL_POINTS)
            # for marker in range(-100, 100):
            #    glVertex2fv(tip_start_pos + self.velocity * marker)
            # glEnd()

        # self.draw_lightlines()

    def draw_obj(self, draw_along_lightbeams: bool) -> None:
        size = 5
        color = (0.7, 0.4, 0)

        worldline_angle = arctan2(self.velocity[1], self.velocity[0])

        player_vertex_in_between = False

        tip_1_start_pos = self.start_pos
        tip_2_start_pos = self.start_pos + array([self.length, 0])
        player_angle_1 = arctan2(
            self.player.pos[1] - tip_1_start_pos[1],
            self.player.pos[0] - tip_1_start_pos[0],
        )
        player_angle_2 = arctan2(
            self.player.pos[1] - tip_2_start_pos[1],
            self.player.pos[0] - tip_2_start_pos[0],
        )

        if draw_along_lightbeams:
            player_past_direction_1 = (
                array([1, 1]) if player_angle_1 < worldline_angle else array([-1, 1])
            )
            player_past_direction_2 = (
                array([1, 1]) if player_angle_2 < worldline_angle else array([-1, 1])
            )
            player_vertex_in_between = not (
                player_past_direction_1 == player_past_direction_2
            ).all()
        else:
            player_past_direction_1 = self.player.get_basis_x()
            player_past_direction_2 = self.player.get_basis_x()

        proper_time_1, _ = intersecc(
            tip_1_start_pos, self.velocity, self.player.pos, player_past_direction_1
        )
        proper_time_2, _ = intersecc(
            tip_2_start_pos, self.velocity, self.player.pos, player_past_direction_2
        )
        pos1 = tip_1_start_pos + self.velocity * proper_time_1
        pos2 = tip_2_start_pos + self.velocity * proper_time_2

        # line
        glColor3fv(color)
        glLineWidth(size)
        glBegin(GL_LINE_STRIP)
        glVertex2fv(pos1)
        if player_vertex_in_between:
            glVertex2fv(self.player.pos)
        glVertex2fv(pos2)
        glEnd()

        # end points
        # self.draw_clock(proper_time_1 / 10, pos1, 30)
        # self.draw_clock(proper_time_2 / 10, pos2, 30)

        # glColor3f(0, 0, 0)
        # glPointSize(size)
        # glBegin(GL_POINTS)
        # glVertex2fv(pos1)
        # glVertex2fv(pos2)
        # glEnd()

        # if floor(proper_time) % 2 == 0:
        #    glColor3f(1, 1, 1)
        #    glPointSize(size / 2)
        #    glBegin(GL_POINTS)
        #    glVertex2fv(pos)
        #    glEnd()

    def draw_lightlines(self) -> None:
        velocityLightLeft = array([-1, 1])
        velocityLightRight = array([1, 1])

        glColor3f(1, 1, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        for lightbeam in range(-100, 100):
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(
                self.start_pos + self.velocity * lightbeam + velocityLightLeft * 100
            )
            glVertex2fv(self.start_pos + self.velocity * lightbeam)
            glVertex2fv(
                self.start_pos + self.velocity * lightbeam + velocityLightRight * 100
            )
        glEnd()

    def draw_clock(
        self, t: float, pos: NDArray[np.float_], clock_radius: float
    ) -> None:
        glPushMatrix()

        xt, yt = pos
        glTranslate(xt, yt, 0)

        hand_length = clock_radius * 0.01
        angle = -pi / 2 + 2 * pi * t
        hand_vector = array([hand_length * cos(angle), -hand_length * sin(angle)])

        # outer circle
        glColor3f(0.4, 0.2, 0)
        glPointSize(clock_radius)
        glBegin(GL_POINTS)
        glVertex2fv(ZERO_2D)
        glEnd()

        # inner circle
        glColor3f(1, 1, 1)
        glPointSize(clock_radius * 0.9)
        glBegin(GL_POINTS)
        glVertex2fv(ZERO_2D)
        glEnd()

        # hand
        glMultMatrixd(mat_inv(lorentz_transform(self.player.phi)))
        glColor3f(0, 0, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2fv(ZERO_2D)
        glVertex2fv(ZERO_2D + hand_vector)
        glEnd()

        # ticks around clock
        glBegin(GL_LINES)
        for sec in range(0, 10):
            sec_angle = -pi / 2 + 2 * pi * (sec / 10)
            sec_vector = array([cos(sec_angle), sin(sec_angle)])

            glVertex2fv(sec_vector * hand_length * 1.1)
            glVertex2fv(sec_vector * hand_length * 0.9)

        glEnd()

        glPopMatrix()


class HistoryWorldLine(Worldline):
    def __init__(self) -> None:
        self.points: list[tuple[NDArray[np.float_], float]] = []

    def add_point(self, point: NDArray[np.float_], proper_time: float) -> None:
        self.points.append((np.copy(point), proper_time))

        last_index = 0
        for i, pt in enumerate(reversed(self.points)):
            if pt[1] < proper_time - 1:
                last_index = len(self.points) - i
                break

        del self.points[:last_index]

    def draw(self) -> None:
        glLineWidth(4)

        glBegin(GL_LINE_STRIP)
        for pos, proper_time in self.points:
            glColor4f(floor(proper_time) % 2, 0.5, 0, 1)
            glVertex2fv(pos)
        glEnd()
