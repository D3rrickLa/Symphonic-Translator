from PySide6.QtWidgets import QSizePolicy, QSlider, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from src.widgets.base_widget import BaseWidget
from src.models.enums import MidiControlType

class FaderWidget(BaseWidget):
    def __init__(self, parent = None, slider_id: int = None):
        super().__init__(parent)    
        self.setFixedSize(50, 200)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._parent = parent 
        self._slider_id = slider_id
        self._side_panel = super().get_side_panel()
        self._layout = QVBoxLayout(self)

         # Make sure parent exists and has a layout before adding widgets
        if self._parent and hasattr(self._parent, "_layout"):
            self._parent.layout.addWidget(self._side_panel)  # Correct way to access layout
        
        self.create_widget()

    @property
    def slider_id(self) -> int:
        return self._slider_id
    @property
    def layout(self):
        return self._layout
    @property
    def side_panel(self):
        return self._side_panel
    @property
    def parent_widget(self):
        return self._parent
    @property
    def slider(self):
        return self._slider
    @property
    def value_label(self):
        return self._value_label

    def toggle_side_panel(self):
        """Toggle the visibility of the side panel."""
        fader_data = super().get_profile_detection()
        _data = fader_data.get_profile_by_key(self.slider_id, f"{self.parent_widget.profile_dropdown.currentText()}", str(MidiControlType.CONTROL_CHANGE.name))

        if _data is None:
            self.set_fader_info()
            self.side_panel.action_dropdown[0].setCurrentIndex(0)
            self.side_panel.midi_note_edit_text.setText(f"{self.slider_id}")
            self.side_panel.midi_value.setText("") 
        else:
            self.set_fader_info
            action = _data.get("action", {})
            self.side_panel.action_dropdown[0].setCurrentIndex(int(action))
            
            params = _data.get("params", {})                    

            cc_control_id = str(params.get("cc_control_id", ""))
            filtered_params = {k: v for k, v in params.items() if k != "cc_control_id"}
            first_param_value = str(next(iter(filtered_params.values()), ""))

            # Set values to the UI
            self.side_panel.midi_note_edit_text.setText(cc_control_id)  # Set cc_control_id
            self.side_panel.midi_value.setText(first_param_value)  # Set first non-cc_control_id value
        
        self.side_panel.update_side_panel_visibility() 

    def set_fader_info(self):
        self.side_panel.non_key_id = self.slider_id
        self.side_panel.control_type_dropdown[0].setCurrentIndex(1)            
        self.side_panel.profile_label_text.setText(f"{self.parent_widget.profile_dropdown.currentText()}")

    def create_widget(self):
        """Create and add widgets to the layout."""
        self._slider = QSlider(Qt.Vertical, self)
        self._slider.setMinimum(0)
        self._slider.setMaximum(127)
        self._slider.setValue(64)
        self._slider.setTickPosition(QSlider.TicksBelow)
        self._slider.setTickInterval(16)
        self._slider.valueChanged.connect(self.update_widget)
        self._slider.sliderPressed.connect(self.toggle_side_panel)

        self._value_label = QLabel("64", self)
        self._value_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self._slider)
        self.layout.addWidget(self._value_label)


    def update_widget(self, value):
        """Update widget properties or data."""
        self.value_label.setText(str(value))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_side_panel()