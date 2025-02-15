import json
import mido
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox
from PySide6.QtCore import QThread, Signal
# Load JSON Profile
def load_profile():
    with open("profiles.json", "r") as file:
        return json.load(file)

class MidiListenerThread(QThread):
    midi_signal = Signal(str)

    def __init__(self, midi_device, active_profile):
        super().__init__()
        self.midi_device = midi_device
        self.active_profile = active_profile
        self.running = True

    def run(self):
        try:
            with mido.open_input(self.midi_device) as port:
                print(f"Listening on {self.midi_device}...")

                for msg in port:
                    if not self.running:
                        break

                    self.midi_signal.emit(str(msg))

                    if self.active_profile:
                        match msg.type:
                            case "note_on" if msg.velocity > 0:
                                action = self.active_profile.get("KEY", {}).get(str(msg.note))
                                self.execute_action(action)
                    else:
                        print(f"MIDI Message Received: {msg}")

        except Exception as e:
            print(f"MIDI Listening Error: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class MidiListener(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MIDI Listener")
        self.setGeometry(100, 100, 400, 200)
        
        self.profile = load_profile()
        self.active_profile = None
        self.midi_thread = None
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select Profile and MIDI Device")
        layout.addWidget(self.label)
        
        self.profile_selector = QComboBox()
        self.profile_selector.addItems(self.profile.keys())
        self.profile_selector.currentTextChanged.connect(self.set_active_profile)
        layout.addWidget(self.profile_selector)
        
        self.midi_selector = QComboBox()
        self.midi_selector.addItems(mido.get_input_names())
        layout.addWidget(self.midi_selector)
        
        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.start_listening)
        layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_active_profile(self, profile_name):
        self.active_profile = self.profile[profile_name]

    def start_listening(self):
        selected_device = self.midi_selector.currentText()
        if not selected_device:
            print("No MIDI device selected.")
            return

        if self.midi_thread and self.midi_thread.isRunning():
            self.midi_thread.stop()
        
        print("Starting MIDI listener...")
        self.midi_thread = MidiListenerThread(selected_device, self.active_profile)
        self.midi_thread.midi_signal.connect(self.update_gui)
        self.midi_thread.start()

    def update_gui(self, message):
        self.label.setText(f"Received: {message}")

if __name__ == "__main__":
    app = QApplication([])
    window = MidiListener()
    window.show()
    app.exec()