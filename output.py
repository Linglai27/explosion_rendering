import rtweekend
from vec3 import Color


def write_color(pixel_color: Color, samples_per_pixel):
    color_count = 256
    scale = 1 / samples_per_pixel
    gamma = 0.5
    r = (pixel_color.x() * scale) ** gamma
    g = (pixel_color.y() * scale) ** gamma
    b = (pixel_color.z() * scale) ** gamma
    r = int(rtweekend.clamp(r, 0, 0.999) * color_count)
    g = int(rtweekend.clamp(g, 0, 0.999) * color_count)
    b = int(rtweekend.clamp(b, 0, 0.999) * color_count)
    print("{0} {1} {2}\n".format(r, g, b))
