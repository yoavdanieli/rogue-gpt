{
  "trigger": {
    "type": "keypress"/"mouseclick"/"periodic",
    "key": str  # In case this is keypress, the key that needs to be pressed in pygame format, for example "K_a"
    "perdiod": int # In case this is periodic, what's the interval between triggers. In frames, 60 FPS
  },

  # A new object will be created for the event that will start doing what we desire.
  # The new object is created at the position of the object that created it, the first object
  # is created by the player.
  "event_object": {
    "type": "object_types.PARTICLE",   # Currently only particles are supported

    # The model of the object as a list of colored squares. Will be used for collision as well
    "model": [
      {
        "x_offset": int,
        "y_offset": int,
        "width": int,
        "height": int,
        "color": [int, int, int], # RGB
        "invisible": bool?,
      },
      ...
    ],

    # Every action is NOT performed within its own frame, they are eagerly executed as fast as possible.
    # Use sleeps to control the pace of execution.
    #
    # You can define variables and perform very basic arithmetic (+-) and comparisons (==, >) to control
    # your flow.
    # Only use variables you have explicitly declared
    "actions": {
      "entry": { # Entry must exist and will be called at the start
        "type": "sleep",  # This command can be used to skip frames
        "duration": int/str, # In frames, 60 FPS. int for a constant value, str for a variable name 
        "next": str # ID of the next operation
      },
      "1": {  # ID can be any string, will be referenced by "next" and other fields in other entries
        "type": "create_object",
        "event_object": {
          # Same as event_object above, can have its own independent action flow
        },
        "next": str,
      },
      "2": {
        "type": "move",   # Move once in the current frame
        "x": int/str,     # int for a constant value, str for a variable name
        "y": int/str,
        "next": str,
      },
      "3": {
        "type": "disappear",    # End the life of the current object. No "next" field as this is the ending of the current object
      },
      "4": {
        "type": "set_variable", # Set a variable with the given name. Variables can currently only be numbers
        "name": str,
        "value": int,
      },
      "5": {
        "type": "add_value",    # Add two values into a variables. The source values can be int for a const or string for an existing variable name
        "value1": str/int,
        "value2": str/int,
        "dest_name": str,
      },
      "6": {
        "type": "if_eq",        # Check if two values are equal. Values can be int for constants or str for variable name
        "value1": str/int,
        "value2": str/int,
        "true": str?,           # The ID of the next step if the evaluation is true, non mandatory field
        "false": str?,          # The ID of the next step if the evaluation is false, non mandatory field
      },
      "7": {
        "type": "if_gt",        # Check if value1 is greater than value2. Values can be int for constants or str for variable name
        "value1": str/int,
        "value2": str/int,
        "true": str?,           # The ID of the next step if the evaluation is true, non mandatory field
        "false": str?,          # The ID of the next step if the evaluation is false, non mandatory field
      },
    },

    "on_collision": {
      # Same as actions field, with the trigger value being the type of the object we collided with
    }
  },
}