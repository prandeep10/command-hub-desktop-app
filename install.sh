#!/bin/bash

# Get absolute directory of script
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_PYTHON="$APP_DIR/venv/bin/python"
APP_PY="$APP_DIR/app.py"
ICON_PNG="$APP_DIR/assets/icon.png"
DESKTOP_FILE="$APP_DIR/command-hub.desktop"
TARGET_DESKTOP_DIR="$HOME/.local/share/applications"

echo "⚡ Installing Command Hub Desktop Launcher..."
echo "App Directory: $APP_DIR"
echo "Python Path:   $VENV_PYTHON"

# Create .desktop file
cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=Command Hub
Comment=Personal Command Launcher & Command Library
Exec="$VENV_PYTHON" "$APP_PY"
Icon=$ICON_PNG
Terminal=false
Type=Application
Categories=Utility;Development;
Keywords=command;launcher;terminal;git;docker;linux;cli;
EOF

chmod +x "$DESKTOP_FILE"

# Install to ~/.local/share/applications/
mkdir -p "$TARGET_DESKTOP_DIR"
cp "$DESKTOP_FILE" "$TARGET_DESKTOP_DIR/command-hub.desktop"
chmod +x "$TARGET_DESKTOP_DIR/command-hub.desktop"

# Refresh desktop database if tool exists
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$TARGET_DESKTOP_DIR" &> /dev/null
fi

echo "✅ Desktop launcher installed successfully!"
echo "📍 Location: $TARGET_DESKTOP_DIR/command-hub.desktop"
echo "📌 You can now search 'Command Hub' in your application menu and pin it to your taskbar/dock!"
