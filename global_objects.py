from camera import Camera
from collision import CollisionGrid

class GlobalObjects:
    camera = Camera()
    collision_grid = CollisionGrid()

    game_objects = {}

globals = GlobalObjects()
