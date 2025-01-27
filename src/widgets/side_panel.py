from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGroupBox, QComboBox, QHBoxLayout, QLineEdit
from src.MidiItem import Actions, MidiControlType, MidiElement
class SidePanel(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setFixedWidth(200)  # Optional: Set a fixed width for the side panel
        self.setStyleSheet("background-color: rgb(68, 75, 82);")
        self.setGeometry(parent.width(), 0, self.minimumWidth(), parent.height())

        self.parent_widget = parent
        self.layout = QVBoxLayout(self)

        group_box = QGroupBox("", self)
        group_box_layout = QVBoxLayout(group_box)

        close_widget_button = QPushButton("X", group_box)
        close_widget_button.setFixedSize(30,30)
        close_widget_button.clicked.connect(self.close)
        
        save_widget_button = QPushButton("Save", group_box)
        save_widget_button.clicked.connect(self.save)
        
        reset_widget_button = QPushButton("Reset", group_box)
        reset_widget_button.clicked.connect(self.reset)

        # Add the buttons to a horizontal layout that will stretch them
        save_layout = QHBoxLayout()
        save_layout.addWidget(save_widget_button)
        save_layout.addWidget(reset_widget_button)
        save_layout.setAlignment(Qt.AlignCenter)  # Center the button

        self.action_dropdown = QComboBox(group_box)
        self.action_dropdown.addItems([e.name for e in Actions])
        self.action_dropdown.setStyleSheet("background-color: green")

        self.control_type_dropdown = QComboBox(group_box)
        self.control_type_dropdown.addItems([e.name for e in MidiControlType])
        self.control_type_dropdown.setStyleSheet("background-color: blue")

        self.midi_channel_dropdown = QComboBox(group_box)
        self.midi_channel_dropdown.addItems([str(i) for i in range(16)])

        # Action Dropdown with Label
        action_layout = QHBoxLayout()
        action_label = QLabel("Action:")
        action_layout.addWidget(action_label)
        action_layout.addWidget(self.action_dropdown)

        # Control Type Dropdown with Label
        control_type_layout = QHBoxLayout()
        control_type_label = QLabel("Control Type:")
        control_type_layout.addWidget(control_type_label)
        control_type_layout.addWidget(self.control_type_dropdown)

        # MIDI Channel Dropdown with Label
        midi_channel_layout = QHBoxLayout()
        midi_channel_label = QLabel("MIDI Channel:")
        midi_channel_layout.addWidget(midi_channel_label)
        midi_channel_layout.addWidget(self.midi_channel_dropdown)

        # Fix size for all combo boxes
        fixed_width = 150  # Choose a suitable width
        self.action_dropdown.setFixedWidth(fixed_width)
        self.control_type_dropdown.setFixedWidth(fixed_width)
        self.midi_channel_dropdown.setFixedWidth(fixed_width)

        self.midi_note_text = QLineEdit(group_box)
        self.midi_note_text.setPlaceholderText("Enter midi note here")
        
        self.midi_value = QLineEdit(group_box)
        self.midi_value.setPlaceholderText("Enter value here")


        group_box_layout.addWidget(close_widget_button)
        group_box_layout.addLayout(control_type_layout)
        group_box_layout.addLayout(action_layout)
        group_box_layout.addLayout(midi_channel_layout)
        group_box_layout.addWidget(self.midi_note_text)
        group_box_layout.addWidget(self.midi_value)
        group_box_layout.addLayout(save_layout)

        # Add the group box to the main layout
        self.layout.addWidget(group_box)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)  # Animation duration in milliseconds
        self.side_widget_visible = False 

    def close(self):
        self.toggle()

    def save(self):
        element = MidiElement(MidiControlType[self.control_type_dropdown.currentText()], Actions[self.action_dropdown.currentText()],
                              self.midi_channel_dropdown.currentText(), self.midi_note_text.text(), self.midi_value.text())
        print(f"midi element: {element.describe()}")

    def reset(self):
        self.control_type_dropdown.setCurrentIndex(0)
        self.action_dropdown.setCurrentIndex(0)
        self.midi_channel_dropdown.setCurrentIndex(0) 
        self.midi_note_text.clear()                  
        self.midi_value.clear()       
        self.save()               
        

    def toggle(self):        
        if self.animation.state() == QPropertyAnimation.Running:
            return  # Do nothing if animation is still running
        
        if self.side_widget_visible:  # <-- Use the correct attribute name
            # Slide out
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(
                self.geometry().translated(self.width(), 0)
            )
        else:
            # Slide in
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(
                self.
                geometry().translated(-self.width(), 0)
            )
   
        self.animation.start()
        self.side_widget_visible = not self.side_widget_visible
        self.raise_()
    
    def resizeEvent(self, event):
        # Adjust the height and reposition the side widget based on visibility
        if self.side_widget_visible:
            self.setGeometry(
                self.parent_widget.width() - self.width(),  # Align to the right edge
                0,
                self.width(),
                self.parent_widget.height()
            )
        else:
            self.setGeometry(
                self.parent_widget.width(),  # Off-screen
                0,
                self.width(),
                self.parent_widget.height()
            )

        super().resizeEvent(event)
