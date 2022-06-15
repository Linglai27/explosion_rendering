import math


def degrees_to_radians(degrees: float):
    return degrees * math.pi / 180.0


def clamp(x: float, mi: float, ma: float):
    if x < mi:
        return mi
    if x > ma:
        return ma
    return x
