import json
import os
import pygetwindow as gw
from src.MidiItem import MidiElement, Actions
class ProfileDetection():
    def __init__(self):
        self.default_profile = {
            "default": {
                "KEYS": {
                    "69": {"action": "1", "params": {"command": "start notepad"}},
                    "70": {"action": "1", "params": {"command": "start chrome"}}
                },
                "cc": {
                    "1": {"action": "3"}
                },
                "pw": {
                    "1": {"action": "4", "params": {"message": "Pitch wheel moved!"}}
                }
            } 
        }

    def load_profiles(self, file_path="profiles.json"):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        
        except FileNotFoundError:
            with open(file_path, "w") as file:
                json.dump(self.default_profile, file, indent=4)
            return self.default_profile
        
        except json.JSONDecodeError:
            print(f"JSON Decode Error: {file_path} is corrupted. Replacing with default profiles.")
            with open(file_path, "w") as file:
                json.dump(self.default_profile, file, indent=4)
                return self.default_profile
            
    def get_active_app(self):
        active_window = gw.getActiveWindow()
        if active_window: return active_window.title.lower()
        return None

    def get_profile(self, profiles):
        active_app = self.get_active_app()
        
        for app, actions in profiles.items():

            if app in active_app:
                return actions
        return profiles["default"] # fallback
    
    def get_app_name_from_path(self, file_path):
        # Get the base name (e.g., "chrome.exe" from the full path)
        base_name = os.path.basename(file_path)
        
        # Remove the .exe extension (e.g., "chrome.exe" becomes "chrome")
        app_name, _ = os.path.splitext(base_name)
        
        print(app_name)
        return app_name.lower()  # Return the app name in lowercase for consistency

    def save_profile(self, item: MidiElement):
        profile_data = {}

        # Load existing data if the file exists
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as file:
                try:
                    profile_data = json.load(file)
                except json.JSONDecodeError:
                    profile_data = {}  # Handle case where file is empty or corrupted

        if item.profile_name not in profile_data:
            profile_data[item.profile_name] = {}

        if item.control_type.name not in profile_data[item.profile_name]:
            profile_data[item.profile_name][item.control_type.name] = {}

        # Add or update the note data
        profile_data[item.profile_name][item.control_type.name][item.midi_note] = {
            "action": str(item.action_type.value),
            "params": {self.get_param_type(item.action_type): item.get_value()}
        }

        # Write updated data back to the file
        with open("profiles.json", "w") as file:
            json.dump(profile_data, file, indent=4)

    def save_profile_non(self, item: MidiElement, id):
        """For the knobs and faders, will use this so that the assign knob/fader when click would load the right info"""
        profile_data = {}

        # Load existing data if the file exists
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as file:
                try:
                    profile_data = json.load(file)
                except json.JSONDecodeError:
                    profile_data = {}  # Handle case where file is empty or corrupted

        if item.profile_name not in profile_data:
            profile_data[item.profile_name] = {}

        if item.control_type.name not in profile_data[item.profile_name]:
            profile_data[item.profile_name][item.control_type.name] = {}

        # Add or update the note data
        profile_data[item.profile_name][item.control_type.name][str(id)] = {
            "action": str(item.action_type.value).lower(),
            "params": {
                "cc_control_id": item.midi_note,
                self.get_param_type(item.action_type): item.get_value()        
            },
            
        }

        # Write updated data back to the file
        with open("profiles.json", "w") as file:
            json.dump(profile_data, file, indent=4)
            pass

    def load_key_profile(self, id, profile, type):
        profile_data = {}
        with open("profiles.json", "r") as file:
            try:
                profile_data = json.load(file)
            except json.JSONDecodeError:
                profile_data = {}  # Handle case where file is empty or corrupted
        try:
            _key = f"{id}"
            return profile_data[str(profile)][type].get(_key, None)
        except Exception as e:
            print(e)
            return None

    def get_param_type(self, type: Actions):
        match(type):
            case Actions.RUN_COMMAND:
                return "command"
            case Actions.KEYBOARD_SHORTCUT:
                return "shortcut"
            case Actions.RUN_SCRIPT:
                return "script"
            case Actions.PRINT_MESSAGE:
                return "message"
            case _:
                return "none"

    def run_app(self):
        loaded_profiles = self.load_profiles()
        return self.get_profile(loaded_profiles)



   