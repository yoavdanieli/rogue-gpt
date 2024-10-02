from general_objects.player import Player
from custom_event_engine.custom_event_engine import Ability, CustomEventObject
from custom_event_level_test.ability1 import ability_desc as ability_desc1
from custom_event_level_test.ability2 import ability_desc as ability_desc2

class CustomEventPlayer(Player):
    def __init__(self):
        super().__init__()

        self.ability_desc = ability_desc2

        self.ability = Ability.parse_obj(self.ability_desc)

        self.counter = 0

        # self.custom_events = []

    def on_frame(self, events, keys_pressed):
        self.counter += 1

        if self.counter % 30 == 0:
            CustomEventObject(self.ability.event_object, self).register()
