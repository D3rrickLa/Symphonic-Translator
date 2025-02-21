from src.models.enums import MidiControlType, MidiActionType
from dataclasses import dataclass, field

@dataclass
class Midi:
    id: float
    profile_name: str
    control_type: MidiControlType
    action_type: MidiActionType
    midi_channel: int = 1
    midi_note: str = None
    midi_value: str = field(default=None)

    @midi_value.setter
    def midi_value(self, new_value):
        if isinstance(new_value, str):
            self._midi_value = new_value
        else:
            raise ValueError("Midi value must be a string")
    
    def __str__(self):
        """Prints a description of the MIDI element."""
        return (f"Profile: {self.profile_name}, "
                f"Type: {self.control_type.name}, "
                f"Action: {self.action_type.name}, "
                f"Channel: {self.midi_channel}, "
                f"Note: {self.midi_note}, "
                f"Value: {self.midi_value}")