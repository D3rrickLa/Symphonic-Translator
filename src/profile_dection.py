import json
import pygetwindow as gw
from src.MidiItem import MidiElement, MidiControlType
class ProfileDetection():
    def __init__(self):
        self.default_profile = {
            "default": {
                "notes": {
                    "69": {"action": "run_command", "params": {"command": "start notepad"}},
                    "70": {"action": "run_command", "params": {"command": "start chrome"}}
                },
                "cc": {
                    "1": {"action": "none"}
                },
                "pw": {
                    "1": {"action": "print_message", "params": {"message": "Pitch wheel moved!"}}
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
        return profiles # fallback
    
    def save_profile(self, item: MidiElement):
        profile_data = {}
        profile_data[item.profile_name] = {}
        
        profile_data[item.profile_name]["notes"] = {}
        if item.control_type == MidiControlType.KEY:
            profile_data[item.profile_name]["notes"][item.midi_note] = {
                "action" : str(item.action_type).lower(),
                "params" : {"command_testing" : item.get_value()}
            }
        with open("profiles.json", "w") as file:
            json.dump(profile_data, file, indent=4)

    def run_app(self):
        loaded_profiles = self.load_profiles()
        return self.get_profile(loaded_profiles)

