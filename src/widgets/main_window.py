import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QHBoxLayout, QComboBox, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import QThread, Signal, QProcess
from side_panel import SidePanel
from knob_widget import KnobWidget
from fader_widget import FaderWidget
from piano_widget import PianoWidget
from add_profile_widget import AddProfileWidget
from src.profile_detection import ProfileDetection
import mido
import subprocess 
from src.MidiItem import Actions
from keyboard import send

class MidiListenerThread(QThread):
    midi_action_signal = Signal(dict)  # Signal to send the action dictionary back to the main thread

    def __init__(self, midi_device):
        super().__init__()
        self.midi_device = midi_device

    def run(self):
        # This will run in the background in a separate thread, so it doesn't block the main thread
        try:
            with mido.open_input(self.midi_device) as port:
                for msg in port:
                    # Run the profile detection, assuming it is non-blocking
                    active_profile = ProfileDetection().run_app()

                    # Match the message and execute the action
                    match msg.type:
                        case "note_on" if msg.velocity > 0:
                            print(active_profile)
                            action = active_profile["KEY"].get(str(msg.note))
                            print(action)
                            self.execute_action(action)
                           
                            if msg.note == 72:
                                break

                        case "control_change":
                            action = active_profile["cc"].get(str(msg.control))
                            self.execute_action(action)

                        case "pitchwheel":
                            action = active_profile["pw"].get('1')
                            self.execute_action(action)
                        
        except Exception as e:
            print(f"Error: {e}")

    def execute_action(self, action_conf):
        if not action_conf or "action" not in action_conf:
            print("No action configured")
            return

        action_type = action_conf["action"]
        parameters = action_conf.get("params", {})

        try:
            match int(action_type):
                case Actions.RUN_COMMAND.value:
                    command = parameters.get("RUN_COMMAND", "")
                    subprocess.run(command, shell=True) if command else print("No command provided for 'run_command'.")    

                case Actions.KEYBOARD_SHORTCUT.value:
                    keys = parameters.get("KEYBOARD_SHORTCUT", "")
                    print(keys)
                    send(keys) if keys else  print("No keys provided for 'keyboard_shortcut'.")
                 
                case Actions.RUN_SCRIPT.value:
                    script = parameters.get("RUN_SCRIPT", "")
                    subprocess.run(["python", script], shell=True) if script else print("No script provided for 'run_script'.")
                
                case "print_message":  # TODO get rid of this
                    message = parameters.get("PRINT_MESSAGE", "No message provided.")
                    print(message)

                case Actions.NONE.value:  # TODO get rid of this
                    print("No action assigned to this input")

                case _:
                    print(f"Unknown action type: {action_type}")

        except Exception as e:
            print(f"Error executing action: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symphonic Translator")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")        
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Exit")

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Select All")
        edit_menu.addAction("Remove All")
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Create the main layout for the central widget
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(5, 0, 5, 0)  # Remove margins for better alignment
        
       

        self.profile_dropdown = QComboBox(self)
        self.load_profiles()
        

        self.button = QPushButton("Add New Profile")
        self.button.clicked.connect(self.open_add_window)

        self.del_button = QPushButton("Delete Current Profile")
        self.del_button.clicked.connect(self.delete_profile)

        self.button_layout = QHBoxLayout(self)
        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.del_button)

        self.start_button = QPushButton("Start Scan")
        self.start_button.clicked.connect(self.run_detection)

        self.side_panel = SidePanel(self)
        self.side_panel.setMinimumWidth(300)

        # Add stretch to center the content
        self.layout.addStretch()  # Top stretch
        piano_layout = self.build_controller()
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.profile_dropdown)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(piano_layout)  # Add the actual piano layout
        self.layout.addStretch()  # Bottom stretch
        self.new_window = None  # Placeholder for the second window

    def run_detection(self):
        # When the user clicks "Start Scan," start the MIDI detection in a new thread
        self.midi_thread = MidiListenerThread("Minilab3 MIDI 0")
        self.midi_thread.midi_action_signal.connect(self.on_action_received)  # Connect to a method to handle actions
        self.midi_thread.start()

    def on_action_received(self, action):
        # Handle the action received from the MIDI thread
        print(f"Received action: {action}")
        # You can use this to trigger other actions or update the GUI

    def load_profiles(self):
        self.profile_dropdown.clear()
        profiles = ProfileDetection()
        print([i for i in profiles.load_profiles().keys()])
        self.profile_dropdown.addItems([i for i in profiles.load_profiles().keys()])

    def delete_profile(self):
        selected_profile = self.profile_dropdown.currentText()
        if not selected_profile:
            QMessageBox.warning(self, "No Selection", "Please select a profile to delete.")
            return

        # Confirm deletion
        reply = QMessageBox.question(self, "Delete Profile",
                                     f"Are you sure you want to delete '{selected_profile}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        PROFILE_FILE = "profiles.json"
        # Load JSON
        try:
            with open(PROFILE_FILE, "r") as file:
                profiles = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            profiles = {}

        # Remove profile if it exists
        if selected_profile in profiles:
            del profiles[selected_profile]

            # Save updated JSON
            with open(PROFILE_FILE, "w") as file:
                json.dump(profiles, file, indent=4)

            # Refresh the combo box
            self.load_profiles()
            QMessageBox.information(self, "Deleted", f"Profile '{selected_profile}' deleted successfully!")
        else:
            QMessageBox.warning(self, "Error", "Profile not found.")

    def open_add_window(self):
        if self.new_window is None or not self.new_window.isVisible():
            self.new_window = AddProfileWidget()  # No parent -> opens separately
            self.new_window.profile_added.connect(self.load_profiles)
            self.new_window.show()

    def build_controller(self):
        layout = QVBoxLayout()

        piano_widget = PianoWidget(self, self.side_panel)

        fader_layout = QGridLayout()
        for i, _ in enumerate(range(8)):
            fader = FaderWidget(parent=self, side_panel=self.side_panel, side_id=i)
            fader_layout.addWidget(fader, 0, i)

        knob_layout = QGridLayout()
        knob_layout.setHorizontalSpacing(5)
        knob_layout.setVerticalSpacing(10)
        knob_id = 0
        for row in range(2): 
            for col in range(4): 
                knob = KnobWidget(parent = self, side_panel=self.side_panel, knob_id=knob_id)
                knob.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)  # Allow knobs to shrink
                knob_layout.addWidget(knob, row, col)
                knob_id+=1 

        control_layout = QHBoxLayout() 
        control_layout.addLayout(fader_layout) 
        control_layout.addLayout(knob_layout) 

        layout.addLayout(control_layout)
        layout.addWidget(piano_widget)

        return layout
    
    def closeEvent(self, event):
        if self.new_window:
            self.new_window.close()
        event.accept()
        return super().closeEvent(event)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


"""
TODO
connect the midi script, seems to have some blocking thing happening
"""