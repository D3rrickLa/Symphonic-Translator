from src.widgets.base_widget import BaseWidget
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from src.models.enums import MidiControlType
import math

class KnobWidget(BaseWidget):
    def __init__(self, parent=None, knob_id = None):
        super().__init__(parent)
        self.setMinimumSize(80, 80)    
        self._parent = parent

        self._min_value = 0
        self._max_value = 127
        self._knob_id = knob_id
        self._side_panel = super().get_side_panel()
        self._value = (self.max_value + self.min_value) // 2  # Default to midpoint value
        self._angle = 0  # Starting angle for the knob
        self._is_dragging = False
    
    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value
    
    @property
    def knob_id(self):
        return self._knob_id

    @property
    def side_panel(self):
        return self._side_panel

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._min_value <= new_value <= self._max_value:
            self._value = new_value
        else:
            raise ValueError(f"Value must be between {self._min_value} and {self._max_value}.")

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle  # You can add validation if necessary
    @property
    def parent_widget(self):
        return self._parent
    @property
    def is_dragging(self):
        return self._is_dragging

    @is_dragging.setter
    def is_dragging(self, dragging):
        self._is_dragging = dragging

    def toggle_side_panel(self):
        """Toggle the visibility of the side panel."""
        knob_data = super().get_profile_detection()
        _data = knob_data.get_profile_by_key(self.knob_id, f"{self.parent_widget.profile_dropdown.currentText()}", str(MidiControlType.CONTROL_CHANGE.name))
        if _data is None:
            self.set_knob_info()
            self.side_panel.action_dropdown[0].setCurrentIndex(0)
            self.side_panel.midi_note_edit_text.setText(f"{self.knob_id}") 
            self.side_panel.midi_value.setText("") 
        else:
            self.set_knob_info()            
            action = _data.get("action", {})
            self.side_panel.action_dropdown[0].setCurrentIndex(int(action))
            
            params = _data.get("params", {})

            # Get cc_control_id (default to empty string if missing)
            cc_control_id = str(params.get("cc_control_id", ""))

            # Get the first non-cc_control_id parameter dynamically
            filtered_params = {k: v for k, v in params.items() if k != "cc_control_id"}
            first_param_value = str(next(iter(filtered_params.values()), ""))

            # Set values to the UI
            self.side_panel.midi_note_edit_text.setText(cc_control_id)  # Set cc_control_id
            self.side_panel.midi_value.setText(first_param_value) 

        self.side_panel.update_side_panel_visibility() 

    def set_knob_info(self):
        self.side_panel.non_key_id = self.knob_id
        self.side_panel.control_type_dropdown[0].setCurrentIndex(1)            
        self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}") # Set first non-cc_control_id value
    
    def create_widget(self):
        """Create and add widgets to the layout."""
        pass

    
    def update_widget(self, value):
        """Update widget properties or data."""
        pass
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_in_knob_area(event.pos()):
                self.toggle_side_panel()


    def is_in_knob_area(self, pos):
        """Check if the mouse click is inside the knob area."""
        center = QPoint(self.width() // 2, self.height() // 2)
        distance = math.sqrt((pos.x() - center.x()) ** 2 + (pos.y() - center.y()) ** 2)
        knob_radius = min(self.width(), self.height()) // 2
        return distance <= knob_radius
    
    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Define the size and the center of the knob
        knob_radius=  min(self.width(), self.height()) // 2- 10
        center = QPoint(self.width() // 2, self.height() // 2)

        # Draw the knob circle
        painter.setPen(QPen(QColor(100, 100, 100), 3))
        painter.setBrush(QBrush(QColor(150, 150, 150)))  # Light gray
        painter.drawEllipse(center, knob_radius, knob_radius)
        
        # Calculate the angle for the value indicator
        angle_range = 270  # Range of rotation (e.g., -135° to +135°)
        start_angle = -135  # Start angle (leftmost position)
        normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.angle = start_angle + normalized_value * angle_range
        
        painter.save()

        # Draw the value indicator line
        painter.setPen(QPen(QColor(50, 50, 50), 4))
        indicator_length = knob_radius - 5
        angle_radians = math.radians(-90)
        # angle_radians = math.radians(self.angle)
        end_x = center.x() + math.cos(angle_radians) * indicator_length
        end_y = center.y() + math.sin(angle_radians) * indicator_length
        painter.drawLine(center, QPoint(end_x, end_y))

        # Restore painter to prevent affecting subsequent drawings
        painter.restore()
        
        # Draw the value text in the center
        painter.setPen(Qt.black)
        painter.setFont(self.font())
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, f"{self.value}")
        text_rect.translate(0, 10)
        painter.drawText(text_rect, Qt.AlignCenter, f"{self.value}")