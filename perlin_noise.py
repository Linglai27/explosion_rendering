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

    def fractal_brownian_motion(self, pt: Point3):

        res = 0
        freq = 256
        freq_amp = 2
        amp = 0.5
        amp_mul = 0.5
        num_layer = 4

        pt = pt.scalar_multiply(freq)

        for i in range(num_layer):
            res += (self.eval(pt) + 1) * amp / 2
            amp *= amp_mul
            pt = pt.scalar_multiply(freq_amp)

        return res / 0.9375


class PerlinNoise3D:

    def __init__(self, k_max_vertices: int):
        self.gradient_table = []

        for _ in range(k_max_vertices):
            theta = math.acos(2 * random.random() - 1)
            phi = 2 * random.random() * math.pi
            x = math.cos(phi) * math.sin(theta)
            y = math.sin(phi) * math.sin(theta)
            z = math.cos(theta)
            self.gradient_table.append(Vec3(x, y, z))

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

    def hash(self, x, y, z):
        return self.permutation_table[self.permutation_table[self.permutation_table[x] + y] + z]

    def eval(self, pt: Point3):
        xi = math.floor(pt.x())
        yi = math.floor(pt.y())
        zi = math.floor(pt.z())

        dx = pt.x() - xi
        dy = pt.y() - yi
        dz = pt.z() - zi

        largest_size = len(self.gradient_table)
        rx0 = xi % largest_size
        rx1 = (rx0 + 1) % largest_size
        ry0 = yi % largest_size
        ry1 = (ry0 + 1) % largest_size
        rz0 = zi % largest_size
        rz1 = (rz0 + 1) % largest_size

        c000 = self.gradient_table[self.hash(rx0, ry0, rz0)]
        c100 = self.gradient_table[self.hash(rx1, ry0, rz0)]
        c010 = self.gradient_table[self.hash(rx0, ry1, rz0)]
        c001 = self.gradient_table[self.hash(rx0, ry0, rz1)]
        c110 = self.gradient_table[self.hash(rx1, ry1, rz0)]
        c011 = self.gradient_table[self.hash(rx0, ry1, rz1)]
        c101 = self.gradient_table[self.hash(rx1, ry0, rz1)]
        c111 = self.gradient_table[self.hash(rx1, ry1, rz1)]

        x0, x1 = dx, dx - 1
        y0, y1 = dy, dy - 1
        z0, z1 = dz, dz - 1

        pt000 = Vec3(x0, y0, z0)
        pt100 = Vec3(x1, y0, z0)
        pt010 = Vec3(x0, y1, z0)
        pt001 = Vec3(x0, y0, z1)
        pt110 = Vec3(x1, y1, z0)
        pt011 = Vec3(x0, y1, z1)
        pt101 = Vec3(x1, y0, z1)
        pt111 = Vec3(x1, y1, z1)

        a = PerlinNoise3D.linear_interpolation(Vec3.dot(c000, pt000), Vec3.dot(c100, pt100),
                                               PerlinNoise3D.smooth_func(dx, 1))
        b = PerlinNoise3D.linear_interpolation(Vec3.dot(c010, pt010), Vec3.dot(c110, pt110),
                                               PerlinNoise3D.smooth_func(dx, 1))
        c = PerlinNoise3D.linear_interpolation(Vec3.dot(c001, pt001), Vec3.dot(c101, pt101),
                                               PerlinNoise3D.smooth_func(dx, 1))
        d = PerlinNoise3D.linear_interpolation(Vec3.dot(c011, pt011), Vec3.dot(c111, pt111),
                                               PerlinNoise3D.smooth_func(dx, 1))

        e = PerlinNoise3D.linear_interpolation(a, b, PerlinNoise3D.smooth_func(dy, 1))
        f = PerlinNoise3D.linear_interpolation(c, d, PerlinNoise3D.smooth_func(dy, 1))

        return PerlinNoise3D.linear_interpolation(e, f, PerlinNoise3D.smooth_func(dz, 1))

    @staticmethod
    def linear_interpolation(lo, hi, t):
        return lo * (1 - t) + hi * t

    @staticmethod
    def smooth_func(t, opt=1):
        if opt == 1:
            return 0.5 * (1 - math.cos(t * math.pi))

        if opt == 2:
            return t * t * (3 - 2 * t)

    def fractal_brownian_motion(self, x: Point3):

        p = Vec3.rotate(x)
        f = 0

        f += self.eval(p) * 0.5
        p = p.scalar_multiply(2.32)

        f += self.eval(p) * 0.25
        p = p.scalar_multiply(3.03)

        f += self.eval(p) * 0.125
        p = p.scalar_multiply(2.61)

        f += self.eval(p) * 0.0625

        return f / 0.9375


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

    num_layer = 5

    for j in range(image_height - 1, - 1, - 1):
        for i in range(image_width):

            noise_val = 0

            freq = 0.02
            amp = 1
            freq_mul = 2
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

# driver_code()
