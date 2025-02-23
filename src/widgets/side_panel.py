from PySide6.QtCore import QPropertyAnimation, Qt, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGroupBox, QComboBox, QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy, QApplication
from src.models.midi import Midi
from src.models.enums import MidiActionType, MidiControlType
from src.models.profile_detection import ProfileDetection
from enum import Enum
import time

class SidePanel(QWidget):
    def __init__(self, parent: QMainWindow=None):
        super().__init__(parent)
        self._non_key_id = -1
        self._parent_widget = parent
        self._profile_detection = ProfileDetection()
        self._side_panel_widget_visibility = False 

        self.setFixedWidth(300)
        self.setStyleSheet("background-color: rgb(68, 75, 82);")
        self.setGeometry(self._parent_widget.width(), 0, self.minimumWidth(), self._parent_widget.height())

        # Connect the parent's resize event to force the side panel to update
        if self.parent_widget:
            self.parent_widget.installEventFilter(self)


        self.layout = QVBoxLayout(self)
        self._create_widget()
        self._create_animation()

    @property
    def parent_widget(self)->QMainWindow:
        return self._parent_widget
    
    @property
    def profile_detection(self)->ProfileDetection:
        return self._profile_detection
    
    @property
    def non_key_id(self)->str:
        return self._non_key_id
    
    @non_key_id.setter
    def non_key_id(self, value) -> None:
        self._non_key_id = value

    @property
    def side_panel_widget_visibility(self)->bool:
        return self._side_panel_widget_visibility    

    @property
    def animation(self)->QPropertyAnimation:
        return self._animation
    
    @property
    def profile_label_text(self)->QLabel:
        return self._profile_label_text
    
    @property
    def control_type_dropdown(self)->tuple:
        return self._control_type_dropdown
    
    @property
    def action_dropdown(self)->tuple:
        return self._action_dropdown
    
    @property
    def midi_channel_dropdown(self)->tuple:
        return self._midi_channel_dropdown
    
    @property
    def midi_note_edit_text(self)->QLineEdit:
        return self._midi_note_edit_text
    
    @property
    def midi_value(self)->QLineEdit:
        return self._midi_value

    @side_panel_widget_visibility.setter
    def side_panel_widget_visibility(self, isVisible):
        if isinstance(isVisible, bool):
            self._side_panel_widget_visibility = isVisible
        else:
            raise ValueError("The visibility provided must be a Boolean")
    
    def eventFilter(self, obj, event):
        """Intercepts parent resize events and forces update."""
        if obj == self.parent_widget and event.type() == QEvent.Resize:
            self.resize_panel()  # Call resize logic
        return super().eventFilter(obj, event)
    
    def resize_panel(self):
        """Recalculate position and height when parent resizes."""
        if self.side_panel_widget_visibility:
            self.setGeometry(
                self.parent_widget.width() - self.width(),  # Align to right edge
                0,
                self.width(),
                self.parent_widget.height()
            )
        else:
            self.setGeometry(
                self.parent_widget.width(),  # Move off-screen
                0,
                self.width(),
                self.parent_widget.height()
            )

        self.update()
    
    def _create_animation(self):        
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(250)  # Animation duration in milliseconds

    def _create_widget(self):
        _group_box = QGroupBox("", self)
        _group_box_layout = QVBoxLayout(_group_box)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self._add_close_button(_group_box_layout, _group_box)
        self._add_profile_widgets(_group_box_layout)
        self._add_control_widgets(_group_box_layout, _group_box)
        self._add_midi_widgets(_group_box_layout)
        
        max_width = self.lineup # to line up hte profile name with the combo boxes
        if max_width:
            self._profile_label_text.setFixedWidth(max_width)  
            self._profile_label_text.setStyleSheet("color: rgb(79, 227, 118); font-weight: bold;")
        
        _group_box_layout.addItem(spacer)
        self._add_save_reset_buttons(_group_box_layout, _group_box)
        _group_box_layout.setAlignment(Qt.AlignTop)  # This is the key line!



        self.layout.addWidget(_group_box)

    def _add_close_button(self, layout: QVBoxLayout, groupbox: QGroupBox):
        _close_button_widget = QPushButton("X", groupbox)
        _close_button_widget.setFixedSize(30, 30)
        _close_button_widget.clicked.connect(self.update_side_panel_visibility)
        layout.addWidget(_close_button_widget)

    def _add_profile_widgets(self, layout: QVBoxLayout):
        _profile_label = QLabel("Profile:")
        self._profile_label_text = QLabel(" ___N/A___")
        _profile_layout = QHBoxLayout()
        _profile_layout.addWidget(_profile_label)
        _profile_layout.addWidget(self._profile_label_text)    
        layout.addLayout(_profile_layout)

    def _add_control_widgets(self, layout: QVBoxLayout, groupbox: QGroupBox):
        self._action_dropdown = self._create_combobox("Action:", MidiActionType, groupbox)
        self._control_type_dropdown = self._create_combobox("Control Type:", MidiControlType, groupbox)
        self._midi_channel_dropdown = self._create_channels("Midi Channel:", 16, groupbox)
        layout.addLayout(self._action_dropdown[1])
        layout.addLayout(self._control_type_dropdown[1])
        layout.addLayout(self._midi_channel_dropdown[1])
        
        max_width = max(
            self._action_dropdown[0].sizeHint().width(),
            self._control_type_dropdown[0].sizeHint().width(),
            self._midi_channel_dropdown[0].sizeHint().width()
        )

        self.lineup = max_width

        for dropdown in [self._action_dropdown[0], self._control_type_dropdown[0], self._midi_channel_dropdown[0]]:
            dropdown.setFixedWidth(max_width)  # Set fixed width to the maximum width
            dropdown.setStyleSheet("background-color: rgb(68, 194, 101);")

    def _create_combobox(self, label_text, enum_type: Enum, groupbox: QGroupBox):
        dropdown = QComboBox(groupbox)
        dropdown.addItems([e.name for e in enum_type])
        dropdown.setStyleSheet("background-color: lightgray")
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        layout.addWidget(dropdown)
        return dropdown, layout
    
    def _create_channels(self, label_text, channel_amt=16, groupbox: QGroupBox = None):
        dropdown = QComboBox(groupbox)
        dropdown.addItems(map(str, range(channel_amt)))
        dropdown.setStyleSheet("background-color: lightgray")
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        layout.addWidget(dropdown)
        return dropdown, layout

    def _add_midi_widgets(self, layout: QVBoxLayout):
        self._midi_note_edit_text = QLineEdit(self)
        self._midi_note_edit_text.setPlaceholderText("Enter MIDI note here")

        self._midi_value = QLineEdit(self)
        self._midi_value.setPlaceholderText("Enter value here")

        layout.addWidget(self._midi_note_edit_text)
        layout.addWidget(self._midi_value)

    def _add_save_reset_buttons(self, layout: QVBoxLayout, groupbox: QGroupBox):
        _save_button_widget = QPushButton("Save", groupbox)
        _reset_button_widget = QPushButton("Reset", groupbox)

        # Connect buttons to their respective methods
        _save_button_widget.clicked.connect(self.save_macro)
        _reset_button_widget.clicked.connect(self.reset_macro)

        # Create layout for buttons
        save_reset_layout = QHBoxLayout()
        save_reset_layout.addWidget(_save_button_widget)
        save_reset_layout.addWidget(_reset_button_widget)
        save_reset_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(save_reset_layout)

    def update_side_panel_visibility(self):
        """Toggle the visibility of the side panel."""
        if self.animation.state() == QPropertyAnimation.Running:
            return  # Do nothing if animation is still running
        
        if self.side_panel_widget_visibility:
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
        self.side_panel_widget_visibility = not self.side_panel_widget_visibility
        self.raise_() 

    def save_macro(self):
        """Define the save macro logic here."""
        try:
            midi_item = Midi(time.time_ns(), self.profile_label_text.text(), MidiControlType[self.control_type_dropdown[0].currentText()], MidiActionType[self.action_dropdown[0].currentText()],
                                self.midi_channel_dropdown[0].currentText(), self.midi_note_edit_text.text(), self.midi_value.text())
            
            if MidiControlType[self.control_type_dropdown[0].currentText()] == MidiControlType.CONTROL_CHANGE:
                print("saving cc")
                self.profile_detection.save_profile(midi_item, self.non_key_id)
            else:
                print("saving keys")
                self.profile_detection.save_profile(midi_item)
        except Exception as e:
            print(f"Error occured during saving inside the Side Panel: {e}")

    def reset_macro(self):
        """Define the reset macro logic here."""
        pass
    