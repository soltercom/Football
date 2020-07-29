from random import randint

from Ball import Ball
from Field import Field
from Util import Rectangle, Vector


class Goalkeeper:
    RADIUS = 10
    COLOR1 = "#0077c2"
    COLOR2 = "#b61827"

    @property
    def left(self):
        return self.pos.sub(Vector(Goalkeeper.RADIUS, 0))

    @property
    def right(self):
        return self.pos.add(Vector(Goalkeeper.RADIUS, 0))

    @property
    def color(self):
        if self.team == 1:
            return Goalkeeper.COLOR1
        elif self.team == 2:
            return Goalkeeper.COLOR2

    def __init__(self, canvas, team):
        self.canvas = canvas
        self.team = team
        self.pos = Vector(0, 0)
        self.old_pos = Vector(0, 0)
        self.shape = None
        self.miss_ball = False

    def set(self, new_pos):
        self.old_pos = self.pos
        self.pos = new_pos
        self.paint()

    def get_ball(self, ball, team):
        if team == 1:
            ball.set(self.right)
        elif team == 2:
            ball.set(self.left)

    def move_to_ball_y(self, ball: Ball, field: Field):
        if field.goal_start_y <= ball.pos.y <= field.goal_end_y:
            y = field.center_y + (ball.pos.y - field.center_y) / 2
            self.set(Vector(self.pos.x, y))

    def set_on_center(self, field: Field):
        if self.team == 1:
            self.set(Vector(field.start_x + Field.BOX / 3, field.center_y))
        elif self.team == 2:
            self.set(Vector(field.end_x - Field.BOX / 3, field.center_y))

    def ball_hit_test(self, ball: Ball) -> bool:
        if not self.miss_ball and self.rectangle().hit(ball.pos):
            if randint(0, 5) == 3:
                self.miss_ball = True
                return False
            else:
                ball.rebound_x()
                return True
        else:
            return False

    def paint(self):
        if self.shape is None:
            self.shape = self.canvas.create_rectangle(- Goalkeeper.RADIUS, - Goalkeeper.RADIUS,
                                                      Goalkeeper.RADIUS, Goalkeeper.RADIUS,
                                                      outline='black', fill=self.color)
        delta = self.pos.sub(self.old_pos)
        self.canvas.move(self.shape, delta.x, delta.y)

    def rectangle(self) -> Rectangle:
        return self.pos.rect(Goalkeeper.RADIUS)