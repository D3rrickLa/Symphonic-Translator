from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt
from src.profile_detection import ProfileDetection
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
        fader_data = ProfileDetection()
        _data = fader_data.load_key_profile(self.slider_id, f"{self._parent.profile_dropdown.currentText()}", "FADER")
        if _data is None:
            self.side_panel.set_non_key(self.slider_id)
            self.side_panel.control_type_dropdown.setCurrentIndex(1)            
            self.side_panel.action_dropdown.setCurrentIndex(0)
            self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
            self.side_panel.midi_note_text.setText(f"{self.slider_id}")
            self.side_panel.midi_value.setText("") 
        else:
            self.side_panel.set_non_key(self.slider_id)
            self.side_panel.control_type_dropdown.setCurrentIndex(1)
            self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
            
            action = _data.get("action", {})
            self.side_panel.action_dropdown.setCurrentIndex(int(action))
            
            params = _data.get("params", {})                    

            cc_control_id = str(params.get("cc_control_id", ""))
            filtered_params = {k: v for k, v in params.items() if k != "cc_control_id"}
            first_param_value = str(next(iter(filtered_params.values()), ""))

            # Set values to the UI
            self.side_panel.midi_note_text.setText(cc_control_id)  # Set cc_control_id
            self.side_panel.midi_value.setText(first_param_value)  # Set first non-cc_control_id value

        self.side_panel.toggle()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_side_panel()