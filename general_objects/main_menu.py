from definitions import game_states
from menu import Menu, Button, Slider, TextBox
from global_objects import globals

class MainMenu:
    MAIN = 'MAIN'
    SETTINGS = 'SETTINGS'

    def __init__(self):
        self.state = self.MAIN

        self.init_main_menu()
        self.init_settings_menu()

    def init_main_menu(self):
        self.main_menu = Menu(exit_callback=self.menu_exit_callback)

        play_button = Button("Play", 140, 50, lambda: self.on_play_click())
        settings_button = Button("Settings", 140, 50, lambda: self.switch_submenu(self.SETTINGS))

        self.main_menu.add_item(play_button)
        self.main_menu.add_item(settings_button)

    def init_settings_menu(self):
        self.settings_menu = Menu(
            exit_callback=self.menu_exit_callback,
            parent_menu_state=self.MAIN)

        # Add a volume slider
        volume_slider = Slider("Volume", 200, 20, 0, 100, 50)
        self.settings_menu.add_item(volume_slider)

        # Add a text box
        text_box = TextBox("Text Box", 200, 40)
        self.settings_menu.add_item(text_box)

        # Add Apply button
        def apply_settings():
            print(f"Settings applied: Volume = {volume_slider.current_value}, Text = '{text_box.text}'")
            self.menu_exit_callback()

        apply_button = Button("Apply", 100, 50, apply_settings)
        self.settings_menu.add_item(apply_button)

        # Add Cancel button
        def cancel_settings():
            self.menu_exit_callback()

        cancel_button = Button("Cancel", 100, 50, cancel_settings)
        self.settings_menu.add_item(cancel_button)

    def get_menu(self):
        if self.state == self.MAIN:
            return self.main_menu
        elif self.state == self.SETTINGS:
            return self.settings_menu

    def on_play_click(self):
        self.switch_global_state(game_states.RUNNING)
        globals.current_level.start()

    def switch_global_state(self, state):
        print(f"Switching to game state {state}")
        globals.game_state = state

    def switch_submenu(self, submenu):
        print(f"switching to submenu {submenu}")
        self.state = submenu

    def menu_exit_callback(self):
        if self.get_menu().parent_menu_state:
            self.switch_submenu(self.get_menu().parent_menu_state)
