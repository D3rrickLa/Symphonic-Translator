from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QFileDialog,
    QLabel
)
class AddProfileWidget(QWidget):
    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self._parent = parent
        self.setWindowTitle("Add New Profile")
        self.resize(300, 200)

        layout = QGridLayout(self)

        profile_name_text = QLineEdit("Enter Profile Name")
        button = QPushButton("Select a File")
        button.clicked.connect(self.open_file_dialog)
        self.label = QLabel("No file selected", self)

        
        add_profile_button = QPushButton(text="Add Profile")

        layout.addWidget(profile_name_text)
        layout.addWidget(self.label)
        layout.addWidget(button)
        layout.addWidget(add_profile_button)
        self.setLayout(layout)  # Fix layout assignment

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a FIle", "","Executable Files (*.exe);;All Files (*)" )

        if file_path:  # If a file was selected
            self.label.setText(f"Selected File:\n{file_path}")
            print(f"User selected: {file_path}")  # Debugging