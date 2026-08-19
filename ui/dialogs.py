import os
import subprocess
from typing import List, Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QMessageBox, QFrame
)
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt, QProcess, QTimer
from models import Command, Category

class AddEditCommandDialog(QDialog):
    def __init__(self, categories: List[Category], command: Optional[Command] = None, current_category: str = "General", parent=None):
        super().__init__(parent)
        self.categories = categories
        self.command = command
        self.current_category = current_category
        self.setFixedWidth(520)
        self.setWindowTitle("Edit Command" if command else "Add New Command")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title Field
        lbl_title = QLabel("Command Title:")
        lbl_title.setObjectName("formLabel")
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("e.g. Restart Nginx Service")
        if self.command:
            self.input_title.setText(self.command.title)
        layout.addWidget(lbl_title)
        layout.addWidget(self.input_title)

        # Category Dropdown
        lbl_cat = QLabel("Category:")
        lbl_cat.setObjectName("formLabel")
        self.combo_cat = QComboBox()
        self.combo_cat.setEditable(True)
        
        default_index = 0
        for i, cat in enumerate(self.categories):
            self.combo_cat.addItem(cat.name)
            if self.command and self.command.category.lower() == cat.name.lower():
                default_index = i
            elif not self.command and self.current_category.lower() == cat.name.lower():
                default_index = i
                
        self.combo_cat.setCurrentIndex(default_index)
        layout.addWidget(lbl_cat)
        layout.addWidget(self.combo_cat)

        # Description Field
        lbl_desc = QLabel("Description (Optional):")
        lbl_desc.setObjectName("formLabel")
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Brief explanation of what the command does")
        if self.command:
            self.input_desc.setText(self.command.description)
        layout.addWidget(lbl_desc)
        layout.addWidget(self.input_desc)

        # Code Field
        lbl_code = QLabel("Command Snippet / Code:")
        lbl_code.setObjectName("formLabel")
        self.input_code = QTextEdit()
        self.input_code.setFont(QFont("Cascadia Code", 10))
        self.input_code.setPlaceholderText("e.g. sudo systemctl restart nginx")
        self.input_code.setFixedHeight(120)
        if self.command:
            self.input_code.setText(self.command.code)
        layout.addWidget(lbl_code)
        layout.addWidget(self.input_code)

        # Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save Command")
        btn_save.setObjectName("btnPrimary")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.on_save)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

    def on_save(self):
        title = self.input_title.text().strip()
        category = self.combo_cat.currentText().strip()
        code = self.input_code.toPlainText().strip()
        desc = self.input_desc.text().strip()

        if not title:
            QMessageBox.warning(self, "Validation Error", "Please provide a command title.")
            return
        if not category:
            QMessageBox.warning(self, "Validation Error", "Please specify a category.")
            return
        if not code:
            QMessageBox.warning(self, "Validation Error", "Please enter the command text.")
            return

        self.result_data = {
            "title": title,
            "category": category,
            "description": desc,
            "code": code
        }
        self.accept()

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(400)
        self.setWindowTitle("Add New Category")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        lbl = QLabel("Category Name:")
        lbl.setObjectName("formLabel")
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("e.g. Kubernetes, Ansible, Redis")
        layout.addWidget(lbl)
        layout.addWidget(self.input_name)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_create = QPushButton("Create Category")
        btn_create.setObjectName("btnPrimary")
        btn_create.setCursor(Qt.PointingHandCursor)
        btn_create.clicked.connect(self.on_create)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_create)

        layout.addLayout(btn_layout)

    def on_create(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Category name cannot be empty.")
            return
        self.category_name = name
        self.accept()

class DangerousCommandDialog(QDialog):
    def __init__(self, command: Command, parent=None):
        super().__init__(parent)
        self.command = command
        self.setFixedWidth(480)
        self.setWindowTitle("⚠️ Safety Confirmation")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        lbl_warn = QLabel("⚠️ High-Risk Command Confirmation")
        lbl_warn.setStyleSheet("font-size: 16px; font-weight: bold; color: #f38ba8;")
        layout.addWidget(lbl_warn)

        lbl_msg = QLabel(
            f"You are about to run <b>{self.command.title}</b>.<br>"
            "This command contains potential system-modifying operations (such as <code>sudo</code>, <code>rm</code>, or database modifications)."
        )
        lbl_msg.setWordWrap(True)
        layout.addWidget(lbl_msg)

        code_box = QTextEdit()
        code_box.setReadOnly(True)
        code_box.setText(self.command.code)
        code_box.setFixedHeight(80)
        code_box.setStyleSheet("background-color: #11111b; color: #f38ba8; font-family: monospace;")
        layout.addWidget(code_box)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("Yes, Execute Command")
        btn_confirm.setObjectName("btnDanger")
        btn_confirm.setCursor(Qt.PointingHandCursor)
        btn_confirm.clicked.connect(self.accept)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)

        layout.addLayout(btn_layout)

class TerminalOutputDialog(QDialog):
    def __init__(self, command: Command, parent=None):
        super().__init__(parent)
        self.command = command
        self.setWindowTitle(f"Terminal Output: {command.title}")
        self.resize(650, 420)
        self.process = QProcess(self)
        self.setup_ui()
        self.start_command()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Status Bar Header
        header_layout = QHBoxLayout()
        self.lbl_status = QLabel("▶ Executing command...")
        self.lbl_status.setStyleSheet("font-weight: bold; color: #89b4fa;")
        header_layout.addWidget(self.lbl_status)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Output console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Cascadia Code", 10))
        self.console.setStyleSheet("background-color: #11111b; color: #a6e3a1; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.console, 1)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_kill = QPushButton("Stop Execution")
        self.btn_kill.setObjectName("btnDanger")
        self.btn_kill.clicked.connect(self.process.kill)

        btn_close = QPushButton("Close Window")
        btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_kill)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def start_command(self):
        self.console.append(f"$ {self.command.code}\n")
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_ready_read)
        self.process.finished.connect(self.on_finished)

        # Run with bash shell
        self.process.start("bash", ["-c", self.command.code])

    def on_ready_read(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        self.console.insertPlainText(data)
        self.console.moveCursor(QTextCursor.End)

    def on_finished(self, exit_code, exit_status):
        self.btn_kill.setEnabled(False)
        if exit_code == 0:
            self.lbl_status.setText("✓ Execution Finished Successfully (Code 0)")
            self.lbl_status.setStyleSheet("font-weight: bold; color: #a6e3a1;")
        else:
            self.lbl_status.setText(f"❌ Process Exited with Code {exit_code}")
            self.lbl_status.setStyleSheet("font-weight: bold; color: #f38ba8;")
