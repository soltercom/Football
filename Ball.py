from random import randint

from Field import Field
from Util import Vector


class Ball:
    RADIUS = 5
    COLOR = "#ffff72"
    OUTLINE = "#c41c00"

    def __init__(self, canvas, field: Field):
        self.field = field
        self.canvas = canvas
        self.pos = Vector(0, 0)
        self.old_pos = Vector(0, 0)
        self.v = Vector(0, 0)
        self.shape = None

    def move(self):
        self.old_pos = self.pos
        self.pos = self.pos.add(self.v)
        self.paint()

    def set(self, new_pos: Vector):
        self.old_pos = self.pos
        self.pos = new_pos
        self.v = Vector(0, 0)
        self.paint()

    def set_on_center(self):
        self.set(self.field.center)

    def set_rand_speed(self, team: int):
        if team == 1:
            vx = randint(40, 60) / 10
            if randint(0, 1) == 0:
                vy = randint(1, 10) / 5
            else:
                vy = -randint(1, 10) / 5
            self.v = Vector(vx, vy)
        elif team == 2:
            vx = -randint(40, 60) / 10
            if randint(0, 1) == 0:
                vy = randint(1, 10) / 5
            else:
                vy = -randint(1, 10) / 5
            self.v = Vector(vx, vy)

    def direct_to_point(self, point: Vector):
        m = randint(20, 60) / 10
        self.v = Vector(m, m).mul(point.sub(self.pos).norm())

    def shoot(self, num_goal):
        y_min = self.field.center_y - Field.BOX
        y_max = self.field.center_y + Field.BOX
        y = y_min + randint(0, y_max - y_min)
        if num_goal == 1:
            point = Vector(self.field.start_x, y)
        else:
            point = Vector(self.field.end_x, y)
        m = randint(40, 80) / 10
        self.v = Vector(m, m).mul(point.sub(self.pos).norm())

    def stop(self):
        self.v = Vector(0, 0)

    def rebound_x(self):
        self.v.x = -self.v.x

    def rebound_y(self):
        self.v.y = -self.v.y

    def paint(self):
        if self.shape is None:
            self.shape = self.canvas.create_oval(-Ball.RADIUS, -Ball.RADIUS, Ball.RADIUS, Ball.RADIUS, outline=Ball.OUTLINE,
                                                 fill=Ball.COLOR)
        delta = self.pos.sub(self.old_pos)
        self.canvas.move(self.shape, delta.x, delta.y)

    def field_hit_test(self):
        if self.pos.y <= (self.field.start_y + Ball.RADIUS):
            self.rebound_y()
        if self.pos.y >= (self.field.end_y - Ball.RADIUS):
            self.rebound_y()
        # if self.pos.x <= (self.field.start_x + Ball.RADIUS):
        #    self.rebound_x()
        # if self.pos.x >= (self.field.end_x - Ball.RADIUS):
        #    self.rebound_x()

    def is_out1(self) -> bool:
        return self.pos.x <= (self.field.start_x + Ball.RADIUS)

    def is_out2(self) -> bool:
        return self.pos.x >= (self.field.end_x - Ball.RADIUS)

    def is_goal1(self) -> bool:
        return self.field.goal1_rectangle.hit(self.pos.sub(Vector(Ball.RADIUS, 0)))

    def is_goal2(self) -> bool:
        return self.field.goal2_rectangle.hit(self.pos.add(Vector(Ball.RADIUS, 0)))

    def dist2_to_goal(self, goal_num: int):
        if goal_num == 1:
            return self.pos.dist2(self.field.goal1)
        else:
            return self.pos.dist2(self.field.goal2)

    def set_in_goal1(self):
        self.set(Vector(self.field.start_x - 2 * Ball.RADIUS, self.pos.y))

    def set_in_goal2(self):
        self.set(Vector(self.field.end_x + 2 * Ball.RADIUS, self.pos.y))
