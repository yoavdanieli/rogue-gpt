class CollisionGrid:
    # Grid to track object locations
    grid = {}

    # Register an object in the spatial grid
    def register(self, obj):
        """Register all squares of an object in the grid by their (x, y) positions."""
        if not obj.collidable:
            return  # Exempted objects are not registered for collision
        for square in obj.squares:
            for i in range(square.width):
                for j in range(square.height):
                    grid_pos = (obj.x + square.offset_x + i, obj.y + square.offset_y + j)
                    if grid_pos in self.grid:
                        self.grid[grid_pos].append(obj)
                    else:
                        self.grid[grid_pos] = [obj]

    # Unregister an object from the grid
    def unregister(self, obj):
        """Remove an object from its current position in the grid."""
        if not obj.collidable:
            return  # Exempted objects are not registered for collision
        for square in obj.squares:
            for i in range(square.width):
                for j in range(square.height):
                    grid_pos = (obj.x + square.offset_x + i, obj.y + square.offset_y + j)
                    if grid_pos in self.grid and obj in self.grid[grid_pos]:
                        self.grid[grid_pos].remove(obj)
                        if not self.grid[grid_pos]:  # Clean up empty grid cells
                            del self.grid[grid_pos]
