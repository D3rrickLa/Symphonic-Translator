import unittest
from unittest.mock import patch, mock_open
from src.models.profile_detection import ProfileDetection

class TestProfileDetection(unittest.TestCase):

    def setUp(self):
        self.default_profile = {
            "default": {
                "file_path" : "None",
                "profile_name" : "default",
                "KEYS": {
                    "69" : {"action": "1", "params": {"command": "start notepad"}},
                    "70" : {"action": "1", "params": {"command": "start chrome"}}
                }
            }
        }
        self.profile_detection = ProfileDetection()
        

    def test_default_profile(self):
        self.assertEqual(self.default_profile, self.profile_detection.default_profile)

    def test__load_profiles(self):

        current_profiles = {
            "default": {
                "file_path": "NONE",
                "KEY": {
                    "69": {
                        "action": "run_command",
                        "params": {
                            "command": "start notepad"
                        }
                    },
                    "70": {
                        "action": "run_command",
                        "params": {
                            "command": "start chrome"
                        }
                    }
                },
                "cc": {
                    "1": {
                        "action": "none"
                    }
                },
                "pw": {
                    "1": {
                        "action": "print_message",
                        "params": {
                            "message": "Pitch wheel moved!"
                        }
                    }
                }
            },
            "chrome": {
                "file_path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "KEY": {
                    "35": {
                        "action": "2",
                        "params": {
                            "KEYBOARD_SHORTCUT": "CTRL + T"
                        }
                    }
                }
            }
        }

        loaded_profiles = self.profile_detection._load_profiles()
        self.assertEqual(loaded_profiles, current_profiles)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test__load_profiles_file_not_found_boundary(self, mock_open):
        with self.assertRaises(FileNotFoundError):
            result = self.profile_detection._load_profiles("non_existent.json")
            self.assertEqual(result, self.default_profile) 


if __name__ == '__main__':
    unittest.main()