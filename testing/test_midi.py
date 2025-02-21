import unittest
from src.models.midi import Midi, MidiControlType, MidiActionType  # Replace your_module
from src.models.enums import MidiControlType, MidiActionType  # Replace your_module

class TestMidi(unittest.TestCase):

    def setUp(self):
        # Create common test data to avoid repetition
        self.valid_id = 1.0
        self.valid_profile_name = "My Profile"
        self.valid_control_type = MidiControlType.KEY  # Example
        self.valid_action_type = MidiActionType.PRINT_MESSAGE  # Example
        self.valid_midi_channel = 1
        self.valid_midi_note = "C4"
        self.valid_midi_value = "127"

    def test_midi_creation_valid_data(self):
        midi = Midi(self.valid_id, self.valid_profile_name, self.valid_control_type,
                    self.valid_action_type, self.valid_midi_channel, self.valid_midi_note, self.valid_midi_value)
        self.assertEqual(midi._id, self.valid_id)
        self.assertEqual(midi._profile_name, self.valid_profile_name)
        self.assertEqual(midi._control_type, self.valid_control_type)
        self.assertEqual(midi._action_type, self.valid_action_type)
        self.assertEqual(midi._midi_channel, self.valid_midi_channel)
        self.assertEqual(midi._midi_note, self.valid_midi_note)
        self.assertEqual(midi._midi_value, self.valid_midi_value)

    def test_midi_creation_default_values(self):
        midi = Midi(self.valid_id, self.valid_profile_name, self.valid_control_type, self.valid_action_type)
        self.assertEqual(midi._midi_channel, 1)  # Default
        self.assertIsNone(midi._midi_note)  # Default
        self.assertIsNone(midi._midi_value)  # Default

    def test_midi_value_setter_valid(self):
        midi = Midi(self.valid_id, self.valid_profile_name, self.valid_control_type,
                    self.valid_action_type)
        midi.midi_value = "64"
        self.assertEqual(midi._midi_value, "64")

    def test_midi_value_setter_invalid(self):
        midi = Midi(self.valid_id, self.valid_profile_name, self.valid_control_type,
                    self.valid_action_type)
        with self.assertRaises(ValueError):
            midi.midi_value = 127  # Invalid type

    def test_describe_method(self):
        midi = Midi(self.valid_id, self.valid_profile_name, self.valid_control_type,
                    self.valid_action_type, self.valid_midi_channel, self.valid_midi_note, self.valid_midi_value)
        description = midi.describe()
        expected_description = (f"Profile: {self.valid_profile_name}, "
                                f"Type: {self.valid_control_type.name}, "
                                f"Action: {self.valid_action_type.name}, "
                                f"Channel: {self.valid_midi_channel}, "
                                f"Note: {self.valid_midi_note}, "
                                f"Value: {self.valid_midi_value}")
        self.assertEqual(description, expected_description)

    # Example of testing with different enum values (important!)
    def test_midi_creation_different_enum_values(self):
        midi1 = Midi(self.valid_id, self.valid_profile_name, MidiControlType.FADER, MidiActionType.PRINT_MESSAGE)
        self.assertEqual(midi1._control_type, MidiControlType.FADER)
        self.assertEqual(midi1._action_type, MidiActionType.PRINT_MESSAGE)

        midi2 = Midi(self.valid_id, self.valid_profile_name, MidiControlType.KEY, MidiActionType.RUN_COMMAND)
        self.assertEqual(midi2._control_type, MidiControlType.KEY)
        self.assertEqual(midi2._action_type, MidiActionType.RUN_COMMAND)


if __name__ == '__main__':
    unittest.main()