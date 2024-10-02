ability_desc = {
    "trigger": {
        "type": "keypress",
        "key": "K_q"
    },
    "event_object": {
        "type": "PARTICLE",
        "model": [
        {
            "x_offset": 0,
            "y_offset": 0,
            "width": 1,
            "height": 1,
            "color": [128, 0, 128],  # Purple
            "invisible": False
        }
        ],
        "actions": {
        "entry": {
            "type": "set_variable",
            "name": "distance_travelled",
            "value": 0,
            "next": "move"
        },
        "move": {
            "type": "sleep",  # Adding sleep to control travel time
            "duration": 5,   # Wait for 5 frames between each movement
            "next": "move_step"
        },
        "move_step": {
            "type": "move",
            "x": 0,
            "y": -1,  # Move upwards (negative y direction)
            "next": "check_distance"
        },
        "check_distance": {
            "type": "add_value",
            "value1": "distance_travelled",
            "value2": 1,
            "dest_name": "distance_travelled",
            "next": "if_reached_10"
        },
        "if_reached_10": {
            "type": "if_eq",
            "value1": "distance_travelled",
            "value2": 10,
            "true": "split_particles",
            "false": "move"
        },
        "split_particles": {
            "type": "create_object",
            "event_object": {
            "type": "PARTICLE",
            "model": [
                {
                "x_offset": 0,
                "y_offset": 0,
                "width": 1,
                "height": 1,
                "color": [128, 0, 128],  # Purple
                "invisible": False
                }
            ],
            "actions": {
                "entry": {
                "type": "move",
                "x": -1,  # Left particle
                "y": 0,
                "next": "disappear"
                },
                "disappear": {
                "type": "disappear"
                }
            }
            },
            "next": "split_right"
        },
        "split_right": {
            "type": "create_object",
            "event_object": {
            "type": "PARTICLE",
            "model": [
                {
                "x_offset": 0,
                "y_offset": 0,
                "width": 1,
                "height": 1,
                "color": [128, 0, 128],  # Purple
                "invisible": False
                }
            ],
            "actions": {
                "entry": {
                "type": "move",
                "x": 1,  # Right particle
                "y": 0,
                "next": "disappear"
                },
                "disappear": {
                "type": "disappear"
                }
            }
            },
            "next": "disappear"
        },
        "disappear": {
            "type": "disappear"
        }
        }
    }
}