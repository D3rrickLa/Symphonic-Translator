from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QSizePolicy
)
from src.widgets.base_widget import BaseWidget
from src.models.enums import MidiControlType

class PianoWidget(BaseWidget):
    def __init__(self, parent: QMainWindow, octaves = 3):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumSize(600, 200)
        
        self._parent = parent
        self._piano_octaves = octaves
        self._key_width = 55
        self._white_keys = []
        self._black_keys = []
        self._white_key_names = ["C", "D", "E", "F", "G", "A", "B"]

        self._side_panel = super().get_side_panel()

        
        # Make sure parent exists and has a layout before adding widgets
        if self._parent and hasattr(self._parent, "_layout"):
            self._parent.layout.addWidget(self._side_panel)  # Correct way to access layout

        self.create_widget()

    @property
    def key_width(self):
        return self._key_width
    
    @property
    def piano_octaves(self):
        return self._piano_octaves
    
    @property
    def side_panel(self):
        return self._side_panel
    
    @property
    def white_keys(self):
        return self._white_keys
    
    @property
    def black_keys(self):
        return self._black_keys

    @property
    def white_key_names(self):
        return self._white_key_names

    def toggle_side_panel(self, key_index):
        """Toggle the visibility of the side panel."""
        piano_key_data = super().get_profile_detection()
        _data = piano_key_data.get_profile_by_key(key_index, f"{self._parent.profile_dropdown.currentText()}", str(MidiControlType.KEY.name))
        
        if _data is None:
            self.set_key_info(key_index)
            self.side_panel.action_dropdown[0].setCurrentIndex(0)
            self.side_panel.midi_value.setText("") 
        else:
            self.set_key_info(key_index)

            action = _data.get("action", {})
            self.side_panel.action_dropdown[0].setCurrentIndex(int(action))

            params = _data.get("params", {})
            if params:
                _, value = next(iter(params.items()))
                self.side_panel.midi_value.setText(value)

        self.side_panel.update_side_panel_visibility() 

    def set_key_info(self, key_index):
        self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
        self.side_panel.control_type_dropdown[0].setCurrentIndex(0)
        self.side_panel.midi_note_edit_text.setText(f"{key_index}")  

    def create_widget(self):
        """Create and add widgets to the layout."""
        black_key_width = self.key_width * 0.6
        black_key_height = self.height() * 0.6 
        black_key_positions = [0, 1, 3, 4, 5]
        white_numbers = [0, 2, 4, 5, 7, 9, 11]
        black_numbers = [1, 3, 6, 8, 10]
  

        for octave in range(self.piano_octaves):
            base_midi = octave * 12  # MIDI base for the current octave
    
             # Create white keys
            for i, note_offset in enumerate(white_numbers):
                midi_value = base_midi + note_offset
                key_name = self.white_key_names[i] + str(octave)  # C4, D4, etc.
                self.white_keys.append(self.create_piano_key(self.key_width, self.height(), midi_value, "white", key_name))

            # Create black keys
            for key_idx, note_offset in enumerate(black_numbers):
                midi_value = base_midi + note_offset
                key_name = self.white_key_names[black_key_positions[key_idx]] + "#" + str(octave)
                btn = self.create_piano_key(black_key_width, black_key_height, midi_value, "black", key_name)
                self.black_keys.append(btn)
    
    def create_piano_key(self, width, height, idx, color, key_name):
        piano_key_btn = QPushButton(self)
        piano_key_btn.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
        piano_key_btn.setFixedSize(width, height)
        piano_key_btn.clicked.connect(lambda _, idx = idx: self.toggle_side_panel(idx))
        return piano_key_btn
    
    def update_widget(self, value):
        """Update widget properties or data."""
        pass


    def resize_piano(self):
        """Ensure the piano scales correctly on resizing."""
        key_height = self.height()

        white_keys_num = 7
        black_key_width = self.key_width * 0.6
        black_key_height = key_height * 0.6
        black_key_positions = self.get_black_key_positions(self.piano_octaves)


        total_piano_width = white_keys_num * self.piano_octaves  * self.key_width
        widget_width = self.width()

        hori_offset = (widget_width - total_piano_width) / 2

        # Resize and reposition white keys
        for i, white_key in enumerate(self.white_keys):
            white_key.setFixedSize(self.key_width, key_height)
            white_key.move(hori_offset + i * self.key_width, 0)

        # Resize and reposition black keys
   
        for i, pos in enumerate(black_key_positions):
            black_key = self.black_keys[i]
            black_key.setFixedSize(black_key_width, black_key_height)
            x_offset = hori_offset + (pos + 1) * self.key_width - (black_key_width / 2)
            black_key.move(x_offset, 0)

    def get_black_key_positions(self, octaves: int):
        white_keys_num = 7
        base_black_key_positions = [0, 1, 3, 4, 5]  # Base positions for one octave
        black_key_positions = []
        
        # For each octave, extend the base positions by the correct offset
        for octave in range(octaves):
            offset = octave * white_keys_num  # 7 positions per octave (one octave has 5 black keys)
            for pos in base_black_key_positions:
                black_key_positions.append(pos + offset)
        
        return black_key_positions
    
    def resizeEvent(self, event):
        """Handle resizing to maintain static key positions."""
        self.resize_piano()
        super().resizeEvent(event)

    def showEvent(self, event):
        """Ensure proper layout when the widget is shown."""
        self.resize_piano()
        super().showEvent(event)