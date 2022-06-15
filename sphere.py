import math

from ray import Ray
from vec3 import Vec3


class Sphere:

    def __init__(self, r, c):
        self.radius = r
        self.center = c

    def hit(self, r_in: Ray, tmin, tmax):
        a = Vec3.dot(r_in.direction, r_in.direction)
        half_b = Vec3.dot(r_in.origin - self.center, r_in.direction)
        c = Vec3.dot(r_in.origin - self.center, r_in.origin - self.center) - self.radius ** 2

        disc = half_b * half_b - a * c
        if disc >= 0:
            disc_sqrt = math.sqrt(disc)
        else:
            return None

        solution = [(-half_b - disc_sqrt) / a, (-half_b + disc_sqrt) / a]
        if tmin <= solution[0] <= tmax:
            return solution[0]
        elif tmin <= solution[1] <= tmax:
            return solution[1]
        else:
            return None
