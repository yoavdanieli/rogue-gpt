import pygame
import sys
import json

from definitions import game_states
from settings import settings
from global_objects import globals
from dummy_objects.dummy_level import DummyLevel
from dummy_objects.particle_level import ParticleLevel
from custom_event_level_test.level import CusomEventLevel
from general_objects.main_menu import MainMenu
from camera import Camera
from collision import CollisionGrid

# Initialize Pygame
pygame.init()

# Game settings
FPS = 60  # Frames per second
FPS_THRESHOLD = 60  # Threshold to trigger FPS warning

# Create the screen object
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Pixelated Game with Enhanced Features")

# Font settings for FPS warning
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
warning_text = font.render('Warning: FPS below 60!', True, (255, 0, 0))

# Init global objects
globals.current_level = CusomEventLevel(screen)
globals.main_menu = MainMenu()
globals.camera = Camera()
globals.collision_grid = CollisionGrid()


def main():
    clock = pygame.time.Clock()  # For controlling the frame rate
    running = True

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

            globals.current_level.handle_frame(events, keys_pressed)

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