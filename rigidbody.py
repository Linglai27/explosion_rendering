from abc import abstractmethod


class RigidBody:

    @abstractmethod
    def signed_distance_function(self, arg):
        return NotImplemented
