from global_objects import globals

class Level:
    BLACK = (0, 0, 0)

    def __init__(self, screen):
        self.running = False
        self.player = None
        self.objects = []

        self.screen = screen
    
    def start(self):
        for obj in self.objects:
            obj.register()

        self.player.register()
    
    def end(self):
        # TODO: Maybe find a better way of handling dynamically created objects
        for obj in globals.game_objects:
            obj.unregister()
    
    def handle_frame(self, events, keys_pressed):
        # Handle player input
        self.player.handle_keys(keys_pressed)

        # Update the camera to follow the character
        globals.camera.update(self.player)

        self.on_frame(events, keys_pressed)

        # Fill the screen with the background color
        self.screen.fill(self.BLACK)

        # Draw all objects
        for _, obj in globals.game_objects.items():
            obj.draw(self.screen)

    def on_frame(self, events, keys_pressed):
        """
        Callback for levels to implement
        """
        pass
