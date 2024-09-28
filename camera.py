from settings import settings

class Camera:
    def __init__(self):
        self.x = 0  # Camera position in game-world pixel units
        self.y = 0
        self.width = settings.screen_width // settings.pixel_size  # Convert screen size to game-world units
        self.height = settings.screen_height // settings.pixel_size

    def update(self, target):
        """Center the camera on the target object, ensuring it stays within the map bounds."""
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

        # Clamp camera within the map boundaries
        self.x = max(0, min(self.x, settings.map_width - self.width))
        self.y = max(0, min(self.y, settings.map_height - self.height))
