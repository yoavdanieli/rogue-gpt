import pygame
import random
from definitions import object_types
from settings import settings
from game_object import GameObject
from square import Square

class Background(GameObject):
    BACKGROUND_COLOR = (20, 20, 20)
    DIRT_COLOR = (50, 50, 50)
    SMALL_DIRT_AMOUNT = 50
    BIG_DIRT_AMOUNT = 15

    def __init__(self):
        background_color_square = [Square(0, 0, settings.map_width, settings.map_height, self.BACKGROUND_COLOR)]

        small_dirt = [self.new_small_dirt() for _ in range(self.SMALL_DIRT_AMOUNT)]

        big_dirt = [self.new_big_dirt() for _ in range(self.BIG_DIRT_AMOUNT)]

        background_model = background_color_square + small_dirt + big_dirt

        super().__init__(0, 0, background_model, type=object_types.BACKGROUND, collidable=False)

    def new_small_dirt(self):
        return Square(random.randint(0, settings.map_width), random.randint(0, settings.map_height), 1, 1, self.DIRT_COLOR)
    
    def new_big_dirt(self):
        return Square(random.randint(0, settings.map_width), random.randint(0, settings.map_height), 3, 3, self.DIRT_COLOR)
