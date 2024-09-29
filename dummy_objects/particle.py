from definitions import object_types
from settings import settings
from game_object import GameObject
from square import Square

class Particle(GameObject):
    def __init__(self, x, y, speed_x, speed_y):
        squares = [
            Square(0, 0, 1, 1, (0, 125, 125))
        ]

        super().__init__(x, y, squares, type=object_types.PARTICLE)

        self.speed_x = speed_x
        self.speed_y = speed_y

    def on_frame(self, events, keys_pressed):
        self.move(self.speed_x, self.speed_y)

        # Allows being to the right of the map, otherwise if it is outside of the map removes itself
        if self.x < 0 or \
                self.y > settings.map_height or \
                self.y < 0:
            print("unregistering a particle")
            self.unregister()

    def on_collision_active(self, other):
        print(f"on particle collision {self.id}")
        if other.type == object_types.PLAYER:
            self.unregister()
            return False

        return super().on_collision_active(other)

    
