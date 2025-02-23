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
from src.models.profile_detection import ProfileDetection
import json
import os

PROFILE_FILE = "profiles.json"

class ProfileWidget(QWidget):
    add_profile = Signal(str)

    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self.setWindowTitle("Add New Profile")
        self.resize(300, 200)
        
        self._parent = parent
        self.create_widget()

    @property
    def profile_file_name(self):
        return self._profile_name_text

    @property
    def file_select_label(self):
        return self._file_select_label

    def create_widget(self):
        _layout = QGridLayout(self)        
        
        self._profile_name_text = QLineEdit()
        self._profile_name_text.setPlaceholderText("Enter Profile Name")
        button = QPushButton("Select a File")
        button.clicked.connect(self.open_file_dialog)
        self._file_select_label = QLabel("No file selected", self)

        
        add_profile_button = QPushButton(text="Add Profile")
        add_profile_button.clicked.connect(self.save_profile)

        _layout.addWidget(self._profile_name_text)
        _layout.addWidget(self._file_select_label)
        _layout.addWidget(button)
        _layout.addWidget(add_profile_button)
        self.setLayout(_layout)  # Fix layout assignment   


    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "","Executable Files (*.exe);;All Files (*)" )
        if self.file_path:  # If a file was selected
            self.file_select_label.setText(f"Selected File: {self.file_path}")
    
    def save_profile(self):
        profile_name = self.profile_file_name.text().strip()

        if not profile_name:
            print("ERROR: Profile name is empty")
            return 
        
        if not self.file_path:
            print("Error: No file selected!")
            return 
        
        profiles = ProfileDetection()
        all_profiles = profiles.get_loaded_profiles()

        if profile_name in all_profiles:
            print("Error: profile name exists")
            return 
        
        try:
            if os.path.exists(PROFILE_FILE):
                with open(PROFILE_FILE, "r") as file:
                    profiles = json.load(file) 
                    
            # Extract the executable name from the file path
            executable_name = os.path.basename(self.file_path)  # Get the full file name with extension
            executable_name_without_extension = os.path.splitext(executable_name)[0]  # Remove the extension
            # Add new profile
            profiles[profile_name] = {
                "file_path": self.file_path,
                "program_window_name" : executable_name_without_extension,
                "KEY": {
                    "69" : {"action": "1", "params": {"command": "start notepad"}},
                    "70" : {"action": "1", "params": {"command": "start chrome"}}
                },
                "CONTROL_CHANGE": {
                    "69" : {"action": "1", "params": {"command": "start notepad"}},
                    "70" : {"action": "1", "params": {"command": "start chrome"}}
                },
                "PITCHWEEL": {"1": {"action": "print_message", "params": {"message": "Pitch wheel moved!"}}}
            }

            # Save updated profiles back to JSON file
            with open(PROFILE_FILE, "w") as file:
                json.dump(profiles, file, indent=4)

            print(f"Profile '{profile_name}' saved successfully!")
            self.add_profile.emit(profile_name)  # Notify main window
            self.close()   

        except json.JSONDecodeError:
            print("Error: Invalid JSON format! Creating a new profile file.")
            return
