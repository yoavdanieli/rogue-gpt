import pygame
from definitions import object_types
from settings import settings
from game_object import GameObject
from square import Square

class MapOutlineBarrier(GameObject):
    COLOR = (125, 125, 125)

    def __init__(self):
        top_barrier = Square(0, 0, settings.map_width, 1, self.COLOR)
        bottom_barrier = Square(0, settings.map_height - 1, settings.map_width, 1, self.COLOR)
        left_barrier = Square(0, 0, 1, settings.map_height, self.COLOR)
        right_barrier = Square(settings.map_width - 1, 0, 1, settings.map_height, self.COLOR)
        
        barriers = [top_barrier, bottom_barrier, left_barrier, right_barrier]

        super().__init__(0, 0, barriers, type=object_types.BARRIER, collidable=True)
