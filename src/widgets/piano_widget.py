from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout
)
class PianoWidget(QWidget):
    def __init__(self, parent: QMainWindow = None, octaves = 3):
        super().__init__(parent)
        self.setMinimumSize(600, 200)
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.layout = layout
        self.piano_octaves = octaves
        self.key_width = 55

        
        
