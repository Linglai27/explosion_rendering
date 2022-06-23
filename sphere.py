import math

from light import Light
from perlin_noise import PerlinNoise3D
from ray import Ray
from rigidbody import RigidBody
import noise
from vec3 import Vec3, Color, Point3

perlin_noise_3D = PerlinNoise3D(256)


class Sphere(RigidBody):

    def __init__(self, r, c):
        self.radius = r
        self.center = c

    def sphere_trace(self, r_in: Ray, tmin, lights=None):
        cur = tmin

        r_in.direction = r_in.direction.unit_vector()

        encounter = False

        for _ in range(128):
            d = self.signed_distance_function(r_in.at(cur))
            if d <= 0:
                encounter = True
                break
            else:
                cur += max(1e-2, 0.1 * d)

        if not encounter:
            return None

        intersection = r_in.at(cur)
        normal = self.compute_normal(intersection)

        if not lights:
            return [cur, intersection, normal]

        light_intensity = Color(0, 0, 0)
        for light in lights:
            light_intensity += light.intensity.scalar_multiply(
                max(0.4, Vec3.dot(normal, (light.position - intersection).unit_vector())))

        return [cur, intersection, normal, light_intensity]

    def signed_distance_function(self, pt):
        pt2 = pt - self.center
        displacement = - perlin_noise_3D.fractal_brownian_motion(pt2.scalar_multiply(3.4))
        return math.sqrt(Vec3.dot(pt2, pt2)) - (self.radius + displacement)

    def compute_normal(self, pt: Point3):
        eps = 1e-1

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
