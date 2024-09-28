import pygame

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Window dimensions
PIXEL_SIZE = 10  # Size of a "pixel" in the game
BG_COLOR = (0, 0, 0)  # Background color (black)
FPS = 60  # Frames per second

# Modular settings for character movement
char_speed = 5  # Speed of the character in pixels per frame

# Map settings
MAP_WIDTH, MAP_HEIGHT = 1280, 960  # Map dimensions (can be larger than screen)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixelated Game with Camera")

# Define a function to draw objects made of colored squares
def draw_object(surface, x, y, squares):
    """Draw an object defined by a list of (offset_x, offset_y, color) tuples."""
    for square in squares:
        offset_x, offset_y, color = square
        pygame.draw.rect(surface, color, (x + offset_x, y + offset_y, PIXEL_SIZE, PIXEL_SIZE))

# Define the character class
class GameObject:
    def __init__(self, x, y, squares):
        self.x = x
        self.y = y
        self.squares = squares  # The structure of the object as a set of squares

    def draw(self, surface, camera):
        """Draw the object using the camera offset."""
        draw_object(surface, self.x - camera.x, self.y - camera.y, self.squares)

    def move(self, dx, dy):
        """Move the object by dx, dy."""
        self.x += dx
        self.y += dy

        # Clamp the position within the map boundaries
        self.x = max(0, min(self.x, MAP_WIDTH - PIXEL_SIZE))
        self.y = max(0, min(self.y, MAP_HEIGHT - PIXEL_SIZE))

# Define a simple camera class to follow the player
class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        """Center the camera on the target object, ensuring it stays within the map bounds."""
        self.x = target.x + PIXEL_SIZE // 2 - SCREEN_WIDTH // 2
        self.y = target.y + PIXEL_SIZE // 2 - SCREEN_HEIGHT // 2

        # Clamp camera within the map
        self.x = max(0, min(self.x, MAP_WIDTH - SCREEN_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT - SCREEN_HEIGHT))

# Main game loop
def main():
    clock = pygame.time.Clock()  # For controlling the frame rate
    running = True

    # Define the character object (using a 2x2 square for simplicity)
    character_squares = [
        (0, 0, (255, 0, 0)),  # Red squares for the character
        (PIXEL_SIZE, 0, (255, 0, 0)),
        (0, PIXEL_SIZE, (255, 0, 0)),
        (PIXEL_SIZE, PIXEL_SIZE, (255, 0, 0)),
    ]
    character = GameObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, character_squares)

    # Define the map as a set of colored squares
    map_squares = []
    for i in range(0, MAP_WIDTH, PIXEL_SIZE):
        for j in range(0, MAP_HEIGHT, PIXEL_SIZE):
            if (i + j) % (PIXEL_SIZE * 4) == 0:  # Simple checkered pattern
                map_squares.append((i, j, (0, 255, 0)))  # Green tiles for the map

    # Create the camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    while running:
        clock.tick(FPS)  # Ensure the game runs at the desired frame rate

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the game window
                running = False

        # Get the current state of the keyboard
        keys_pressed = pygame.key.get_pressed()

        # Handle movement
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

        # Draw the map (only visible squares within the camera view)
        for square in map_squares:
            offset_x, offset_y, color = square
            # Only draw if within camera view
            if camera.x - PIXEL_SIZE <= offset_x <= camera.x + SCREEN_WIDTH and \
               camera.y - PIXEL_SIZE <= offset_y <= camera.y + SCREEN_HEIGHT:
                pygame.draw.rect(screen, color, (offset_x - camera.x, offset_y - camera.y, PIXEL_SIZE, PIXEL_SIZE))

        # Draw the character
        character.draw(screen, camera)

        # Update the display
        pygame.display.flip()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()