from enum import Enum

class MidiControlType(Enum):
    KEY = 0
    CONTROL_CHANGE = 1
    PITCHWHEEL = 2

class MidiActionType(Enum):
    NONE = 0
    RUN_COMMAND = 1
    KEYBOARD_SHORTCUT = 2
    RUN_SCRIPT = 3
    PRINT_MESSAGE = 4