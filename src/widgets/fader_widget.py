from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt

from side_panel import SidePanel

class FaderWidget(QWidget):
    def __init__(self, parent=None, side_panel: SidePanel = None, side_id = None):
        super().__init__(parent)
        self.setFixedSize(50, 200)
        self._parent = parent

        self.layout = QVBoxLayout(self)
        slider = QSlider(Qt.Vertical, self)
        slider.setMinimum(0)
        slider.setMaximum(127)
        slider.setValue(64)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(16)

        self.value_label = QLabel("64", self)
        self.value_label.setAlignment(Qt.AlignCenter)

        self.slider_id = side_id

        self.side_panel = side_panel
        parent.layout.addWidget(self.side_panel)

        self.layout.addWidget(slider)
        self.layout.addWidget(self.value_label)

        slider.valueChanged.connect(self.update_label)
        slider.sliderPressed.connect(self.toggle_side_panel)
    
    def update_label(self, value):
        """Update the value displayed below the fader."""
        self.value_label.setText(str(value))

    def toggle_side_panel(self):
        """Toggle the side panel."""
        self.side_panel.set_non_key(self.slider_id)
        self.side_panel.control_type_dropdown.setCurrentIndex(1)
        self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
        self.side_panel.midi_note_text.setText(f"{self.slider_id}")
        self.side_panel.toggle()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_side_panel()