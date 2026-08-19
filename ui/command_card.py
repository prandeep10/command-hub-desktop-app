from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
)
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtCore import Qt, QTimer, Signal
from models import Command

DANGEROUS_KEYWORDS = [
    "rm -rf", "sudo rm", "dd if=", "mkfs", "drop database", "drop table",
    "truncate ", "killall", "shutdown", "reboot", "chmod 777 -R /"
]

class CommandCardWidget(QFrame):
    copy_triggered = Signal(Command)
    run_triggered = Signal(Command)
    favorite_toggled = Signal(Command)
    edit_triggered = Signal(Command)
    delete_triggered = Signal(Command)

    def __init__(self, command: Command, parent=None):
        super().__init__(parent)
        self.command = command
        self.setObjectName("commandCard")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Header Row: Title + Category Badge + Favorite Star
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.lbl_title = QLabel(self.command.title)
        self.lbl_title.setObjectName("cardTitle")

        self.lbl_category = QLabel(self.command.category)
        self.lbl_category.setObjectName("cardCategory")

        # Favorite Star Button
        self.btn_fav = QPushButton("★" if self.command.is_favorite else "☆")
        self.btn_fav.setFixedSize(32, 28)
        self.btn_fav.setCursor(Qt.PointingHandCursor)
        if self.command.is_favorite:
            self.btn_fav.setStyleSheet("color: #f9e2af; font-size: 15px; font-weight: bold;")
        else:
            self.btn_fav.setStyleSheet("color: #a6adc8; font-size: 15px;")
        self.btn_fav.clicked.connect(self.on_toggle_favorite)

        header_layout.addWidget(self.lbl_title, 1)
        header_layout.addWidget(self.lbl_category)
        header_layout.addWidget(self.btn_fav)

        layout.addLayout(header_layout)

        # Description Label (if present)
        if self.command.description:
            self.lbl_desc = QLabel(self.command.description)
            self.lbl_desc.setObjectName("cardDescription")
            self.lbl_desc.setWordWrap(True)
            layout.addWidget(self.lbl_desc)

        # Code Container Box
        self.code_edit = QTextEdit()
        self.code_edit.setObjectName("codeBox")
        self.code_edit.setReadOnly(True)
        self.code_edit.setText(self.command.code)

        # Adjust height according to line count
        lines_count = len(self.command.code.splitlines())
        calc_height = max(52, min(220, lines_count * 22 + 20))
        self.code_edit.setFixedHeight(calc_height)

        layout.addWidget(self.code_edit)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)

        self.btn_copy = QPushButton("📋 Copy")
        self.btn_copy.setObjectName("btnCopy")
        self.btn_copy.setCursor(Qt.PointingHandCursor)
        self.btn_copy.clicked.connect(self.on_copy_clicked)

        self.btn_run = QPushButton("▶ Run")
        self.btn_run.setObjectName("btnRun")
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.clicked.connect(lambda: self.run_triggered.emit(self.command))

        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.clicked.connect(lambda: self.edit_triggered.emit(self.command))

        self.btn_delete = QPushButton("🗑️ Delete")
        self.btn_delete.setObjectName("btnDanger")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(lambda: self.delete_triggered.emit(self.command))

        actions_layout.addWidget(self.btn_copy)
        actions_layout.addWidget(self.btn_run)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_edit)
        actions_layout.addWidget(self.btn_delete)

        layout.addLayout(actions_layout)

    def on_copy_clicked(self):
        # Copy command text to system clipboard
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.command.code)

        # Visual feedback on copy button
        original_text = "📋 Copy"
        self.btn_copy.setText("✓ Copied!")
        self.btn_copy.setStyleSheet("background-color: #a6e3a1; color: #11111b; font-weight: bold;")
        
        QTimer.singleShot(1500, lambda: self.reset_copy_button(original_text))
        self.copy_triggered.emit(self.command)

    def reset_copy_button(self, original_text):
        self.btn_copy.setText(original_text)
        self.btn_copy.setStyleSheet("")

    def on_toggle_favorite(self):
        self.command.is_favorite = not self.command.is_favorite
        self.btn_fav.setText("★" if self.command.is_favorite else "☆")
        if self.command.is_favorite:
            self.btn_fav.setStyleSheet("color: #f9e2af; font-size: 15px; font-weight: bold;")
        else:
            self.btn_fav.setStyleSheet("color: #a6adc8; font-size: 15px;")
        self.favorite_toggled.emit(self.command)
