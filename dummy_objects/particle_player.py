from general_objects.player import Player

class ParticlePlayer(Player):
    COLOR_ROTATION = [
        (255, 0, 0),
        (125, 125, 0),
        (125, 0, 125),
    ]

    def __init__(self):
        super().__init__()

        self.color_state = 0

    def on_collision_passive(self, other):
        self.color_state += 1
        self.color_state = self.color_state % len(self.COLOR_ROTATION)

        self.squares[0].color = self.COLOR_ROTATION[self.color_state]

        self.unregister()
        self.register()

        return super().on_collision_passive(other)
