from definitions import game_states

class GlobalObjects:
    game_state = game_states.MAIN_MENU

    main_menu = None
    camera = None
    collision_grid = None

    game_objects = {}

globals = GlobalObjects()
