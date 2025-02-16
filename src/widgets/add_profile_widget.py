from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QFileDialog,
    QLabel,
)
from PySide6.QtCore import Signal
from src.profile_detection import ProfileDetection
import json
import os

PROFILE_FILE = "profiles.json"

class AddProfileWidget(QWidget):
    profile_added = Signal(str)
    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self._parent = parent
        self.setWindowTitle("Add New Profile")
        self.resize(300, 200)

        layout = QGridLayout(self)

        self.profile_name_text = QLineEdit()
        self.profile_name_text.setPlaceholderText("Enter Profile Name")
        button = QPushButton("Select a File")
        button.clicked.connect(self.open_file_dialog)
        self.label = QLabel("No file selected", self)

        
        add_profile_button = QPushButton(text="Add Profile")
        add_profile_button.clicked.connect(self.save_profile)

        layout.addWidget(self.profile_name_text)
        layout.addWidget(self.label)
        layout.addWidget(button)
        layout.addWidget(add_profile_button)
        self.setLayout(layout)  # Fix layout assignment

    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select a FIle", "","Executable Files (*.exe);;All Files (*)" )

        if self.file_path:  # If a file was selected
            self.label.setText(f"Selected File:\n{self.file_path}")
            print(f"User selected: {self.file_path}")  # Debugging

    def save_profile(self):
        profile_name = self.profile_name_text.text().strip()
        
        if not profile_name:
            print("Error: Profile name is empty!")
            return

        if not self.file_path:
            print("Error: No file selected!")
            return
        
        profiles = ProfileDetection()
        all_profiles = profiles.load_profiles()

        if profile_name in all_profiles:
            print("Error, profile name exists")
            return 
        
            # Load existing profiles
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as file:
                    profiles = json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format! Creating a new profile file.")
                profiles = {}
        else:
            profiles = {}  # Create a new dictionary if file doesn't exist

        # Prevent overwriting an existing profile
        if profile_name in profiles:
            print(f"Error: Profile '{profile_name}' already exists!")
            return

        # Add new profile
        profiles[profile_name] = {
            "file_path": self.file_path,
            "notes": {
                "69": {"action": "run_command", "params": {"command": "start notepad"}},
                "70": {"action": "run_command", "params": {"command": "start chrome"}}
            },
            "cc": {"1": {"action": "none"}},
            "pw": {"1": {"action": "print_message", "params": {"message": "Pitch wheel moved!"}}}
        }

        # Save updated profiles back to JSON file
        with open(PROFILE_FILE, "w") as file:
            json.dump(profiles, file, indent=4)

        print(f"Profile '{profile_name}' saved successfully!")
        self.profile_added.emit(profile_name)  # Notify main window
        self.close()

