import pygame
from uuid import uuid4
from settings import settings
from global_objects import globals

def draw_object(surface, x, y, squares):
    """Draw an object defined by a list of (offset_x, offset_y, width, height, color) tuples."""
    for square in squares:
        offset_x, offset_y, width, height, color = square
        pygame.draw.rect(surface, color, (
            (x + offset_x) * settings.pixel_size,  # Convert to raw screen pixels
            (y + offset_y) * settings.pixel_size,
            width * settings.pixel_size, height * settings.pixel_size))  # Scale width and height

class GameObject:
    def __init__(self, x, y, squares, collidable=True):
        """
        Initialize a game object.
        
        Args:
            x (int): X position in game-world pixel units.
            y (int): Y position in game-world pixel units.
            squares (list): List of squares defining the object.
            collidable (bool): Whether the object participates in collision detection.
        """
        self.id = uuid4()
        self.x = x  # Position in game-world pixel units
        self.y = y  # Position in game-world pixel units
        self.squares = squares  # Structure of the object as squares (with sizes)
        self.collidable = collidable  # Collision flag

    def register(self):
        globals.collision_grid.register(self)
        globals.game_objects[self.id] = self

    def unregister(self):
        globals.collision_grid.unregister(self)
        globals.game_objects.pop(self.id)

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
        self.x = new_x
        self.y = new_y

        # Register the object in the new grid position
        globals.collision_grid.register(self)

    def check_collision(self, new_x, new_y):
        """Check if moving to the new position would cause a collision."""
        for square in self.squares:
            offset_x, offset_y, width, height, _ = square
            # Check for collision by looking at the grid positions that this square would occupy
            for i in range(width):
                for j in range(height):
                    new_grid_pos = (new_x + offset_x + i, new_y + offset_y + j)
                    if new_grid_pos in globals.collision_grid.grid:
                        for other in globals.collision_grid.grid[new_grid_pos]:
                            if other != self:
                                # Trigger the collision callback
                                self.on_collision(other)
                                other.on_collision(self)
                                return True
        return False

    def on_collision(self, other):
        """Callback when this object collides with another."""
        print(f"Collision detected between {self} and {other}")

    def __repr__(self):
        """String representation for debugging."""
        return f"GameObject({self.x}, {self.y}, Collidable={self.collidable})"