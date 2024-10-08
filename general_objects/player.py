import pygame
from definitions import object_types
from settings import settings
from game_object import GameObject
from square import Square

class Player(GameObject):
    def __init__(self):
        # Define the character object with a 2x2 square size (in game-world units)
        character_model_squares = [
            Square(0, 0, 2, 2, (255, 0, 0)),  # Red square, 2x2
        ]

        super().__init__(32, 24, character_model_squares, type=object_types.PLAYER)

    def handle_keys(self, keys_pressed):
        # Handle movement in game-world pixel units
        dx, dy = 0, 0
        if keys_pressed[pygame.K_LEFT]:
            dx = -settings.player_speed
        if keys_pressed[pygame.K_RIGHT]:
            dx = settings.player_speed
        if keys_pressed[pygame.K_UP]:
            dy = -settings.player_speed
        if keys_pressed[pygame.K_DOWN]:
            dy = settings.player_speed

        if dx or dy:
            self.move(dx, dy)

    def on_collision_active(self, other):
        # Particles will never stop us!!!
        if other.type == object_types.PARTICLE:
            return False

        return True
