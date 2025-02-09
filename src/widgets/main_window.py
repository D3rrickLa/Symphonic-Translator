from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QHBoxLayout, QComboBox, QPushButton
from side_panel import SidePanel
from knob_widget import KnobWidget
from fader_widget import FaderWidget
from piano_widget import PianoWidget
from add_profile_widget import AddProfileWidget
from src.profile_dection import ProfileDetection

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
        
        profiles = ProfileDetection()

        self.profile_dropdown = QComboBox(self)
        self.profile_dropdown.addItems([i for i in profiles.run_app().keys()])

        self.button = QPushButton("Add New Profile")
        self.button.clicked.connect(self.open_add_window)

        self.side_panel = SidePanel(self)
        self.side_panel.setMinimumWidth(300)

        # Add stretch to center the content
        self.layout.addStretch()  # Top stretch
        piano_layout = self.build_controller()
        self.layout.addWidget(self.profile_dropdown)
        self.layout.addWidget(self.button)
        self.layout.addLayout(piano_layout)  # Add the actual piano layout
        self.layout.addStretch()  # Bottom stretch
        self.new_window = None  # Placeholder for the second window

    def open_add_window(self):
        if self.new_window is None or not self.new_window.isVisible():
            self.new_window = AddProfileWidget()  # No parent -> opens separately
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
need a way to save the fader and knob cc channel info
"""