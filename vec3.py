import math
import random


class Vec3:

    def __init__(self, x=0, y=0, z=0):
        self.element = [x, y, z]

    def x(self):
        return self.element[0]

    def y(self):
        return self.element[1]

    def z(self):
        return self.element[2]

    def __add__(self, other):
        return Vec3(self.element[0] + other.element[0], self.element[1] + other.element[1],
                    self.element[2] + other.element[2])

    def __iadd__(self, other):
        self.element[0] += other.element[0]
        self.element[1] += other.element[1]
        self.element[2] += other.element[2]

        return self

    def set(self, val0=0, val1=0, val2=0):
        self.element[0] = val0
        self.element[1] = val1
        self.element[2] = val2

    def __mul__(self, other):
        return Vec3(self.element[0] * other.element[0], self.element[1] * other.element[1],
                    self.element[2] * other.element[2])

    def scalar_multiply(self, t):
        return Vec3(self.element[0] * t, self.element[1] * t, self.element[2] * t)

    def __neg__(self):
        return self.scalar_multiply(-1)

    def __sub__(self, other):
        return self + (-other)

    def __imul__(self, other):
        self.element[0] *= other.element[0]
        self.element[1] *= other.element[1]
        self.element[2] *= other.element[2]

    def __truediv__(self, t):
        return self.scalar_multiply(1 / t)

    def near_zero(self):
        tolerance = 1e-8

        return abs(self.element[0]) < tolerance and abs(self.element[1]) < tolerance and abs(
            self.element[2]) < tolerance

    def print(self):
        print("{0}, {1}, {2}".format(self.element[0], self.element[1], self.element[2]))

    @staticmethod
    def dot(u, v):
        return u.element[0] * v.element[0] + u.element[1] * v.element[1] + u.element[2] * v.element[2]

    @staticmethod
    def cross(u, v):
        return Vec3(u.element[1] * v.element[2] - u.element[2] * v.element[1],
                    u.element[2] * v.element[0] - u.element[0] * v.element[2],
                    u.element[0] * v.element[1] - u.element[1] * v.element[0])

    def unit_vector(self):
        return self / ((Vec3.dot(self, self)) ** 0.5)

    def length(self):
        return (Vec3.dot(self, self)) ** 0.5

    def direct_product(self, other):
        return Vec3(self.element[0] * other.element[0], self.element[1] * other.element[1],
                    self.element[2] * other.element[2])

    @staticmethod
    def random_unit_vector():
        return Vec3.random_in_unit_sphere().unit_vector()

    @staticmethod
    def random_in_hemisphere(normal):
        in_unit_sphere = Vec3.random_in_unit_sphere()
        if Vec3.dot(in_unit_sphere, normal) > 0:
            return in_unit_sphere
        else:
            return -in_unit_sphere

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random().scalar_multiply(2) - Vec3(1, 1, 1)
            if Vec3.dot(p, p) > 1:
                continue
            return p

    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
            if Vec3.dot(p, p) >= 1:
                continue
            return p

    @staticmethod
    def random(mi=0, ma=1):
        return Vec3(random.uniform(mi, ma), random.uniform(mi, ma), random.uniform(mi, ma))

    @staticmethod
    def reflect(v, n):
        return v - n.scalar_multiply(2 * Vec3.dot(v, n))

    @staticmethod
    def refract(r, n, eta_ratio):
        cos_theta = min(Vec3.dot(-r, n), 1)
        r_out_perp = (r + n.scalar_multiply(cos_theta)).scalar_multiply(eta_ratio)
        r_out_parallel = n.scalar_multiply(-math.sqrt(math.fabs(1 - Vec3.dot(r_out_perp, r_out_perp))))
        return r_out_perp + r_out_parallel


Point3 = Vec3
Color = Vec3
