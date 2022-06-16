# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import math

import output
from light import Light
from ray import Ray
from sphere import Sphere
from vec3 import Color, Point3, Vec3

if __name__ == '__main__':
    # Image

    aspect_ratio = 16 / 9
    image_width = 400
    image_height = int(image_width / aspect_ratio)

    # Camera

    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1

    origin = Point3(0, 0, 0)
    horizontal = Vec3(viewport_width, 0, 0)
    vertical = Vec3(0, viewport_height, 0)
    lower_left_corner = origin - horizontal.scalar_multiply(0.5) - vertical.scalar_multiply(0.5) - Vec3(0, 0, focal_length)

    # Lights

    light1 = Light(Vec3(0.5, 0.4, 1.0), Point3(2, 2, -1))
    light2 = Light(Vec3(0.3, 0.7, 0.9), Point3(-5, -2, -1))
    lights = [light2]

    # Objects

    sphere_1 = Sphere(1 / math.sqrt(2), Point3(0, 0, -1), Color(1.0, 1.0, 1.0))

    print("P3\n{0} {1} \n255\n".format(image_width, image_height))

    for j in range(image_height - 1, - 1, - 1):
        for i in range(image_width):
            u = i / (image_width - 1)
            v = j / (image_height - 1)
            pixel_color = Color(0.2, 0.7, 0.8)

            r_in = Ray(origin, lower_left_corner + horizontal.scalar_multiply(u) + vertical.scalar_multiply(v) - origin)

            samples_per_pixel = 1

            tmp = sphere_1.hit(r_in, 0, math.inf, lights)
            if tmp is not None and len(tmp) == 3:
                pixel_color = sphere_1.color * tmp[2]
            output.write_color(pixel_color, samples_per_pixel)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
