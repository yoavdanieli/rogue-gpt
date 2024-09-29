from general_objects.level import Level
from square import Square
from general_objects.player import Player
from game_object import GameObject

class DummyLevel(Level):
    def __init__(self, screen):
        super().__init__(screen)

        self.player = Player()

        # Define a wall object that will cause a collision with a larger size
        wall_squares = [Square(0, 0, 3, 1, (0, 255, 0))]  # Green rectangle, 3x1
        self.objects.append(GameObject(40, 24, wall_squares))

        # Define an exempted object (e.g., decorative element) that does not collide
        decorative_squares = [Square(0, 0, 4, 4, (0, 0, 255))]  # Blue square, 4x4
        self.objects.append(GameObject(50, 30, decorative_squares, collidable=False))
