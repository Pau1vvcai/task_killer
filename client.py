import sys, os, json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import uuid

class ManageClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manage")
        self.resize(600, 600)

        self.date_str = datetime.now().strftime("%Y-%m-%d")
        self.log_file = f"task_log_{self.date_str}.json"
        
        self.tasks = {"active": [], "completed": [], "trash": []}
        
        self.initUI()
        self.load_tasks()

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        font_layout = QHBoxLayout()
        self.font_label = QLabel("Font Size:")
        self.font_spinbox = QSpinBox()
        self.font_spinbox.setRange(12, 20)
        self.font_spinbox.setValue(12)
        self.font_spinbox.valueChanged.connect(self.change_font_size)
        font_layout.addWidget(self.font_label)
        font_layout.addWidget(self.font_spinbox)
        font_layout.addStretch()
        mainLayout.addLayout(font_layout)

        self.tabs = QTabWidget()
        mainLayout.addWidget(self.tabs)

        # ===== Active Tab =====
        self.tab_active = QWidget()
        active_layout = QVBoxLayout(self.tab_active)
        self.list_active = QListWidget()
        active_layout.addWidget(self.list_active)
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a new task...")
        self.add_btn = QPushButton("Add Task")
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.add_btn)
        active_layout.addLayout(input_layout)
        
        btn_active_layout = QHBoxLayout()
        self.btn_mark_completed = QPushButton("Mark Completed")
        self.btn_delete_error = QPushButton("Delete (Error)")
        btn_active_layout.addWidget(self.btn_mark_completed)
        btn_active_layout.addWidget(self.btn_delete_error)
        active_layout.addLayout(btn_active_layout)
        self.tabs.addTab(self.tab_active, "Active")

        # ===== Completed Tab =====
        self.tab_completed = QWidget()
        completed_layout = QVBoxLayout(self.tab_completed)
        self.list_completed = QListWidget()
        completed_layout.addWidget(self.list_completed)
        
        self.btn_delete_completed = QPushButton("Delete Completed")
        self.btn_keep_active_from_completed = QPushButton("Keep It Active")
        completed_layout.addWidget(self.btn_delete_completed)
        completed_layout.addWidget(self.btn_keep_active_from_completed)
        self.tabs.addTab(self.tab_completed, "Completed")
        self.btn_keep_active_from_completed.clicked.connect(lambda: self.keep_it_active("completed"))

        # ===== Trash Tab =====
        self.tab_trash = QWidget()
        trash_layout = QVBoxLayout(self.tab_trash)
        self.list_trash = QListWidget()
        trash_layout.addWidget(self.list_trash)
        
        self.btn_permanent_delete = QPushButton("Permanently Delete")
        self.btn_keep_active_from_trash = QPushButton("Keep It Active")
        trash_layout.addWidget(self.btn_permanent_delete)
        trash_layout.addWidget(self.btn_keep_active_from_trash)
        self.tabs.addTab(self.tab_trash, "Trash")


        self.add_btn.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)
        self.btn_mark_completed.clicked.connect(self.mark_completed)
        self.btn_delete_error.clicked.connect(self.delete_error)
        self.btn_delete_completed.clicked.connect(self.delete_completed)
        self.btn_permanent_delete.clicked.connect(self.permanent_delete)
        self.btn_keep_active_from_trash.clicked.connect(lambda: self.keep_it_active("trash"))

        self.change_font_size(self.font_spinbox.value())

    def change_font_size(self, size):
        font = QFont()
        font.setPointSize(size)
        self.list_active.setFont(font)
        self.input.setFont(font)
        self.add_btn.setFont(font)
        self.btn_mark_completed.setFont(font)
        self.btn_delete_error.setFont(font)
        self.list_completed.setFont(font)
        self.btn_delete_completed.setFont(font)
        self.list_trash.setFont(font)
        self.btn_permanent_delete.setFont(font)
        self.btn_keep_active_from_trash.setFont(font)
        self.btn_keep_active_from_completed.setFont(font)
        self.font_label.setFont(font)
        self.font_spinbox.setFont(font)

    def load_tasks(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print("Error loading tasks:", e)
                self.tasks = {"active": [], "completed": [], "trash": []}
        else:
            self.tasks = {"active": [], "completed": [], "trash": []}
        self.refresh_ui()

    def save_tasks(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error saving tasks:", e)

    def refresh_ui(self):
        self.list_active.clear()
        for task in self.tasks["active"]:
            item = QListWidgetItem(task["text"])
            item.setData(Qt.UserRole, task)
            self.list_active.addItem(item)

        self.list_completed.clear()
        for task in self.tasks["completed"]:
            item = QListWidgetItem(task["text"])
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
            item.setData(Qt.UserRole, task)
            self.list_completed.addItem(item)

        self.list_trash.clear()
        for task in self.tasks["trash"]:
            item = QListWidgetItem(task["text"])
            item.setData(Qt.UserRole, task)
            self.list_trash.addItem(item)

    def add_task(self):
        text = self.input.text().strip()
        if text:
            task = {
                "text": text,
                "status": "active",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "id" : str(uuid.uuid4())
            }
            self.tasks["active"].append(task)
            self.save_tasks()
            self.refresh_ui()
            self.input.clear()

    def mark_completed(self):
        selected = self.list_active.selectedItems()
        for item in selected:
            task_item = item.data(Qt.UserRole)
            task_id = task_item.get("id")
            for t in self.tasks["active"]:
                if t.get("id") == task_id:
                    t["status"] = "completed"
                    self.tasks["active"].remove(t)
                    self.tasks["completed"].append(t)
                    break  
        self.save_tasks()
        self.refresh_ui()

    def delete_error(self):
        selected = self.list_active.selectedItems()
        for item in selected:
            task_item = item.data(Qt.UserRole)
            task_id = task_item.get("id")
            for t in self.tasks["active"]:
                if t.get("id") == task_id:
                    t["status"] = "Trash"
                    self.tasks["active"].remove(t)
                    self.tasks["trash"].append(t)
                    break  
        self.save_tasks()
        self.refresh_ui()

    def delete_completed(self):
        selected = self.list_completed.selectedItems()
        for item in selected:
            task_item = item.data(Qt.UserRole)
            task_id = task_item.get("id")
            for t in self.tasks["completed"]:
                if t.get("id") == task_id:
                    self.tasks["completed"].remove(t)
                    self.tasks["trash"].append(t)
                    break 
        self.save_tasks()
        self.refresh_ui()

    def permanent_delete(self):
        selected = self.list_trash.selectedItems()
        for item in selected:
            task_item = item.data(Qt.UserRole)
            task_id = task_item.get("id")
            for t in self.tasks["trash"]:
                if t.get("id") == task_id:
                    self.tasks["trash"].remove(t)
                    break
        self.save_tasks()
        self.refresh_ui()

    def keep_it_active(self, source):
        if source == "trash":
            list_widget = self.list_trash
        elif source == "completed":
            list_widget = self.list_completed
        else:
            return
        selected = selected = list_widget.selectedItems()
        for item in selected:
            task_item = item.data(Qt.UserRole)
            task_id = task_item.get("id")
            for t in self.tasks[source]:
                if t.get("id") == task_id:
                    self.tasks[source].remove(t)
                    self.tasks["active"].append(t)
                    break  
        self.save_tasks()
        self.refresh_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManageClient()
    window.show()
    sys.exit(app.exec_())
