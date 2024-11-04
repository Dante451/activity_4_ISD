from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox, QDialog
from PySide6.QtCore import Signal, Slot

class TaskEditor(QDialog):
    status_updated = Signal(int, str)  

    def __init__(self, row: int, current_task: str, current_status: str):
        super().__init__()
        
        self.row = row  
        self.setWindowTitle("Edit Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])
        self.status_combo.setCurrentText(current_status)  
        
        self.save_button = QPushButton("Save Status", self)
        self.cancel_button = QPushButton("Cancel", self)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Editing Task: {current_task}")) 
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)

        self.save_button.clicked.connect(self.on_save_status) 
        self.cancel_button.clicked.connect(self.reject)

    def __initialize_widgets(self, row: int, status: str):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("Edit Task Status")

        self.row = row

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.save_button = QPushButton("Save", self)

        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

    @Slot()
    def on_save_status(self):
        new_status = self.status_combo.currentText()
        self.status_updated.emit(self.row, new_status)  
        self.accept() 

