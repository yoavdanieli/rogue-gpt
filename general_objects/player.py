import pygame
from settings import settings
from game_object import GameObject

class Player(GameObject):
    def __init__(self):
        # Define the character object with a 2x2 square size (in game-world units)
        character_model_squares = [
            (0, 0, 2, 2, (255, 0, 0)),  # Red square, 2x2
        ]

        super().__init__(32, 24, character_model_squares)

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

        self.move(dx, dy)
