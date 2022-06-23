# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time
import matplotlib.pyplot as plt

import output
import rtweekend
from light import Light
from perlin_noise import PerlinNoise3D
from ray import Ray
from sphere import Sphere
from vec3 import Color, Point3, Vec3


def palette_fire(d: float):
    yellow = Color(1.7, 1.3, 1.0)
    orange = Color(1, 0.6, 0)
    red = Color(1, 0, 0)
    darkgray = Color(0.2, 0.2, 0.2)
    gray = Color(0.4, 0.4, 0.4)

    x = rtweekend.clamp(d, 0, 1)

    if x < 0.25:
        return Vec3.linear_interpolation(gray, darkgray, 4 * x)
    elif x < 0.5:
        return Vec3.linear_interpolation(darkgray, red, 4 * x - 1)
    elif x < 0.75:
        return Vec3.linear_interpolation(red, orange, 4 * x - 2)
    else:
        return Vec3.linear_interpolation(orange, yellow, 4 * x - 3)


if __name__ == '__main__':

    # Start Timing
    start = time.perf_counter()

    # Image

    aspect_ratio = 1
    image_width = 384
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

    light1 = Light(Vec3(1, 1, 1), Point3(10, 10, 10))
    lights = [light1]

    # Objects

    sphere_1 = Sphere(1.5, Point3(0, 0, -3))

    # noise attribute set up
    noise_amplitude = 1

    # Rendering

    output_file = open("output2.ppm", "w+")
    begin_txt = "P3\n{0} {1} \n255\n".format(image_width, image_height)
    output_file.write(begin_txt)

    # Date Recording
    noise_stat = []

    for j in range(image_height - 1, - 1, - 1):

        for i in range(image_width):
            u = i / (image_width - 1)
            v = j / (image_height - 1)
            pixel_color = Color(0.2, 0.7, 0.8)

            r_in = Ray(origin, lower_left_corner + horizontal.scalar_multiply(u) + vertical.scalar_multiply(v) - origin)

            samples_per_pixel = 1

            tmp = sphere_1.sphere_trace(r_in, 0, lights)
            if tmp is not None and len(tmp) == 4:
                noise_level = (sphere_1.radius - (tmp[1] - sphere_1.center).length()) / noise_amplitude
                noise_stat.append(noise_level)
                pixel_color = palette_fire((noise_level + 0.25) * 2) * tmp[3]
            output.write_color(output_file, pixel_color, samples_per_pixel)

        print("{0} percent done".format(int((image_height - j) / image_height * 100)))

    output_file.close()
    plt.hist(noise_stat)
    plt.show()

    # End Timing
    end = time.perf_counter()

    print(end - start)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
