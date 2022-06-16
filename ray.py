from vec3 import Vec3, Point3


class Ray:
    def __init__(self, start: Point3, dir: Vec3):
        self.origin = start
        self.direction = dir

    def at(self, t):
        return self.origin + self.direction.scalar_multiply(t)
