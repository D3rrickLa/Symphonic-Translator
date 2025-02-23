import json
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QHBoxLayout, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QSpacerItem, QLabel
from PySide6.QtCore import QThread, Signal, QProcess
from src.models.midi_detection import MidiDetection
from src.widgets.piano_widget import PianoWidget
from src.widgets.fader_widget import FaderWidget
from src.widgets.knob_widget import KnobWidget
from src.widgets.profile_widget import ProfileWidget
from src.models.profile_detection import ProfileDetection
import mido
import subprocess 
from src.models.enums import MidiActionType
from keyboard import send

class MidiListenerThread(QThread):
    def __init__(self, midi_device):
        super().__init__()
        self._midi_device = midi_device
        self.running = True  # Control flag

    def stop(self):
        self.running = False  # Set flag to stop the thread
        time.sleep(0.1)


    def run(self):
        self.run_scan()

    @property
    def midi_device(self):
        return self._midi_device
    
    def run_scan(self):
        try:
            available_devices = mido.get_input_names()
            if self.midi_device not in available_devices:
                print(f"MIDI device '{self.midi_device}' not available.")
                return
            
            with mido.open_input(self.midi_device) as port:
                while self.running:
                    try:
                        for msg in port:
                            if not self.running:  # Check running flag at the beginning of the loop
                                break  # Immediately break if stopping

                            active_profile = ProfileDetection().run_app()

                            # Match the message and execute the action
                            match msg.type:
                                case "note_on" if msg.velocity > 0:
                                    action = active_profile["KEY"].get(str(msg.note))
                                    print(action)
                                    self.execute_action(action)

                                    if msg.note == 72:
                                        break

                                case "cc":
                                    action = active_profile["CONTROL_CHANGE"].get(str(msg.control))
                                    self.execute_action(action)

                                case "pw":
                                    action = active_profile["PITCH_WHEEL"].get('1')
                                    self.execute_action(action)
                    except Exception as e:
                        print(f"Error processing MIDI message: {e}")
                        break  # Exit the inner loop on error

        except Exception as e:
            print(f"Error in run_scan method: {e}")

    def execute_action(self, action_conf):
        if not action_conf or "action" not in action_conf:
            # print("No action configured")
            return

        action_type = action_conf["action"]
        parameters = action_conf.get("params", {})

        try:
            match int(action_type):
                case MidiActionType.RUN_COMMAND.value:
                    command = parameters.get("RUN_COMMAND", "")
                    subprocess.run(command, shell=True) if command else print("No command provided for 'run_command'.")    

                case MidiActionType.KEYBOARD_SHORTCUT.value:
                    keys = parameters.get("KEYBOARD_SHORTCUT", "")
                    send(keys) if keys else  print("No keys provided for 'keyboard_shortcut'.")
                 
                case MidiActionType.RUN_SCRIPT.value:
                    script = parameters.get("RUN_SCRIPT", "")
                    subprocess.run(["python", script], shell=True) if script else print("No script provided for 'run_script'.")
                
                case "print_message":  # TODO get rid of this
                    message = parameters.get("PRINT_MESSAGE", "No message provided.")
                    print(message)

                case MidiActionType.NONE.value:  # TODO get rid of this
                    print("No action assigned to this input")

                case _:
                    print(f"Unknown action type: {action_type}")

        except Exception as e:
            print(f"Error executing action: {e}")

PROFILE_LOCATION = "profiles.json"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Symphonic Translator")
        self.setGeometry(100, 100, 1200, 800)

        self._profile_detection = ProfileDetection()
        self._midi_detection = MidiDetection()
        self._is_second_window = None
        self._midi_device = None
        self.create_widget()

    @property 
    def midi_device(self):
        return self._midi_device
    
    @midi_device.setter 
    def midi_device(self, value):
        self._midi_device = value

    @property
    def midi_detection(self):
        return self._midi_detection
    @property
    def profile_dropdown(self):
        return self._profile_dropdown

    @property
    def profile_detection(self):
        return self._profile_detection

    @property
    def is_second_window(self):
        return self._is_second_window
    
    @is_second_window.setter
    def is_second_window(self, value):
        self._is_second_window = value

    def create_widget(self):
        """Create and add widgets to the layout."""
        _main_widget = QWidget()
        self.setCentralWidget(_main_widget)
        self.create_menu_bar()

        _layout = QVBoxLayout(_main_widget)
        _layout.setSpacing(0)
        _layout.setContentsMargins(5, 0 , 5, 0)

        self.create_midi_device_dropdown(_layout)
        fader_layout = self.create_faders()
        knob_layout = self.create_knobs() 

        control_layout = QHBoxLayout() 
        control_layout.addLayout(fader_layout) 
        control_layout.addLayout(knob_layout) 
        _layout.addLayout(control_layout)

   
        _piano = PianoWidget(self)
        _layout.addWidget(_piano)
        self.create_profile_button_group(_layout)
        self.layout = _layout

    def create_profile_dropdown(self, _layout):
        self._profile_dropdown = QComboBox()
        self.load_profiles()
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        _layout.addItem(spacer)
        _layout.addWidget(self._profile_dropdown)

    def create_profile_button_group(self, layout: QVBoxLayout):
        master_button_layout = QVBoxLayout()
        master_button_layout.setSpacing(0)  # Remove extra spacing
        master_button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout = QHBoxLayout()
        

        self.start_button = QPushButton("Start", self)
        add_profile_button = QPushButton("Add New Profile", self)
        del_button = QPushButton("Delete Current Profile", self)
        
        self.start_button.clicked.connect(self.run_application)
        add_profile_button.clicked.connect(self.open_add_window)       
        del_button.clicked.connect(self.delete_profile)

        # Add buttons to the horizontal layout

        button_layout.addWidget(add_profile_button)
        button_layout.addWidget(del_button)
        master_button_layout.addWidget(self.start_button)
        master_button_layout.addLayout(button_layout)
        # Add the horizontal button layout to the provided vertical layout
        self.create_profile_dropdown(master_button_layout)

        layout.addLayout(master_button_layout)

    def create_midi_device_dropdown(self, layout: QVBoxLayout):
        _hlayout = QHBoxLayout()
        midi_text_label = QLabel("Selece Midi Device")
        self.midi_devices_dropdown = QComboBox()
        self.load_midi_device_list()
        _hlayout.addWidget(midi_text_label)
        _hlayout.addWidget(self.midi_devices_dropdown)

        layout.addLayout(_hlayout)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")        
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Exit")

    def create_faders(self):
        fader_layout = QGridLayout()
        for i, _ in enumerate(range(8)):
            fader = FaderWidget(parent=self, slider_id=i)
            fader_layout.addWidget(fader, 0, i)
        return fader_layout

    def create_knobs(self):
        knob_layout = QGridLayout()
        knob_layout.setHorizontalSpacing(5)
        knob_layout.setVerticalSpacing(10)
        knob_id = 0
        for row in range(2): 
            for col in range(4): 
                knob = KnobWidget(parent = self, knob_id=knob_id)
                knob.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)  # Allow knobs to shrink
                knob_layout.addWidget(knob, row, col)
                knob_id+=1
        return knob_layout

    def load_midi_device_list(self):
        self.midi_devices_dropdown.clear()
        self.midi_devices_dropdown.addItems([i for i in self.midi_detection.list_midi_devices()])

    def load_profiles(self):
        global PROFILE_LOCATION
        self.profile_dropdown.clear()
        profiles = self.profile_detection
        self.profile_dropdown.addItems([i for i in profiles.get_loaded_profiles()])
    
    def open_add_window(self):
        print("working")
        if  self.is_second_window is None or not self.is_second_window.isVisible():
            print("inside")
            self.is_second_window = ProfileWidget()  # No parent -> opens separately
            self.is_second_window.add_profile.connect(self.load_profiles)
            self.is_second_window.show()
            self.is_second_window.raise_()  # Bring to the front

    def delete_profile(self):
        selected_profile = self.profile_dropdown.currentText()
        if not selected_profile:
            QMessageBox.warning(self, "No Selection", "Please select a profile to delete.")
            return

        # Confirm deletion
        reply = QMessageBox.question(self, "Delete Profile",f"Are you sure you want to delete '{selected_profile}'?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # Load JSON
        try:
            with open(PROFILE_LOCATION, "r") as file:
                profiles = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            profiles = {}

        # Remove profile if it exists
        if selected_profile in profiles:
            del profiles[selected_profile]

            # Save updated JSON
            with open(PROFILE_LOCATION, "w") as file:
                json.dump(profiles, file, indent=4)

            # Refresh the combo box
            self.load_profiles()
            QMessageBox.information(self, "Deleted", f"Profile '{selected_profile}' deleted successfully!")
        else:
            QMessageBox.warning(self, "Error", "Profile not found.")

    def closeEvent(self, event):
        if self.is_second_window:
            self.is_second_window.close()
        event.accept()
        return super().closeEvent(event)

    def run_application(self):
        if hasattr(self, "midi_thread") and self.midi_thread.isRunning():
            print("Stopping app")
            self.midi_thread.stop()  # Tell thread to stop
            self.midi_thread.quit()
            self.midi_thread.wait(1)
            self.start_button.setText("Start")  # Update button text
            
        else:
            print("Starting app")
            print(f"selected {self.midi_devices_dropdown.currentText()}")
            # self.midi_thread = MidiListenerThread("Minilab3 MIDI 0")
            self.midi_thread = MidiListenerThread(self.midi_devices_dropdown.currentText())
            self.midi_thread.start()  # Calls run(), which calls run_scan()
            self.start_button.setText("Stop")  # Update button text
    
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()