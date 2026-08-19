from pathlib import Path
from typing import List, Set
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea,
    QMessageBox, QSystemTrayIcon, QMenu, QFrame
)
from PySide6.QtGui import QIcon, QKeySequence, QAction, QShortcut
from PySide6.QtCore import Qt

from models import Command, Category
from parser import CommandParser
from ui.styles import Themes
from ui.sidebar import SidebarWidget
from ui.command_card import CommandCardWidget, DANGEROUS_KEYWORDS
from ui.dialogs import (
    AddEditCommandDialog, AddCategoryDialog, DangerousCommandDialog, TerminalOutputDialog
)

class MainWindow(QMainWindow):
    def __init__(self, base_dir: Path, icon_path: Path):
        super().__init__()
        self.base_dir = base_dir
        self.commands_dir = base_dir / "commands"
        self.fav_file = self.commands_dir / "favorites.json"
        self.icon_path = icon_path

        self.commands_dir.mkdir(parents=True, exist_ok=True)

        self.current_theme = "dark"
        self.active_category = "All"
        self.search_query = ""
        self.favorites: Set[str] = CommandParser.load_favorites(self.fav_file)

        self.all_commands: List[Command] = []
        self.categories: List[Category] = []

        self.setWindowTitle("Command Hub - Personal Command Library")
        self.resize(1080, 680)

        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        self.reload_data()

    def setup_ui(self):
        # Apply dark theme by default
        self.setStyleSheet(Themes.DARK)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.category_selected.connect(self.on_category_selected)
        self.sidebar.search_changed.connect(self.on_search_changed)
        self.sidebar.add_command_clicked.connect(self.on_add_command)
        self.sidebar.add_category_clicked.connect(self.on_add_category)
        self.sidebar.theme_toggled.connect(self.toggle_theme)
        main_layout.addWidget(self.sidebar)

        # Right Content Area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(24, 20, 24, 16)
        content_layout.setSpacing(16)

        # Content Header Bar
        header_bar = QHBoxLayout()
        self.lbl_content_title = QLabel("All Commands")
        self.lbl_content_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #89b4fa;")

        self.lbl_count_info = QLabel("")
        self.lbl_count_info.setStyleSheet("color: #a6adc8; font-size: 13px;")

        header_bar.addWidget(self.lbl_content_title)
        header_bar.addStretch()
        header_bar.addWidget(self.lbl_count_info)
        content_layout.addLayout(header_bar)

        # Scrollable Cards Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(14)
        self.cards_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.cards_container)
        content_layout.addWidget(self.scroll_area, 1)

        main_layout.addWidget(content_area, 1)

    def setup_shortcuts(self):
        # Ctrl + K: Focus Search
        shortcut_search = QShortcut(QKeySequence("Ctrl+K"), self)
        shortcut_search.activated.connect(self.sidebar.focus_search)

        # Ctrl + N: Add Command
        shortcut_add_cmd = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_add_cmd.activated.connect(self.on_add_command)

        # Ctrl + Shift + N: Add Category
        shortcut_add_cat = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        shortcut_add_cat.activated.connect(self.on_add_category)

        # Ctrl + R: Refresh
        shortcut_refresh = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut_refresh.activated.connect(self.reload_data)

    def setup_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self)
        if self.icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(self.icon_path)))

        tray_menu = QMenu()
        show_action = QAction("Show Command Hub", self)
        show_action.triggered.connect(self.show_normal_window)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def show_normal_window(self):
        self.showNormal()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_normal_window()

    def reload_data(self):
        self.all_commands.clear()
        self.categories.clear()

        # Parse all .txt files in commands directory
        txt_files = sorted(list(self.commands_dir.glob("*.txt")))
        cat_counts = {}

        for txt_file in txt_files:
            cat_name, cmds = CommandParser.parse_file(txt_file, self.favorites)
            self.all_commands.extend(cmds)
            cat_counts[cat_name] = (txt_file, len(cmds))

        for cat_name, (txt_file, count) in cat_counts.items():
            self.categories.append(Category(
                name=cat_name,
                filename=txt_file.name,
                file_path=txt_file,
                count=count
            ))

        fav_count = sum(1 for c in self.all_commands if c.is_favorite)
        self.sidebar.populate_categories(
            self.categories,
            total_count=len(self.all_commands),
            fav_count=fav_count,
            active_category=self.active_category
        )

        self.refresh_cards_view()

    def refresh_cards_view(self):
        # Clear existing cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Filter commands
        filtered_commands: List[Command] = []

        for cmd in self.all_commands:
            # Category filter
            if self.active_category == "Favorites":
                if not cmd.is_favorite:
                    continue
            elif self.active_category != "All":
                if cmd.category.lower() != self.active_category.lower():
                    continue

            # Search query filter
            if self.search_query and not cmd.matches_search(self.search_query):
                continue

            filtered_commands.append(cmd)

        # Update Header info
        if self.search_query:
            self.lbl_content_title.setText(f"Search Results for '{self.search_query}'")
        elif self.active_category == "All":
            self.lbl_content_title.setText("All Commands")
        elif self.active_category == "Favorites":
            self.lbl_content_title.setText("★ Favorite Commands")
        else:
            self.lbl_content_title.setText(f"{self.active_category} Commands")

        self.lbl_count_info.setText(f"Showing {len(filtered_commands)} of {len(self.all_commands)} commands")

        # Empty state widget
        if not filtered_commands:
            empty_lbl = QLabel("No commands found matching your criteria.\nClick '+ Add Command' to add one!")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setStyleSheet("color: #a6adc8; font-size: 14px; padding: 40px;")
            self.cards_layout.addWidget(empty_lbl)
            return

        # Render Command Cards
        for cmd in filtered_commands:
            card = CommandCardWidget(cmd)
            card.favorite_toggled.connect(self.on_favorite_toggled)
            card.run_triggered.connect(self.on_run_command)
            card.edit_triggered.connect(self.on_edit_command)
            card.delete_triggered.connect(self.on_delete_command)
            self.cards_layout.addWidget(card)

    def on_category_selected(self, cat_name: str):
        self.active_category = cat_name
        self.refresh_cards_view()

    def on_search_changed(self, query: str):
        self.search_query = query
        self.refresh_cards_view()

    def on_favorite_toggled(self, command: Command):
        fav_key = f"{command.category}:{command.title}"
        if command.is_favorite:
            self.favorites.add(command.id)
            self.favorites.add(fav_key)
        else:
            self.favorites.discard(command.id)
            self.favorites.discard(fav_key)

        CommandParser.save_favorites(self.fav_file, self.favorites)
        fav_count = sum(1 for c in self.all_commands if c.is_favorite)
        self.sidebar.populate_categories(
            self.categories,
            total_count=len(self.all_commands),
            fav_count=fav_count,
            active_category=self.active_category
        )

    def on_add_command(self):
        dialog = AddEditCommandDialog(self.categories, current_category=self.active_category, parent=self)
        if dialog.exec() == AddEditCommandDialog.Accepted:
            data = dialog.result_data
            cat_name = data["category"]
            cat_slug = cat_name.lower().replace(" ", "_")
            target_file = self.commands_dir / f"{cat_slug}.txt"

            # Parse existing commands in target file
            _, existing_cmds = CommandParser.parse_file(target_file, self.favorites)
            
            new_cmd = Command(
                category=cat_name,
                title=data["title"],
                description=data["description"],
                code=data["code"],
                file_path=target_file
            )
            existing_cmds.append(new_cmd)

            # Save back to target file
            CommandParser.save_category_file(target_file, cat_name, existing_cmds)
            self.reload_data()

    def on_edit_command(self, command: Command):
        dialog = AddEditCommandDialog(self.categories, command=command, parent=self)
        if dialog.exec() == AddEditCommandDialog.Accepted:
            data = dialog.result_data
            orig_file = command.file_path or (self.commands_dir / f"{command.category.lower()}.txt")

            # Remove from orig file
            if orig_file.exists():
                cat_title, cmds = CommandParser.parse_file(orig_file, self.favorites)
                cmds = [c for c in cmds if c.id != command.id and c.title != command.title]
                CommandParser.save_category_file(orig_file, cat_title, cmds)

            # Add to new file
            new_cat_name = data["category"]
            new_cat_slug = new_cat_name.lower().replace(" ", "_")
            target_file = self.commands_dir / f"{new_cat_slug}.txt"

            _, target_cmds = CommandParser.parse_file(target_file, self.favorites)
            command.title = data["title"]
            command.category = new_cat_name
            command.description = data["description"]
            command.code = data["code"]
            command.file_path = target_file
            target_cmds.append(command)

            CommandParser.save_category_file(target_file, new_cat_name, target_cmds)
            self.reload_data()

    def on_delete_command(self, command: Command):
        reply = QMessageBox.question(
            self,
            "Delete Command",
            f"Are you sure you want to delete '{command.title}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            target_file = command.file_path
            if target_file and target_file.exists():
                cat_title, cmds = CommandParser.parse_file(target_file, self.favorites)
                cmds = [c for c in cmds if c.title != command.title]
                CommandParser.save_category_file(target_file, cat_title, cmds)
                self.reload_data()

    def on_add_category(self):
        dialog = AddCategoryDialog(parent=self)
        if dialog.exec() == AddCategoryDialog.Accepted:
            cat_name = dialog.category_name
            cat_slug = cat_name.lower().replace(" ", "_")
            target_file = self.commands_dir / f"{cat_slug}.txt"

            if not target_file.exists():
                CommandParser.save_category_file(target_file, cat_name, [])
            self.reload_data()

    def on_run_command(self, command: Command):
        is_dangerous = any(kw in command.code for kw in DANGEROUS_KEYWORDS)
        if is_dangerous:
            warn_dialog = DangerousCommandDialog(command, parent=self)
            if warn_dialog.exec() != DangerousCommandDialog.Accepted:
                return

        out_dialog = TerminalOutputDialog(command, parent=self)
        out_dialog.exec()

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.setStyleSheet(Themes.LIGHT)
            self.sidebar.btn_theme.setText("☀️ Switch Theme")
        else:
            self.current_theme = "dark"
            self.setStyleSheet(Themes.DARK)
            self.sidebar.btn_theme.setText("🌙 Switch Theme")
