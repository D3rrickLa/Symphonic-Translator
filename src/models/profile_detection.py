import json 
import os 
import pygetwindow as gw 
from src.models.midi import Midi
from src.models.enums import MidiActionType, MidiControlType

class ProfileDetection():
    def __init__(self):
        self._default_profile = {
            "default": {
                "file_path" : "None",
                "profile_name" : "default",
                "KEYS": {
                    "69" : {"action": "1", "params": {"command": "start notepad"}},
                    "70" : {"action": "1", "params": {"command": "start chrome"}}
                }
            }
        }
        self._profile_default_name="profiles.json"
    
    @property
    def default_profile(self):
        return self._default_profile
    
    @property
    def profile_name(self):
        return self._profile_default_name
    
    def _load_profiles(self, file_path: str):
        if not file_path:
            file_path = self.profile_name

        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return self._generate_default_profile(file_path)
        except json.JSONDecodeError:
            print(f"JSON Decode Error: {file_path} is corrupted. Replacing with default profiles.")
            return self._generate_default_profile(file_path)

    def _generate_default_profile(self, file_path):
        with open(file_path, "w") as file: 
            json.dump(self.default_profile, file, indent=4)
            return self.default_profile

    def get_profile(self, profiles):
        active_application = gw.getActiveWindow()
        for app, macros in profiles.items():
            if app in active_application:
                return macros
        return profiles["default"]

    def save_profile(self, midi: Midi, id: str = None):
        profile_data = {}

        if os.path.exists(self.profile_name):
            with open(self.profile_name, "r") as file:
                try:
                    profile_data = json.load(file)
                except json.JSONDecodeError:
                    print(f"JSON Decode Error: {file} is corrupted. Replacing with default profiles.")

        # if midi.profile_name not in profile_data:
        #     profile_data[midi.profile_name] = {}        
        
        # if midi.control_type.name not in profile_data[midi.profile_name]:
        #     profile_data[midi.profile_name][midi.control_type.name] = {}
                
        profile_data.setdefault(midi.profile_name, {}).setdefault(midi.control_type.name, {})
        action_type_str = str(midi.action_type.value).lower()
        action_param = self._get_action_type(midi.action_type)

        match(midi.control_type.name):
            case MidiControlType.KEY:
                profile_data[midi.profile_name][midi.control_type.name][str(midi.midi_note)] = {
                    "action": action_type_str,
                    "params": {action_param: midi.midi_value},
                }

            case MidiControlType.CONTROL_CHANGE:
                profile_data[midi.profile_name][midi.control_type.name][id] = {
                    "action": action_type_str,
                    "params": {
                        "cc_control_id": midi.midi_note,
                        action_param: midi.midi_value,
                    },
                }

    def _get_action_type(self, action_type: MidiActionType):   
        match(action_type):
            case MidiActionType.RUN_COMMAND:
                return "COMMAND"
            case MidiActionType.KEYBOARD_SHORTCUT:
                return "KEYBOARD_SHORTCUT"
            case MidiActionType.RUN_SCRIPT:
                return "RUN_SCRIPT"
            case MidiActionType.PRINT_MESSAGE:
                return "PRINT_MESSAGE"
            case _:
                return "NONE"