from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt, Signal
from models import Category

class SidebarWidget(QWidget):
    category_selected = Signal(str)  # Category name or "All" or "Favorites"
    search_changed = Signal(str)
    add_command_clicked = Signal()
    add_category_clicked = Signal()
    theme_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarWidget")
        self.setFixedWidth(260)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(12)

        # Header Title
        title_label = QLabel("⚡ Command Hub")
        title_label.setObjectName("sidebarHeader")
        layout.addWidget(title_label)

        # Search Box with Ctrl+K shortcut tip
        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBox")
        self.search_box.setPlaceholderText("🔍 Search... (Ctrl + K)")
        self.search_box.textChanged.connect(lambda text: self.search_changed.emit(text))
        layout.addWidget(self.search_box)

        # Category List
        self.cat_list = QListWidget()
        self.cat_list.setObjectName("categoryList")
        self.cat_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.cat_list, 1)

        # Action Buttons
        self.btn_add_cmd = QPushButton("➕ Add Command")
        self.btn_add_cmd.setObjectName("btnPrimary")
        self.btn_add_cmd.setCursor(Qt.PointingHandCursor)
        self.btn_add_cmd.clicked.connect(lambda: self.add_command_clicked.emit())
        layout.addWidget(self.btn_add_cmd)

        self.btn_add_cat = QPushButton("📂 Add Category")
        self.btn_add_cat.setCursor(Qt.PointingHandCursor)
        self.btn_add_cat.clicked.connect(lambda: self.add_category_clicked.emit())
        layout.addWidget(self.btn_add_cat)

        self.btn_theme = QPushButton("🌙 Switch Theme")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.clicked.connect(lambda: self.theme_toggled.emit())
        layout.addWidget(self.btn_theme)

    def populate_categories(self, categories: List[Category], total_count: int, fav_count: int, active_category: str = "All"):
        self.cat_list.clear()

        # All Commands item
        all_item = QListWidgetItem(f"📁 All Commands ({total_count})")
        all_item.setData(Qt.UserRole, "All")
        self.cat_list.addItem(all_item)

        # Favorites item
        fav_item = QListWidgetItem(f"★ Favorites ({fav_count})")
        fav_item.setData(Qt.UserRole, "Favorites")
        self.cat_list.addItem(fav_item)

        # Category items
        selected_widget_item = all_item
        for cat in categories:
            item_text = f"📄 {cat.name} ({cat.count})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, cat.name)
            self.cat_list.addItem(item)
            if cat.name == active_category:
                selected_widget_item = item

        if active_category == "Favorites":
            selected_widget_item = fav_item
        elif active_category == "All":
            selected_widget_item = all_item

        self.cat_list.setCurrentItem(selected_widget_item)

    def on_item_clicked(self, item: QListWidgetItem):
        cat_name = item.data(Qt.UserRole)
        if cat_name:
            self.category_selected.emit(cat_name)

    def focus_search(self):
        self.search_box.setFocus()
        self.search_box.selectAll()
