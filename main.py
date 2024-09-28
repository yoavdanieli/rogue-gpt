import pygame
import sys

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Window dimensions
PIXEL_SIZE = 10  # Size of a "pixel" in the game
BG_COLOR = (0, 0, 0)  # Background color (black)
FPS = 60  # Frames per second
FPS_THRESHOLD = 60  # Threshold to trigger FPS warning

# Modular settings for character movement
char_speed = 1  # Speed in game-world pixel units per frame

# Map settings (in game-world pixel units)
MAP_WIDTH, MAP_HEIGHT = 128, 96  # Map dimensions

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixelated Game with Enhanced Features")

# Font settings for FPS warning
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
warning_text = font.render('Warning: FPS below 60!', True, (255, 0, 0))

# Grid to track object locations
grid = {}

# Register an object in the spatial grid
def register_in_grid(obj):
    """Register all squares of an object in the grid by their (x, y) positions."""
    if not obj.collidable:
        return  # Exempted objects are not registered for collision
    for square in obj.squares:
        offset_x, offset_y, width, height, _ = square
        for i in range(width):
            for j in range(height):
                grid_pos = (obj.x + offset_x + i, obj.y + offset_y + j)
                if grid_pos in grid:
                    grid[grid_pos].append(obj)
                else:
                    grid[grid_pos] = [obj]

# Unregister an object from the grid
def unregister_from_grid(obj):
    """Remove an object from its current position in the grid."""
    if not obj.collidable:
        return  # Exempted objects are not registered for collision
    for square in obj.squares:
        offset_x, offset_y, width, height, _ = square
        for i in range(width):
            for j in range(height):
                grid_pos = (obj.x + offset_x + i, obj.y + offset_y + j)
                if grid_pos in grid and obj in grid[grid_pos]:
                    grid[grid_pos].remove(obj)
                    if not grid[grid_pos]:  # Clean up empty grid cells
                        del grid[grid_pos]

# Define a function to draw objects based on game-world pixel units and sizes
def draw_object(surface, x, y, squares):
    """Draw an object defined by a list of (offset_x, offset_y, width, height, color) tuples."""
    for square in squares:
        offset_x, offset_y, width, height, color = square
        pygame.draw.rect(surface, color, (
            (x + offset_x) * PIXEL_SIZE,  # Convert to raw screen pixels
            (y + offset_y) * PIXEL_SIZE,
            width * PIXEL_SIZE, height * PIXEL_SIZE))  # Scale width and height

# Define the GameObject class using game-world pixel units and sizes
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
        self.x = x  # Position in game-world pixel units
        self.y = y  # Position in game-world pixel units
        self.squares = squares  # Structure of the object as squares (with sizes)
        self.collidable = collidable  # Collision flag
        register_in_grid(self)

    def draw(self, surface, camera):
        """Draw the object using the camera offset."""
        draw_object(surface, self.x - camera.x, self.y - camera.y, self.squares)

    def move(self, dx, dy):
        """Move the object by dx, dy in game-world pixel units."""
        if not self.collidable:
            # If not collidable, simply move without collision checks
            self.x += dx
            self.y += dy
            return

        # Unregister the object from the current grid
        unregister_from_grid(self)

        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collisions in the new position
        if self.check_collision(new_x, new_y):
            # Collision occurred, re-register at the current position and exit
            register_in_grid(self)
            return  # Cancel movement if a collision occurs

        # Apply the move if no collision
        self.x = new_x
        self.y = new_y

        # Register the object in the new grid position
        register_in_grid(self)

    def check_collision(self, new_x, new_y):
        """Check if moving to the new position would cause a collision."""
        for square in self.squares:
            offset_x, offset_y, width, height, _ = square
            # Check for collision by looking at the grid positions that this square would occupy
            for i in range(width):
                for j in range(height):
                    new_grid_pos = (new_x + offset_x + i, new_y + offset_y + j)
                    if new_grid_pos in grid:
                        for other in grid[new_grid_pos]:
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

# Define a simple camera class using game-world pixel units
class Camera:
    def __init__(self, width, height):
        self.x = 0  # Camera position in game-world pixel units
        self.y = 0
        self.width = width // PIXEL_SIZE  # Convert screen size to game-world units
        self.height = height // PIXEL_SIZE

    def update(self, target):
        """Center the camera on the target object, ensuring it stays within the map bounds."""
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

        # Clamp camera within the map boundaries
        self.x = max(0, min(self.x, MAP_WIDTH - self.width))
        self.y = max(0, min(self.y, MAP_HEIGHT - self.height))

# Main game loop
def main():
    clock = pygame.time.Clock()  # For controlling the frame rate
    running = True

    # Define the character object with a 2x2 square size (in game-world units)
    character_squares = [
        (0, 0, 2, 2, (255, 0, 0)),  # Red square, 2x2
    ]
    character = GameObject(32, 24, character_squares)  # Position is in game-world units

    # Define a wall object that will cause a collision with a larger size
    wall_squares = [(0, 0, 3, 1, (0, 255, 0))]  # Green rectangle, 3x1
    wall = GameObject(40, 24, wall_squares)

    # Define an exempted object (e.g., decorative element) that does not collide
    decorative_squares = [(0, 0, 4, 4, (0, 0, 255))]  # Blue square, 4x4
    decorative = GameObject(50, 30, decorative_squares, collidable=False)

    # Create the camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    while running:
        clock.tick(FPS)  # Ensure the game runs at the desired frame rate

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the game window
                running = False

        # Get the current state of the keyboard
        keys_pressed = pygame.key.get_pressed()

        # Handle movement in game-world pixel units
        dx, dy = 0, 0
        if keys_pressed[pygame.K_LEFT]:
            dx = -char_speed
        if keys_pressed[pygame.K_RIGHT]:
            dx = char_speed
        if keys_pressed[pygame.K_UP]:
            dy = -char_speed
        if keys_pressed[pygame.K_DOWN]:
            dy = char_speed

        character.move(dx, dy)

        # Update the camera to follow the character
        camera.update(character)

        # Fill the screen with the background color
        screen.fill(BG_COLOR)

        # Draw all objects
        wall.draw(screen, camera)
        decorative.draw(screen, camera)  # Decorative object (non-collidable)
        character.draw(screen, camera)

        # FPS Monitoring
        current_fps = clock.get_fps()
        if current_fps < FPS_THRESHOLD:
            # Render the warning text
            screen.blit(warning_text, (10, 10))

        # Optional: Display current FPS for debugging (comment out if not needed)
        # fps_text = font.render(f'FPS: {int(current_fps)}', True, (255, 255, 255))
        # screen.blit(fps_text, (10, 40))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
