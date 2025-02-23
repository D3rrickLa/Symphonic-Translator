import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QHBoxLayout, QComboBox, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import QThread, Signal, QProcess
from src.widgets.side_panel import SidePanel
from src.widgets.piano_widget import PianoWidget
from src.widgets.fader_widget import FaderWidget
from src.widgets.knob_widget import KnobWidget
from src.models.profile_detection import ProfileDetection
import mido
import subprocess 
from src.models.enums import MidiActionType
from keyboard import send

PROFILE_LOCATION = "profiles.json"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Symphonic Translator")
        self.setGeometry(100, 100, 1200, 800)

        self._profile_detection = ProfileDetection()

        self.create_widget()

    @property
    def profile_dropdown(self):
        return self._profile_dropdown

    @property
    def profile_detection(self):
        return self._profile_detection

    def toggle_side_panel(self):
        """Toggle the visibility of the side panel."""
        pass

    def create_widget(self):
        """Create and add widgets to the layout."""
        _main_widget = QWidget()
        self.setCentralWidget(_main_widget)
        self.create_menu_bar()

        _layout = QVBoxLayout(_main_widget)
        _layout.setContentsMargins(5, 0 , 5, 0)

        self._profile_dropdown = QComboBox()
        self.load_profiles()

        fader_layout = self.create_faders()
        knob_layout = self.create_knobs() 

        control_layout = QHBoxLayout() 
        control_layout.addLayout(fader_layout) 
        control_layout.addLayout(knob_layout) 
        _layout.addLayout(control_layout)

        _piano = PianoWidget(self)
        _layout.addWidget(_piano)
        self.layout = _layout

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")        
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Exit")

        # edit_menu = menu_bar.addMenu("Edit")
        # edit_menu.addAction("Select All")
        # edit_menu.addAction("Remove All")

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

    def load_profiles(self):
        global PROFILE_LOCATION
        self.profile_dropdown.clear()
        profiles = self.profile_detection
        self.profile_dropdown.addItems([i for i in profiles.get_loaded_profiles()])

    def update_widget(self, value):
        """Update widget properties or data."""
        pass

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()