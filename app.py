import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

def main():
    # Enable high DPI support
    app = QApplication(sys.argv)
    app.setApplicationName("Command Hub")
    app.setOrganizationName("Personal Tools")

    base_dir = Path(__file__).parent.resolve()
    icon_path = base_dir / "assets" / "icon.png"

    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow(base_dir=base_dir, icon_path=icon_path)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
