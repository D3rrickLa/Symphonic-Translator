from enum import Enum
class MidiControlType(Enum):
    KEY = 0
    FADER = 1
    KNOB = 2
    PITCHWHEEL = 3

class Actions(Enum):
    NONE = 0
    RUN_COMMAND = 1
    KEYBOARD_SHORTCUT = 2
    RUN_SCRIPT = 3
    PRINT_MESSAGE = 4

class MidiElement():
    def __init__(self, control_type: MidiControlType, action_type: Actions, midi_channel=1, midi_note=None, value=None):
        self.control_type = control_type  # Assign control type from enum
        self.action_type = action_type
        self.midi_channel = midi_channel
        self.midi_note = midi_note
        self.value = value
        
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def describe(self):
        """Prints a description of the MIDI element."""
        return (f"Type: {self.control_type.name}, "
                f"Action: {self.action_type.name}, "
                f"Channel: {self.midi_channel}, "
                f"Note: {self.midi_note}, "
                f"Value: {self.value}")


