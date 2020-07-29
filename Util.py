import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def mul(self, v):
        return Vector(self.x * v.x, self.y * v.y)

    def norm(self):
        if self.x == self.y == 0:
            return self
        else:
            dist = math.sqrt(self.x * self.x + self.y * self.y)
            return Vector(self.x / dist, self.y / dist)

    def dist2(self, v):
        sub_v = self.sub(v)
        return sub_v.x * sub_v.x + sub_v.y * sub_v.y

    def rect(self, r):
        return Rectangle(self.x - r, self.y - r, self.x + r, self.y + r)

    def invert(self, inv_x: bool, inv_y: bool):
        if inv_x:
            x = -self.x
        else:
            x = self.x
        if inv_y:
            y = -self.y
        else:
            y = self.y
        return Vector(x, y)


class Rectangle:
    def __init__(self, left: float, top: float, right: float, bottom: float):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def hit(self, v: Vector) -> bool:
        if self.left <= v.x <= self.right and self.top <= v.y <= self.bottom:
            return True
        else:
            return False


#def dist2(pos1: Vector, pos2: Vector):
#    return (pos2.x - pos1.x) * (pos2.x - pos1.x) + (pos2.y - pos1.y) * (pos2.y - pos1.y)


#def sub_vector(pos1: Vector, pos2: Vector) -> Vector:
#    dist = math.sqrt(dist2(pos1, pos2))
#    return Vector((pos2.x - pos1.x) / dist, (pos2.y - pos1.y) / dist)


#def norm_vector(v: Vector) -> Vector:
#    if v.x == v.y == 0: return v
#    dist = math.sqrt(v.x * v.x + v.y * v.y)
#    return Vector(v.x / dist, v.y / dist)


class Util:
    pass
