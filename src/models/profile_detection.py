import json 
import os 
import pygetwindow as gw 
from src.models.midi import Midi
from src.models.enums import MidiActionType, MidiControlType

class ProfileDetection():
    def __init__(self):
        self._default_profile = {
            "default": { # this is what the users calls the profile
                "file_path" : "None",
                "program_window_name" : "default", # what gw uses to see what user is actively on
                "KEY": {
                    "69" : {"action": "1", "params": {"command": "start notepad"}},
                    "70" : {"action": "1", "params": {"command": "start chrome"}}
                },
                "CONTROL_CHANGE": {
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
    
    def get_loaded_profiles(self, file_path:str = None):
        return self._load_profiles(file_path)

    def _load_profiles(self, file_path: str = None):
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

    def get_profile_by_key(self, id: int, profile, type):
        profile_data = {}
        with open(self.profile_name, "r") as file:
            try:
                profile_data = json.load(file)
                _key = f"{id}"
                return profile_data[str(profile)][type].get(_key, None)
            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"profile detection error: {e}")
                return None


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
            case MidiControlType.KEY.name:
                profile_data[midi.profile_name][midi.control_type.name][str(midi.midi_note)] = {
                    "action": action_type_str,
                    "params": {action_param: midi.midi_value},
                }

            case MidiControlType.CONTROL_CHANGE.name:
                profile_data[midi.profile_name][midi.control_type.name][id] = {
                    "action": action_type_str,
                    "params": {
                        "cc_control_id": midi.midi_note,
                        action_param: midi.midi_value,
                    },
                }
            case _:
                print("NO MATCH")

        with open(self.profile_name, "w") as file:
            json.dump(profile_data, file, indent=4)
            pass

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