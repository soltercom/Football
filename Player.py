from random import randint

from Ball import Ball
from Util import Vector, Rectangle


class Player:
    RADIUS = 10

    COLOR1 = "#80d6ff"
    COLOR2 = "#ff867c"
    OUTLINE = "#000000"

    @property
    def right(self):
        return self.pos.sub(Vector(Player.RADIUS, 0))

    @property
    def left(self):
        return self.pos.add(Vector(Player.RADIUS, 0))

    @property
    def color(self):
        if self.team == 1:
            return Player.COLOR1
        elif self.team == 2:
            return Player.COLOR2

    def __init__(self, canvas, team):
        self.canvas = canvas
        self.team = team
        self.pos = Vector(0, 0)
        self.old_pos = Vector(0, 0)
        self.shape = None

    def set(self, v):
        self.old_pos = self.pos
        self.pos = v
        self.paint()

    def move(self, v: Vector):
        self.set(self.pos.add(v))

    def move_to_point(self, point: Vector):
        v = randint(1, 10) / 10
        self.move(point.sub(self.pos).norm().mul(Vector(v, v)))

    def get_ball(self, ball):
        if self.team == 1:
            ball.set(self.right)
        elif self.team == 2:
            ball.set(self.left)

    def paint(self):
        if self.shape is None:
            self.shape = self.canvas.create_rectangle(-Player.RADIUS, -Player.RADIUS, Player.RADIUS, Player.RADIUS,
                                                      outline=Player.OUTLINE, fill=self.color)
        delta = self.pos.sub(self.old_pos)
        self.canvas.move(self.shape, delta.x, delta.y)

    def rectangle(self) -> Rectangle:
        return self.pos.rect(Player.RADIUS)

    def ball_hit_test(self, ball: Ball) -> bool:
        return self.rectangle().hit(ball.pos)
