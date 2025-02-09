from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout
)
from side_panel import SidePanel

class PianoWidget(QWidget):
    def __init__(self, parent: QMainWindow = None, side_panel: SidePanel = None, octaves = 3):
        super().__init__(parent)
        self._parent = parent
        self.setMinimumSize(600, 200)
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.layout = layout
        self.piano_octaves = octaves
        self.key_width = 55        
        
        self.create_piano(octaves=self.piano_octaves)
        self.resize_piano()

        self.side_panel = side_panel  # Passing the main window (parent)
        parent.layout.addWidget(self.side_panel)


    def create_piano(self, octaves: int = 1):

        white_keys_num = 7
        black_key_width = self.key_width * 0.6
        black_key_height = self.height() * 0.6 
        black_key_positions = [0, 1, 3, 4, 5]
        white_numbers = [0, 2, 4, 5, 7, 9, 11]
        black_numbers = [1, 3, 6, 8, 10]

        self.white_key_names = ["C", "D", "E", "F", "G", "A", "B"]
        self.white_keys = []
        self.black_keys = []

    
        for octave in range(octaves):
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
        piano_key_btn.clicked.connect(lambda _, idx = idx: self.key_pressed(key_name, idx))
        return piano_key_btn
    
    def key_pressed(self, key_name, key_index):
        self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
        self.side_panel.control_type_dropdown.setCurrentIndex(0)
        self.side_panel.midi_note_text.setText(f"{key_index}")
        self.side_panel.toggle()   

    def resizeEvent(self, event):
        """Handle resizing to maintain static key positions."""
        self.resize_piano()
        super().resizeEvent(event)

    def showEvent(self, event):
        """Ensure proper layout when the widget is shown."""
        self.resize_piano()
        super().showEvent(event)

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