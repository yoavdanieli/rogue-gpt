import pygame
from uuid import uuid4
from typing import List
from definitions import object_types
from settings import settings
from global_objects import globals
from square import Square

def draw_object(surface, x, y, squares: List[Square]):
    for square in squares:
        pygame.draw.rect(surface, square.color, (
            (x + square.offset_x) * settings.pixel_size,  # Convert to raw screen pixels
            (y + square.offset_y) * settings.pixel_size,
            square.width * settings.pixel_size, square.height * settings.pixel_size))  # Scale width and height

class GameObject:
    def __init__(self, x, y, squares: List[Square], type=None, collidable=True):
        """
        Initialize a game object.
        
        Args:
            x (int): X position in game-world pixel units.
            y (int): Y position in game-world pixel units.
            squares (list): List of squares defining the object.
            collidable (bool): Whether the object participates in collision detection.
        """

        self.x = x  # Position in game-world pixel units
        self.y = y  # Position in game-world pixel units
        self.squares = squares  # Structure of the object as squares (with sizes)
        self.type = type if type else object_types.GENERIC
        self.collidable = collidable  # Collision flag
        self.id = self.type + '-' + str(uuid4())
        self.registered = False

    def register(self):
        globals.collision_grid.register(self)
        globals.game_objects[self.id] = self
        self.registered = True

    def unregister(self):
        print(f"unregistering {self.id}")
        globals.collision_grid.unregister(self)
        del globals.game_objects[self.id]
        self.registered = False

    def update_position(self, new_x, new_y):
        if not self.registered:
            return

        self.x = new_x
        self.y = new_y

        # Register the object in the new grid position
        globals.collision_grid.unregister(self)
        globals.collision_grid.register(self)

    def draw(self, surface):
        """Draw the object using the camera offset."""
        draw_object(surface, self.x - globals.camera.x, self.y - globals.camera.y, self.squares)

    def move(self, dx, dy):
        """Move the object by dx, dy in game-world pixel units."""
        if not self.collidable:
            # If not collidable, simply move without collision checks
            self.x += dx
            self.y += dy
            return

        # Unregister the object from the current grid
        globals.collision_grid.unregister(self)

        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collisions in the new position
        if self.check_collision(new_x, new_y):
            # Collision occurred, re-register at the current position and exit
            globals.collision_grid.register(self)
            return  # Cancel movement if a collision occurs

        # Apply the move if no collision
        self.update_position(new_x, new_y)

    def check_collision(self, new_x, new_y):
        """Check if moving to the new position would cause a collision."""
        for square in self.squares:
            # Check for collision by looking at the grid positions that this square would occupy
            for i in range(square.width):
                for j in range(square.height):
                    new_grid_pos = (new_x + square.offset_x + i, new_y + square.offset_y + j)
                    if new_grid_pos in globals.collision_grid.grid:
                        for other in globals.collision_grid.grid[new_grid_pos]:
                            if other != self:
                                print(f"collision {self.id} {other.id}")
                                print(f"content: {globals.collision_grid.grid[new_grid_pos]}")
                                # Trigger the collision callback
                                should_not_move = self.on_collision_active(other)
                                other.on_collision_passive(self)
                                return should_not_move
        return False

    def on_collision_active(self, other):
        """Callback when this object collides with another."""
        # print(f"Collision detected between {self} and {other}")
        pass

    def on_collision_passive(self, other):
        """Callback when another object collides with this."""
        # print(f"Collision detected between {self} and {other}")
        pass

    def on_frame(self, events, pressed_keys):
        """
        Callback for objects to implement
        """

        pass

    def __repr__(self):
        """String representation for debugging."""
        return f"GameObject({self.x}, {self.y}, id={self.id})"