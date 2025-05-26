from enum import Enum

import keyboard


class BtnTrigger(Enum):
    ContinuouslyPressedTrigger = 1
    OnPressTrigger = 2
    OnReleaseTrigger = 3


class BtnControl:
    def __init__(self, button, trigger, callback):
        self.button = button
        self.trigger = trigger
        self.callback = callback

        self.last_state = keyboard.is_pressed(button)

    def check(self):
        current_state = keyboard.is_pressed(self.button)

        if self.trigger == BtnTrigger.ContinuouslyPressedTrigger:
            return_bool = current_state
        elif self.trigger == BtnTrigger.OnPressTrigger:
            return_bool = current_state == True and self.last_state == False
        elif self.trigger == BtnTrigger.OnReleaseTrigger:
            return_bool = current_state == False and self.last_state == True
        else:
            raise f"Trigger {self.trigger} not supported"

        self.last_state = current_state
        return return_bool
