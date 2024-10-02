from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, ValidationError
from game_object import GameObject
from square import Square

ValueType = Union[int, str]

# Base class for all action models
class Action(BaseModel):
    type: str
    next: Optional[str] = None

# Specific action model classes
class SleepAction(Action):
    duration: ValueType

class MoveAction(Action):
    x: ValueType
    y: ValueType

class DisappearAction(Action):
    pass

class CreateObjectAction(Action):
    # event_object: Dict[str, Any]  # Should reference an EventObject later
    event_object: "EventObject"

class SetVariableAction(Action):
    name: str
    value: ValueType

class AddValueAction(Action):
    value1: ValueType
    value2: ValueType
    dest_name: str

class IfEqAction(Action):
    value1: ValueType
    value2: ValueType
    true: Optional[str] = None
    false: Optional[str] = None

class IfGtAction(Action):
    value1: ValueType
    value2: ValueType
    true: Optional[str] = None
    false: Optional[str] = None

# Wrapper classes for each action, with execute hooks
class ActionWrapper:
    def __init__(self, model: Action, event_object):
        self.model = model
        self.event_object = event_object

    def execute(self):
        # By default, go to the next command
        self.event_object.set_current_action(self.model.next)
        return self.event_object.execute_current_action()

# Define wrappers for each specific action type
class SleepActionWrapper(ActionWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0

    def execute(self):
        print(f"Sleeping for {self.counter} out of {self.model.duration} frames.")

        if self.counter == self.model.duration:
            self.counter = 0
            return super().execute()
        
        self.counter += 1
        return

class MoveActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Moving by x: {self.model.x}, y: {self.model.y}")

        self.event_object.move(self.model.x, self.model.y)

        return super().execute()

class DisappearActionWrapper(ActionWrapper):
    def execute(self):
        self.event_object.unregister()
        return

class CreateObjectActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Creating object with event_object: {self.model.event_object}")

        self.event_object.create_subobject(self.model.event_object)

        return super().execute()

class SetVariableActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Setting variable {self.model.name} to {self.model.value}")

        self.event_object.variables[self.model.name] = self.event_object.get_value(self.model.value)

        return super().execute()

class AddValueActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Adding {self.model.value1} and {self.model.value2} into {self.model.dest_name}")

        self.event_object.variables[self.model.dest_name] = self.event_object.get_value(self.model.value1) + self.event_object.get_value(self.model.value2)

        return super().execute()

class IfEqActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Checking if {self.model.value1} == {self.model.value2}")

        if self.event_object.get_value(self.model.value1) == self.event_object.get_value(self.model.value2):
            self.event_object.set_current_action(self.model.true)

        else:
            self.event_object.set_current_action(self.model.false)
        
        return self.event_object.execute_current_action()

class IfGtActionWrapper(ActionWrapper):
    def execute(self):
        print(f"Checking if {self.model.value1} > {self.model.value2}")

        if self.event_object.get_value(self.model.value1) > self.event_object.get_value(self.model.value2):
            self.event_object.set_current_action(self.model.true)

        else:
            self.event_object.set_current_action(self.model.false)
        
        return self.event_object.execute_current_action()

# Factory method to create wrappers based on action type
def create_action_wrapper(action_model: Action, event_object) -> ActionWrapper:
    if action_model.type == "sleep":
        return SleepActionWrapper(action_model, event_object)
    elif action_model.type == "move":
        return MoveActionWrapper(action_model, event_object)
    elif action_model.type == "disappear":
        return DisappearActionWrapper(action_model, event_object)
    elif action_model.type == "create_object":
        return CreateObjectActionWrapper(action_model, event_object)
    elif action_model.type == "set_variable":
        return SetVariableActionWrapper(action_model, event_object)
    elif action_model.type == "add_value":
        return AddValueActionWrapper(action_model, event_object)
    elif action_model.type == "if_eq":
        return IfEqActionWrapper(action_model, event_object)
    elif action_model.type == "if_gt":
        return IfGtActionWrapper(action_model, event_object)
    else:
        return ActionWrapper(action_model, event_object)  # Fallback for unhandled actions

# Function to parse action models separately
def parse_action_models(action_dict: Dict[str, Dict[str, Any]]) -> Dict[str, Action]:
    parsed_actions = {}
    for key, action_data in action_dict.items():
        action_type = action_data.get("type")
        try:
            if action_type == "sleep":
                parsed_actions[key] = SleepAction.parse_obj(action_data)
            elif action_type == "move":
                parsed_actions[key] = MoveAction.parse_obj(action_data)
            elif action_type == "disappear":
                parsed_actions[key] = DisappearAction.parse_obj(action_data)
            elif action_type == "create_object":
                parsed_actions[key] = CreateObjectAction.parse_obj(action_data)
            elif action_type == "set_variable":
                parsed_actions[key] = SetVariableAction.parse_obj(action_data)
            elif action_type == "add_value":
                parsed_actions[key] = AddValueAction.parse_obj(action_data)
            elif action_type == "if_eq":
                parsed_actions[key] = IfEqAction.parse_obj(action_data)
            elif action_type == "if_gt":
                parsed_actions[key] = IfGtAction.parse_obj(action_data)
            else:
                parsed_actions[key] = Action.parse_obj(action_data)  # Fallback for unknown types
        except ValidationError as e:
            print(f"Error parsing action '{key}': {e}")
    return parsed_actions

# Define the EventObject class, which contains a model and actions
class ObjectModel(BaseModel):
    x_offset: int
    y_offset: int
    width: int
    height: int
    color: List[int]
    invisible: Optional[bool] = False

    def to_square(self):
        return Square(self.x_offset, self.y_offset, self.width, self.height, self.color, invisible=self.invisible)

class EventObject(BaseModel):
    type: str
    model: List[ObjectModel]
    actions: Dict[str, Dict[str, Any]]  # Raw dicts, will be parsed separately
    on_collision: Optional[Dict[str, Dict[str, Any]]] = None  # Same as actions

# Define the Ability class that contains the trigger and event object
class Trigger(BaseModel):
    type: str
    key: Optional[str] = None
    period: Optional[int] = None

class Ability(BaseModel):
    trigger: Trigger
    event_object: EventObject

class CustomEventObject(GameObject):
    def __init__(self, event_object_description, original_game_object):
        self.event_object_description = event_object_description
        self.action_descriptions = parse_action_models(self.event_object_description.actions)

        event_object_model = self.event_object_description.model
        squares = [square.to_square() for square in event_object_model]

        super().__init__(original_game_object.x, original_game_object.y, squares, self.event_object_description.type, collidable=False)

        self.variables = {}
        self.actions = {}

        for action_key, action_model in self.action_descriptions.items():
            self.actions[action_key] = create_action_wrapper(action_model, self)

        self.current_key = 'entry'

    def on_frame(self, events, keys_pressed):
        self.execute_current_action()

    def set_current_action(self, new_action_key):
        self.current_key = new_action_key

    def execute_current_action(self):
        self.actions[self.current_key].execute()

    def get_value(self, value: ValueType):
        if type(value) == str:
            return self.variables[value]
        
        return value
    
    def create_subobject(self, event_object_description):
        CustomEventObject(event_object_description, self).register()

CreateObjectAction.update_forward_refs()
