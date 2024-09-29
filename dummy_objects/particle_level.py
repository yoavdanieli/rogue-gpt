import random
from settings import settings
from general_objects.level import Level
from dummy_objects.particle_player import ParticlePlayer
from dummy_objects.particle import Particle
from dummy_objects.background import Background
from dummy_objects.map_outline_barrier import MapOutlineBarrier
from game_object import GameObject

class ParticleLevel(Level):
    def __init__(self, screen):
        super().__init__(screen)

        self.player = ParticlePlayer()

        self.objects = [Background(), MapOutlineBarrier()]

        self.particle_delay = 1
        self.counter = 1
      
    def on_frame(self, events, keys_pressed):
        if self.counter % self.particle_delay == 0:
            # Create a new particle at the top of the screen, moving downwards diagonally
            Particle(random.randint(0, settings.map_width * 2), 0, -1, 1).register()

        self.counter += 1
