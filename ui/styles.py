class Themes:
    DARK = """
    /* Main Window & Core Widgets */
    QMainWindow, QDialog {
        background-color: #181825;
        color: #cdd6f4;
        font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    }
    
    QWidget {
        color: #cdd6f4;
        font-size: 13px;
    }

    /* Sidebar Styling */
    #sidebarWidget {
        background-color: #1e1e2e;
        border-right: 1px solid #313244;
    }

    #sidebarHeader {
        font-size: 16px;
        font-weight: bold;
        color: #89b4fa;
        padding: 12px 6px;
    }

    /* Search Box */
    QLineEdit#searchBox {
        background-color: #11111b;
        border: 1px solid #45475a;
        border-radius: 8px;
        padding: 10px 14px;
        color: #cdd6f4;
        font-size: 13px;
        selection-background-color: #89b4fa;
        selection-color: #11111b;
    }

    QLineEdit#searchBox:focus {
        border: 1px solid #89b4fa;
        background-color: #181825;
    }

    /* Category List Buttons */
    QListWidget#categoryList {
        background-color: transparent;
        border: none;
        outline: none;
    }

    QListWidget#categoryList::item {
        background-color: transparent;
        color: #bac2de;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 4px;
        font-weight: 500;
    }

    QListWidget#categoryList::item:hover {
        background-color: #313244;
        color: #cdd6f4;
    }

    QListWidget#categoryList::item:selected {
        background-color: #89b4fa;
        color: #11111b;
        font-weight: bold;
    }

    /* Buttons */
    QPushButton {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #45475a;
        border-color: #585b70;
    }

    QPushButton:pressed {
        background-color: #585b70;
    }

    QPushButton#btnPrimary {
        background-color: #89b4fa;
        color: #11111b;
        border: none;
    }

    QPushButton#btnPrimary:hover {
        background-color: #b4befe;
    }

    QPushButton#btnCopy {
        background-color: #a6e3a1;
        color: #11111b;
        border: none;
    }

    QPushButton#btnCopy:hover {
        background-color: #94e2d5;
    }

    QPushButton#btnRun {
        background-color: #f9e2af;
        color: #11111b;
        border: none;
    }

    QPushButton#btnRun:hover {
        background-color: #f5e0dc;
    }

    QPushButton#btnDanger {
        background-color: #f38ba8;
        color: #11111b;
        border: none;
    }

    QPushButton#btnDanger:hover {
        background-color: #eba0ac;
    }

    /* Command Card Container */
    QFrame#commandCard {
        background-color: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 12px;
        padding: 16px;
    }

    QFrame#commandCard:hover {
        border-color: #89b4fa;
        background-color: #24273a;
    }

    QLabel#cardTitle {
        font-size: 15px;
        font-weight: bold;
        color: #cdd6f4;
    }

    QLabel#cardCategory {
        background-color: #313244;
        color: #89b4fa;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: bold;
    }

    QLabel#cardDescription {
        color: #a6adc8;
        font-size: 12px;
    }

    /* Code Container inside Card */
    QTextEdit#codeBox {
        background-color: #11111b;
        color: #a6e3a1;
        border: 1px solid #313244;
        border-radius: 8px;
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        padding: 10px;
    }

    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background-color: #181825;
        width: 8px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical {
        background-color: #45475a;
        border-radius: 4px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #585b70;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    /* Form Dialog Controls */
    QLabel#formLabel {
        font-weight: 600;
        color: #bac2de;
        margin-top: 6px;
    }

    QLineEdit, QTextEdit {
        background-color: #11111b;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 8px 10px;
        color: #cdd6f4;
    }

    QLineEdit:focus, QTextEdit:focus {
        border-color: #89b4fa;
    }
    """

    LIGHT = """
    QMainWindow, QDialog {
        background-color: #eff1f5;
        color: #4c4f69;
        font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    }
    
    QWidget {
        color: #4c4f69;
        font-size: 13px;
    }

    #sidebarWidget {
        background-color: #e6e9ef;
        border-right: 1px solid #ccd0da;
    }

    #sidebarHeader {
        font-size: 16px;
        font-weight: bold;
        color: #1e66f5;
        padding: 12px 6px;
    }

    QLineEdit#searchBox {
        background-color: #ffffff;
        border: 1px solid #bcc0cc;
        border-radius: 8px;
        padding: 10px 14px;
        color: #4c4f69;
    }

    QLineEdit#searchBox:focus {
        border: 1px solid #1e66f5;
    }

    QListWidget#categoryList {
        background-color: transparent;
        border: none;
    }

    QListWidget#categoryList::item {
        color: #5c5f77;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 4px;
    }

    QListWidget#categoryList::item:hover {
        background-color: #ccd0da;
    }

    QListWidget#categoryList::item:selected {
        background-color: #1e66f5;
        color: #ffffff;
        font-weight: bold;
    }

    QPushButton {
        background-color: #dce0e8;
        color: #4c4f69;
        border: 1px solid #bcc0cc;
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #bcc0cc;
    }

    QPushButton#btnPrimary {
        background-color: #1e66f5;
        color: #ffffff;
        border: none;
    }

    QPushButton#btnPrimary:hover {
        background-color: #7287fd;
    }

    QPushButton#btnCopy {
        background-color: #40a02b;
        color: #ffffff;
        border: none;
    }

    QPushButton#btnRun {
        background-color: #df8e1d;
        color: #ffffff;
        border: none;
    }

    QPushButton#btnDanger {
        background-color: #d20f39;
        color: #ffffff;
        border: none;
    }

    QFrame#commandCard {
        background-color: #ffffff;
        border: 1px solid #ccd0da;
        border-radius: 12px;
        padding: 16px;
    }

    QFrame#commandCard:hover {
        border-color: #1e66f5;
    }

    QLabel#cardTitle {
        font-size: 15px;
        font-weight: bold;
        color: #4c4f69;
    }

    QLabel#cardCategory {
        background-color: #e6e9ef;
        color: #1e66f5;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: bold;
    }

    QLabel#cardDescription {
        color: #6c6f85;
        font-size: 12px;
    }

    QTextEdit#codeBox {
        background-color: #24273a;
        color: #a6e3a1;
        border: 1px solid #ccd0da;
        border-radius: 8px;
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        padding: 10px;
    }

    QLineEdit, QTextEdit {
        background-color: #ffffff;
        border: 1px solid #bcc0cc;
        border-radius: 6px;
        padding: 8px 10px;
        color: #4c4f69;
    }
    """
