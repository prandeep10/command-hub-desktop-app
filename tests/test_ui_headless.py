import sys
import os
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def test_headless_ui():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    app = QApplication(sys.argv)
    icon_path = root_dir / "assets" / "icon.png"

    window = MainWindow(base_dir=root_dir, icon_path=icon_path)
    print("MainWindow instantiated successfully.")

    assert len(window.all_commands) >= 44, f"Expected at least 44 commands, got {len(window.all_commands)}"
    assert len(window.categories) >= 9, f"Expected at least 9 categories, got {len(window.categories)}"
    print("All UI data assertions passed!")

if __name__ == "__main__":
    test_headless_ui()
