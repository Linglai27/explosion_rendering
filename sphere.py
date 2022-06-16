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
            solution = solution[0]
        elif tmin <= solution[1] <= tmax:
            solution = solution[1]
        else:
            return None

        intersection = r_in.origin + r_in.direction.scalar_multiply(solution)
        normal = self.compute_normal(intersection)

        if not lights:
            return [solution, normal]

        light_intensity = Color(1.0, 0.3, 0.2)
        for light in lights:
            light_intensity += light.intensity.scalar_multiply(max(0, Vec3.dot(normal, (light.position - intersection).unit_vector())))

        return [solution, normal, light_intensity]

    def signed_distance_function(self, pt):
        return Vec3.dot(pt, pt)

    def compute_normal(self, pt: Point3):
        eps = 1e-4

        tmp = self.signed_distance_function(pt)
        dx = self.signed_distance_function(pt + Vec3(eps, 0, 0)) - tmp
        dy = self.signed_distance_function(pt + Vec3(0, eps, 0)) - tmp
        dz = self.signed_distance_function(pt + Vec3(0, 0, eps)) - tmp

        return Vec3(dx, dy, dz).unit_vector()
