from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox, QDialog
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv
import os

class ToDoList(QMainWindow):
    """
    A class representing the main window for managing a to-do list.

    This window provides functionality to add, remove, and edit tasks in the 
    to-do list. Users can update the status of each task and save the list 
    to a CSV file. It interacts with a `TaskEditor` dialog to modify task 
    details.

    Inherits from:
        QMainWindow: The base class for the to-do list window.
    """
    
    def __init__(self):
        """
        Initializes the ToDoList window and sets up the user interface.

        Sets up the input fields, buttons, table, and connections for adding, 
        removing, editing tasks, and saving the list to a CSV file. It also 
        loads the existing tasks from a CSV file.
        """
        super().__init__()
        self.__initialize_widgets()
        
        self.remove_button.clicked.connect(self.__on_remove_task)
        self.add_button.clicked.connect(self.__on_add_task)
        self.save_button.clicked.connect(self.__save_to_csv)
        self.task_table.cellClicked.connect(self.__on_edit_task)

        self.__load_data('data/todo.csv')


    def __initialize_widgets(self):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("To-Do List")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.add_button = QPushButton("Add Task", self)
        self.remove_button = QPushButton("Remove Task", self)

        self.save_button = QPushButton("Save to CSV", self)

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])

        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.task_table)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()  
    def __on_add_task(self):
        """
        Handles the event when the "Add Task" button is clicked.

        Retrieves the task name and selected status from the input fields,
        adds the new task to the table, and updates the status label. If no 
        task name is provided, an error message is displayed.
        """
        task_name = self.task_input.text()
        task_status = self.status_combo.currentText()
        
        if task_name:  
            row_count = self.task_table.rowCount()
            self.task_table.insertRow(row_count)
            
            task_item = QTableWidgetItem(task_name)
            status_item = QTableWidgetItem(task_status)
            
            self.task_table.setItem(row_count, 0, task_item)  
            self.task_table.setItem(row_count, 1, status_item) 
            
            self.status_label.setText(f"Added task: {task_name}")
            self.task_input.clear()  
        else:
            self.status_label.setText("Please enter a task and select its status.")

    @Slot(int)
    def __on_remove_task(self):
        """
        Handles the event when the "Remove Task" button is clicked.

        Removes the currently selected task from the table and updates the 
        status label. If no task is selected, an error message is displayed.
        """
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            self.task_table.removeRow(selected_row)
            self.status_label.setText("Task removed.")
        else:
            self.status_label.setText("Please select a task to remove.")

    @Slot(int, int)
    def __on_edit_task(self, row: int, column: int):
        """
        Handles the event when a task row is clicked for editing.

        Opens the `TaskEditor` dialog, allowing the user to modify the task's 
        status. The dialog is populated with the current task and its status.
        Once the status is updated, the task table is updated accordingly.
        
        Args:
            row (int): The row index of the clicked task in the table.
            column (int): The column index of the clicked cell (task or status).
        """
        if row >= 0:
            current_task = self.task_table.item(row, 0).text()
            current_status = self.task_table.item(row, 1).text()
            
            task_editor = TaskEditor(row, current_task, current_status)
            task_editor.status_updated.connect(self.__update_task_status) 
            task_editor.exec()

    @Slot(int, str)
    def __update_task_status(self, row: int, new_status: str):
        """
        Updates the status of a task in the table after editing.

        This method is triggered by the `TaskEditor` dialog once the user 
        updates the status. It updates the task's status in the table and 
        updates the status label with the new status.

        Args:
            row (int): The row index of the task to be updated.
            new_status (str): The new status of the task.
        """
        self.task_table.item(row, 1).setText(new_status)  
        self.status_label.setText(f"Task status updated to: {new_status}")

    def __load_data(self, file_path: str):
        """
        Loads task data from a CSV file and populates the task table.

        The method reads the CSV file, parses each row, and adds the data 
        to the task table using the `__add_table_row` method.
        
        Args:
            file_path (str): The path to the CSV file containing the task data.
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  
            for row in reader:
                self.__add_table_row(row)

    def __add_table_row(self, row_data):
        """
        Adds a new row to the task table with the provided task data.

        Args:
            row_data (list): A list containing task name and status.
        """
        row_count = self.task_table.rowCount()
        
        self.task_table.insertRow(row_count)
        
        task_item = QTableWidgetItem(row_data[0]) 
        status_item = QTableWidgetItem(row_data[1])  
        
        self.task_table.setItem(row_count, 0, task_item) 
        self.task_table.setItem(row_count, 1, status_item) 

    def __save_to_csv(self):
        """
        Saves the current task data from the table to a CSV file.

        The task names and statuses from the table are written to a CSV file 
        (`output/todos.csv`). If the directory does not exist, it is created. 
        A success message is displayed on the status label once the file is saved.
        """
        file_path = 'output/todos.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Status"]) 
            
            for row in range(self.task_table.rowCount()):
                task_item = self.task_table.item(row, 0)
                status_item = self.task_table.item(row, 1)

                if task_item and status_item:
                    task_text = task_item.text()
                    status_text = status_item.text()
                    writer.writerow([task_text, status_text])  
            
        self.status_label.setText("Tasks saved to CSV successfully.")
