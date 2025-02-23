from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from abc import ABC, abstractmethod
from src.widgets.side_panel import SidePanel
from src.models.profile_detection import ProfileDetection

class BaseWidgetMeta(type(QWidget), type(ABC)):
    pass

class BaseWidget(ABC, QWidget, metaclass=BaseWidgetMeta):
    _side_panel_instance = None
    _profile_detection = None

    def __init__(self, parent=None):
        super().__init__(parent)
        
        if BaseWidget._side_panel_instance is None:
            BaseWidget._side_panel_instance = SidePanel(parent)
            BaseWidget._side_panel_instance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        if BaseWidget._profile_detection is None:
            BaseWidget._profile_detection = ProfileDetection()
        

    @abstractmethod
    def toggle_side_panel(self):
        """Toggle the visibility of the side panel."""
        pass

    @abstractmethod
    def create_widget(self):
        """Create and add widgets to the layout."""
        pass

    @abstractmethod
    def update_widget(self, value):
        """Update widget properties or data."""
        pass
    
    @classmethod
    def get_side_panel(cls):
        """Return the shared side panel instance."""
        return cls._side_panel_instance

    @classmethod
    def get_profile_detection(cls):
        """Return the shared profile detection instance."""
        return cls._profile_detection