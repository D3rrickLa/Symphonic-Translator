from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
import math
from side_panel import SidePanel

class KnobWidget(QWidget):
    valueChanged = Signal(int)

    def __init__(self, min_value=0, max_value=100, parent=None, side_panel: SidePanel=None, knob_id = None):
        super().__init__(parent)
        self.setMinimumSize(80, 80)    
        self._parent = parent

        self.min_value = min_value
        self.max_value = max_value
        self.value = (self.max_value + self.min_value) // 2  # Default to midpoint value
        self.angle = 0  # Starting angle for the knob
        self.is_dragging = False
        
        self.setCursor(Qt.PointingHandCursor)  # Set cursor to hand for better interaction

        self.knob_id = knob_id
        self.side_panel = side_panel
        parent.layout.addWidget(self.side_panel)

    def paintEvent(self, event):
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
    
    def is_in_knob_area(self, pos):
        """Check if the mouse click is inside the knob area."""
        center = QPoint(self.width() // 2, self.height() // 2)
        distance = math.sqrt((pos.x() - center.x()) ** 2 + (pos.y() - center.y()) ** 2)
        knob_radius = min(self.width(), self.height()) // 2
        return distance <= knob_radius
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_in_knob_area(event.pos()):
                self.side_panel.enable_non_key()
                self.side_panel.control_type_dropdown.setCurrentIndex(2)
                self.side_panel.profile_label_text.setText(f"{self._parent.profile_dropdown.currentText()}")
                self.side_panel.midi_note_text.setText(f"{self.knob_id} Amongus") 
                self.side_panel.toggle()   