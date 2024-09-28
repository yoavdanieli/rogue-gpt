import pygame
import sys

from definitions import game_states
from settings import settings
from global_objects import globals
from game_object import GameObject
from general_objects.player import Player
from general_objects.main_menu import MainMenu
from camera import Camera
from collision import CollisionGrid

# Initialize Pygame
pygame.init()

# Init global objects
globals.main_menu = MainMenu()
globals.camera = Camera()
globals.collision_grid = CollisionGrid()

# Game settings
BG_COLOR = (0, 0, 0)  # Background color (black)
FPS = 60  # Frames per second
FPS_THRESHOLD = 60  # Threshold to trigger FPS warning

# Create the screen object
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Pixelated Game with Enhanced Features")

# Font settings for FPS warning
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
warning_text = font.render('Warning: FPS below 60!', True, (255, 0, 0))


def main():
    clock = pygame.time.Clock()  # For controlling the frame rate
    running = True

    # Create the player
    player = Player()
    player.register()

    # Define a wall object that will cause a collision with a larger size
    wall_squares = [(0, 0, 3, 1, (0, 255, 0))]  # Green rectangle, 3x1
    GameObject(40, 24, wall_squares).register()

    # Define an exempted object (e.g., decorative element) that does not collide
    decorative_squares = [(0, 0, 4, 4, (0, 0, 255))]  # Blue square, 4x4
    GameObject(50, 30, decorative_squares, collidable=False).register()

    while running:
        clock.tick(FPS)  # Ensure the game runs at the desired frame rate

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:  # Close the game window
                running = False

        if globals.game_state == game_states.RUNNING:
            # Get the current state of the keyboard
            keys_pressed = pygame.key.get_pressed()

            # Exit the game on escape
            # TODO: Return to main menu?
            if keys_pressed[pygame.K_ESCAPE]:
                running = False

            # Handle player input
            player.handle_keys(keys_pressed)

            # Update the camera to follow the character
            globals.camera.update(player)

            # Fill the screen with the background color
            screen.fill(BG_COLOR)

            # Draw all objects
            for _, obj in globals.game_objects.items():
                obj.draw(screen)

        elif globals.game_state == game_states.MAIN_MENU:
            for event in events:
                globals.main_menu.get_menu().handle_event(event)
            globals.main_menu.get_menu().draw(screen)

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