from OpenGL.GL import (
    GL_LINE_STIPPLE,
    GL_LINES,
    glBegin,
    glColor4f,
    glDisable,
    glEnable,
    glEnd,
    glLineStipple,
    glLineWidth,
    glBegin,
    glEnable,
    glEnd,
    glVertex2f,
)


class CoordSystem:
    def __init__(
        self,
        min_x: int,
        max_x: int,
        x_spacing: int,
        min_y: int,
        max_y: int,
        y_spacing: int,
        color: tuple[int, int, int] = (0, 0, 0),
        draw_light_lines: bool = False,
    ) -> None:  # , b1: array, b2: array):
        self.min_x = min_x
        self.max_x = max_x
        self.x_spacing = x_spacing

        self.min_y = min_y
        self.max_y = max_y
        self.y_spacing = y_spacing

        self.color = color
        self.draw_light_lines = draw_light_lines

    def draw(self) -> None:
        # grid
        r, g, b = self.color
        glColor4f(r, g, b, 0.3)
        glLineWidth(1)
        glLineStipple(1, 0xF0F0)
        glEnable(GL_LINE_STIPPLE)

        glBegin(GL_LINES)
        for x in range(self.min_x, self.max_x + self.x_spacing, self.x_spacing):
            glVertex2f(x, self.min_y)
            glVertex2f(x, self.max_y)

        for y in range(self.min_y, self.max_y + self.y_spacing, self.y_spacing):
            glVertex2f(self.min_x, y)
            glVertex2f(self.max_x, y)
        glEnd()

        glDisable(GL_LINE_STIPPLE)

        # axes
        glColor4f(r, g, b, 1)
        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex2f(0, self.min_y)
        glVertex2f(0, self.max_y)
        glVertex2f(self.min_x, 0)
        glVertex2f(self.max_x, 0)
        glEnd()

        # light lines
        if self.draw_light_lines:
            glColor4f(1, 1, 0, 1)
            glLineWidth(2)
            glBegin(GL_LINES)
            glVertex2f(self.min_x, self.min_y)
            glVertex2f(self.max_x, self.max_y)
            glVertex2f(self.min_x, self.max_y)
            glVertex2f(self.max_x, self.min_y)
            glEnd()
