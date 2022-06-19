import math
import random

import output
from vec3 import Color, Vec3, Point3


class PerlinNoise2D:

    def __init__(self, k_max_vertices: int):
        self.gradient_table = []

        for _ in range(k_max_vertices):
            theta = random.random() * math.pi * 2
            self.gradient_table.append(Vec3(math.cos(theta), math.sin(theta), 0))

        self.permutation_table = [w for w in range(k_max_vertices)]
        self.permutation_table.extend(self.permutation_table)
        self.shuffle()

    def shuffle(self):
        k_max_vertices = len(self.gradient_table)

        for k in range(k_max_vertices):
            w = random.randint(0, k_max_vertices - 1)
            self.permutation_table[w], self.permutation_table[k] = self.permutation_table[k], self.permutation_table[w]

        for k in range(k_max_vertices):
            self.permutation_table[k_max_vertices + k] = self.permutation_table[k]

    def eval(self, pt: Point3):
        xi = math.floor(pt.x())
        yi = math.floor(pt.y())

        dx = pt.x() - xi
        dy = pt.y() - yi

        largest_size = len(self.gradient_table)
        rx0 = xi % largest_size
        rx1 = (rx0 + 1) % largest_size
        ry0 = yi % largest_size
        ry1 = (ry0 + 1) % largest_size

        c00 = self.gradient_table[self.permutation_table[self.permutation_table[rx0] + ry0]]
        c01 = self.gradient_table[self.permutation_table[self.permutation_table[rx0] + ry1]]
        c10 = self.gradient_table[self.permutation_table[self.permutation_table[rx1] + ry0]]
        c11 = self.gradient_table[self.permutation_table[self.permutation_table[rx1] + ry1]]

        x0, x1 = dx, dx - 1
        y0, y1 = dy, dy - 1

        pt00 = Vec3(x0, y0, 0)
        pt01 = Vec3(x0, y1, 0)
        pt10 = Vec3(x1, y0, 0)
        pt11 = Vec3(x1, y1, 0)

        interp_x1 = PerlinNoise2D.linear_interpolation(Vec3.dot(c00, pt00), Vec3.dot(c10, pt10), PerlinNoise2D.
                                                       smooth_func(dx, 1))
        interp_x2 = PerlinNoise2D.linear_interpolation(Vec3.dot(c01, pt01), Vec3.dot(c11, pt11), PerlinNoise2D.
                                                       smooth_func(dx, 1))

        return PerlinNoise2D.linear_interpolation(interp_x1, interp_x2, PerlinNoise2D.smooth_func(dy, 1))

    @staticmethod
    def linear_interpolation(lo, hi, t):
        return lo * (1 - t) + hi * t

    @staticmethod
    def smooth_func(t, opt=1):
        if opt == 1:
            return 0.5 * (1 - math.cos(t * math.pi))

        if opt == 2:
            return t * t * (3 - 2 * t)

def driver_code():
    # image_rendering_setting

    image_width = 512
    image_height = 512
    samples_per_pixel = 1
    pixel_storage = []

    noise = PerlinNoise2D(256)

    output_file = open("perlin noise.ppm", "w+")
    begin_txt = "P3\n{0} {1} \n255\n".format(image_width, image_height)

    print(begin_txt)
    output_file.write(begin_txt)

    num_layer = 1

    for j in range(image_height - 1, - 1, - 1):
        for i in range(image_width):

            noise_val = 0

            freq = 1
            amp = 1
            freq_mul = 1.8
            amp_mul = 0.35

            pt = Vec3(i, j, 0).scalar_multiply(freq)

            for k in range(num_layer):
                noise_val += (noise.eval(pt) + 1) / 2 * amp
                pt = pt.scalar_multiply(freq_mul)
                amp *= amp_mul

            pixel_storage.append(noise_val)

    max_noise_val = max(pixel_storage)
    cur_index = 0

    if max_noise_val != 0:
        for j in range(image_height - 1, - 1, - 1):
            for i in range(image_width):
                noise_val = pixel_storage[cur_index]
                cur_index += 1
                output.write_color(output_file, Vec3(noise_val / max_noise_val, noise_val / max_noise_val, noise_val /max_noise_val), samples_per_pixel)
    else:
        for j in range(image_height - 1, - 1, - 1):
            for i in range(image_width):
                noise_val = pixel_storage[cur_index]
                cur_index += 1
                output.write_color(output_file, Vec3(noise_val, noise_val, noise_val))

    output_file.close()

driver_code()
