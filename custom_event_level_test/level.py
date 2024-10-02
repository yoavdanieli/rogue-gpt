import random
from settings import settings
from general_objects.level import Level
from custom_event_level_test.custom_event_player import CustomEventPlayer
from dummy_objects.background import Background
from dummy_objects.map_outline_barrier import MapOutlineBarrier

class CusomEventLevel(Level):
    def __init__(self, screen):
        super().__init__(screen)

        self.player = CustomEventPlayer()

        self.objects = [Background(), MapOutlineBarrier()]
