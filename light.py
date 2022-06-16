from vec3 import Vec3, Point3


class Light:
    def __init__(self, intense: Vec3, pos: Point3):
        self.intensity = intense
        self.position = pos

