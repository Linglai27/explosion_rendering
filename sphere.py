import math

from light import Light
from ray import Ray
from rigidbody import RigidBody
from vec3 import Vec3, Color, Point3


class Sphere(RigidBody):

    def __init__(self, r, c, col=Color(1, 1, 1)):
        self.radius = r
        self.center = c
        self.color = col

    def hit(self, r_in: Ray, tmin, tmax, lights=None):
        cur = tmin

        r_in.direction = r_in.direction.unit_vector()
        if Vec3.dot(r_in.origin - self.center, r_in.origin - self.center) - self.radius ** 2 > 0:
            tmax_possible = math.sqrt(Vec3.dot(r_in.origin - self.center, r_in.origin - self.center) - self.radius ** 2)
            tmax = min(tmax, tmax_possible)

        encounter = False

        while cur <= tmax:
            if self.signed_distance_function(r_in.at(cur)) <= 1e-8:
                encounter = True
                break
            else:
                cur += 1e-2

        if not encounter:
            return None

        intersection = r_in.at(cur)
        normal = self.compute_normal(intersection)

        if not lights:
            return [cur, intersection, normal]

        light_intensity = Color(.3, 0.3, 0.2)
        for light in lights:
            light_intensity += light.intensity.scalar_multiply(max(0, Vec3.dot(normal, (light.position - intersection).unit_vector())))

        return [cur, intersection, normal, light_intensity]

    def signed_distance_function(self, pt):
        return math.sqrt(Vec3.dot(pt - self.center, pt - self.center)) - self.radius - Sphere.sine_noise(pt)

    def compute_normal(self, pt: Point3):
        eps = 1e-4

        tmp = self.signed_distance_function(pt)
        dx = self.signed_distance_function(pt + Vec3(eps, 0, 0)) - tmp
        dy = self.signed_distance_function(pt + Vec3(0, eps, 0)) - tmp
        dz = self.signed_distance_function(pt + Vec3(0, 0, eps)) - tmp

        return Vec3(dx, dy, dz).unit_vector()

    @staticmethod
    def sine_noise(pt: Point3):
        res = 1

        for i in range(3):
            res *= 0.4 * math.sin(48 * pt.element[i])

        return res