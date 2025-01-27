from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from side_panel import SidePanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symphonic Translator")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout(main_widget)
        self.layout.setContentsMargins(0, 0 , 0, 0)
        
        self.side_panel = SidePanel(self)
        self.side_panel.setMinimumWidth(300)

        self.button = QPushButton("Click", self)
        self.button.clicked.connect(self.launch)

        self.layout.addWidget(self.side_panel)
        self.layout.addWidget(self.button)

    def launch(self):
        self.side_panel.toggle()

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
