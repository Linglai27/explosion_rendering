import math
import random

import output
from vec3 import Color, Vec3


class ValueNoise2D:

    def __init__(self, k_max_vertices: int):
        self.random_table = [random.random() for _ in range(k_max_vertices)]
        self.permutation_table = [k for k in range(k_max_vertices)]
        self.permutation_table.extend(self.permutation_table)
        self.shuffle()

    def shuffle(self):
        k_max_vertices = len(self.random_table)

        for k in range(k_max_vertices):
            w = random.randint(0, k_max_vertices - 1)
            self.permutation_table[w], self.permutation_table[k] = self.permutation_table[k], self.permutation_table[w]
            self.permutation_table[k_max_vertices + k] = self.permutation_table[k]

    def eval(self, t: Vec3):
        xi = math.floor(t.x())
        yi = math.floor(t.y())

        dx = t.x() - xi
        dy = t.y() - yi

        largest_size = len(self.random_table)
        rx0 = xi % largest_size
        rx1 = (rx0 + 1) % largest_size
        ry0 = yi % largest_size
        ry1 = (ry0 + 1) % largest_size

        c00 = self.random_table[self.permutation_table[self.permutation_table[rx0] + ry0]]
        c01 = self.random_table[self.permutation_table[self.permutation_table[rx0] + ry1]]
        c10 = self.random_table[self.permutation_table[self.permutation_table[rx1] + ry0]]
        c11 = self.random_table[self.permutation_table[self.permutation_table[rx1] + ry1]]

        interp_x1 = ValueNoise2D.linear_interpolation(c00, c10, ValueNoise2D.smooth_func(dx, 1))
        interp_x2 = ValueNoise2D.linear_interpolation(c01, c11, ValueNoise2D.smooth_func(dx, 1))
        return ValueNoise2D.linear_interpolation(interp_x1, interp_x2, ValueNoise2D.smooth_func(dy, 1))

    @staticmethod
    def linear_interpolation(lo, hi, t):
        return lo * (1 - t) + hi * t

    @staticmethod
    def smooth_func(t, opt=1):
        if opt == 1:
            return 0.5 * (1 - math.cos(t * math.pi))

        if opt == 2:
            return t * t * (3 - 2 * t)


# image_rendering_setting

image_width = 512
image_height = 512
samples_per_pixel = 1
pixel_storage = []

noise = ValueNoise2D(256)
"""print(noise.r)
print(noise.eval(Vec3(1.5, 1.5, 0)))"""

print("P3\n{0} {1} \n255\n".format(image_width, image_height))

num_layer = 5
max_noise_val = 0

for j in range(image_height - 1, - 1, - 1):
    for i in range(image_width):

        noise_val = 0

        freq = 0.02
        amp = 1
        freq_mul = 1.8
        amp_mul = 0.35

        pt = Vec3(i, j, 0).scalar_multiply(freq)

        for k in range(num_layer):
            noise_val += noise.eval(pt) * amp
            pt = pt.scalar_multiply(freq_mul)
            amp *= amp_mul

        pixel_storage.append(noise_val)

max_noise_val = max(pixel_storage)
cur_index = 0

for j in range(image_height - 1, - 1, - 1):
    for i in range(image_width):
        noise_val = pixel_storage[cur_index]
        cur_index += 1
        output.write_color(Vec3(noise_val / max_noise_val, noise_val / max_noise_val, noise_val /max_noise_val), samples_per_pixel)
