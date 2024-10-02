ability_desc = {
  "trigger": {
    "type": "keypress",
    "key": "K_SPACE"
  },
  "event_object": {
    "type": "object_types.PARTICLE",
    "model": [
      {
        "x_offset": 0,
        "y_offset": 0,
        "width": 2,
        "height": 2,
        "color": [255, 0, 0]
      }
    ],
    "actions": {
      "entry": {
        "type": "set_variable",
        "name": "travel_distance",
        "value": 6,   # Further reduced distance
        "next": "move_upwards"
      },
      "move_upwards": {
        "type": "move",
        "x": 0,
        "y": -2,    # Move the projectile upwards by 2 pixels per frame
        "next": "countdown"
      },
      "countdown": {
        "type": "add_value",
        "value1": "travel_distance",
        "value2": -1,
        "dest_name": "travel_distance",
        "next": "check_distance"
      },
      "check_distance": {
        "type": "if_gt",
        "value1": "travel_distance",
        "value2": 0,
        "true": "sleep_then_move",  # Continue moving upwards
        "false": "explode"          # Explode when travel_distance <= 0
      },
      "sleep_then_move": {
        "type": "sleep",
        "duration": 1,    # Sleep for 1 frame before the next move
        "next": "move_upwards"
      },
      "explode": {
        "type": "create_object",
        "event_object": {
          "type": "object_types.PARTICLE",
          "model": [
            {"x_offset": 0, "y_offset": 0, "width": 1, "height": 1, "color": [255, 255, 0]}  # Explosion projectiles
          ],
          "actions": {
            "entry": {
              "type": "set_variable",
              "name": "distance",
              "value": 10,    # Diagonal projectiles will travel for 10 frames
              "next": "move_diag_1"
            },
            "move_diag_1": {
              "type": "move",
              "x": 2,
              "y": 2,    # Move diagonally down-right
              "next": "diag_countdown_1"
            },
            "diag_countdown_1": {
              "type": "add_value",
              "value1": "distance",
              "value2": -1,
              "dest_name": "distance",
              "next": "check_diag_1"
            },
            "check_diag_1": {
              "type": "if_gt",
              "value1": "distance",
              "value2": 0,
              "true": "sleep_then_move_diag_1",   # Continue moving diagonally
              "false": "disappear"
            },
            "sleep_then_move_diag_1": {
              "type": "sleep",
              "duration": 1,   # Sleep to avoid immediate recursion
              "next": "move_diag_1"
            },
            "disappear": {
              "type": "disappear"
            }
          }
        },
        "next": "explode_2"
      },
      "explode_2": {
        "type": "create_object",
        "event_object": {
          "type": "object_types.PARTICLE",
          "model": [
            {"x_offset": 0, "y_offset": 0, "width": 1, "height": 1, "color": [255, 255, 0]}
          ],
          "actions": {
            "entry": {
              "type": "set_variable",
              "name": "distance",
              "value": 10,
              "next": "move_diag_2"
            },
            "move_diag_2": {
              "type": "move",
              "x": -2,
              "y": 2,    # Move diagonally down-left
              "next": "diag_countdown_2"
            },
            "diag_countdown_2": {
              "type": "add_value",
              "value1": "distance",
              "value2": -1,
              "dest_name": "distance",
              "next": "check_diag_2"
            },
            "check_diag_2": {
              "type": "if_gt",
              "value1": "distance",
              "value2": 0,
              "true": "sleep_then_move_diag_2",
              "false": "disappear"
            },
            "sleep_then_move_diag_2": {
              "type": "sleep",
              "duration": 1,
              "next": "move_diag_2"
            },
            "disappear": {
              "type": "disappear"
            }
          }
        },
        "next": "explode_3"
      },
      "explode_3": {
        "type": "create_object",
        "event_object": {
          "type": "object_types.PARTICLE",
          "model": [
            {"x_offset": 0, "y_offset": 0, "width": 1, "height": 1, "color": [255, 255, 0]}
          ],
          "actions": {
            "entry": {
              "type": "set_variable",
              "name": "distance",
              "value": 10,
              "next": "move_diag_3"
            },
            "move_diag_3": {
              "type": "move",
              "x": -2,
              "y": -2,    # Move diagonally up-left
              "next": "diag_countdown_3"
            },
            "diag_countdown_3": {
              "type": "add_value",
              "value1": "distance",
              "value2": -1,
              "dest_name": "distance",
              "next": "check_diag_3"
            },
            "check_diag_3": {
              "type": "if_gt",
              "value1": "distance",
              "value2": 0,
              "true": "sleep_then_move_diag_3",
              "false": "disappear"
            },
            "sleep_then_move_diag_3": {
              "type": "sleep",
              "duration": 1,
              "next": "move_diag_3"
            },
            "disappear": {
              "type": "disappear"
            }
          }
        },
        "next": "explode_4"
      },
      "explode_4": {
        "type": "create_object",
        "event_object": {
          "type": "object_types.PARTICLE",
          "model": [
            {"x_offset": 0, "y_offset": 0, "width": 1, "height": 1, "color": [255, 255, 0]}
          ],
          "actions": {
            "entry": {
              "type": "set_variable",
              "name": "distance",
              "value": 10,
              "next": "move_diag_4"
            },
            "move_diag_4": {
              "type": "move",
              "x": 2,
              "y": -2,    # Move diagonally up-right
              "next": "diag_countdown_4"
            },
            "diag_countdown_4": {
              "type": "add_value",
              "value1": "distance",
              "value2": -1,
              "dest_name": "distance",
              "next": "check_diag_4"
            },
            "check_diag_4": {
              "type": "if_gt",
              "value1": "distance",
              "value2": 0,
              "true": "sleep_then_move_diag_4",
              "false": "disappear"
            },
            "sleep_then_move_diag_4": {
              "type": "sleep",
              "duration": 1,
              "next": "move_diag_4"
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
