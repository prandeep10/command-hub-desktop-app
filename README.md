# ⚡ Command Hub

> **A modern, lightning-fast personal command launcher & developer library app built with PySide6.**  
> *Pin to your Linux taskbar, copy CLI commands in milliseconds, and stop asking ChatGPT for the same commands over and over again.*

---

## 💡 The Concept & Motivation

As developers, we find ourselves asking **ChatGPT**, searching Google, or digging through old notes multiple times a day for the **exact same CLI commands**:

- *"What was the syntax to follow Nginx logs again?"* `journalctl -xe -u nginx`
- *"How do I force rebuild containers without cache?"* `docker compose up -d --build`
- *"What was that git log graph command?"* `git log --oneline --graph --decorate`
- *"How do I clear all Laravel caches in one line?"* `php artisan cache:clear && php artisan config:clear`

Opening a browser tab, navigating to ChatGPT, typing a prompt, and waiting for an AI response just to get a single terminal command breaks your focus and wastes valuable time.

### **The Solution: Command Hub**

**Command Hub** is a lightweight, offline desktop command launcher that sits quietly on your system dock or taskbar. 

- **No AI required. No browser tabs. No online connectivity needed.**
- Press `Ctrl + K` to search your library instantly.
- Click **[📋 Copy]** to copy the command straight to your clipboard, or click **[▶ Run]** to execute it in a terminal pop-up.
- **Zero Database Overhead**: Plain `.txt` files in `commands/` act as your database. You can edit them with VS Code, back them up, or version control them with Git!

---

## ✨ Features

- 🎨 **Modern Dark & Light UI**: Sleek Catppuccin-inspired dark mode interface with glassmorphism accents and a one-click theme switcher.
- 📁 **Plain `.txt` Database**: No SQLite, Postgres, or heavy databases required. Your commands live in human-readable `.txt` files in `commands/` (`git.txt`, `linux.txt`, `docker.txt`, etc.).
- 🔍 **Instant Search (`Ctrl + K`)**: Real-time filtering across titles, descriptions, categories, or command text.
- 📋 **One-Click Clipboard Copying**: Copies command text instantly with visual `✓ Copied!` toast feedback.
- ▶️ **Safe Subprocess Execution**: Run commands directly inside the app with live stdout/stderr console output.
- ⚠️ **High-Risk Safety Warning**: Automatically detects dangerous operations (`sudo`, `rm -rf`, `dd`, `drop database`, `killall`) and prompts for confirmation before executing.
- ★ **Favorites**: Star frequently used commands for one-click access in your *Favorites* filter view.
- 📂 **Full GUI CRUD**: Add, edit, or delete categories and commands directly from the GUI with instant sync back to `.txt` files.
- 📌 **Linux Taskbar & Dock Integration**: Includes an automated installer (`install.sh`) that registers `command-hub.desktop` in `~/.local/share/applications/` so you can pin it to your desktop panel.

---

## 🖥️ UI Layout Preview

```text
┌──────────────────────────────────────────────────────────┐
│  ⚡ COMMAND HUB                           🔍 Search...   │
├───────────────┬──────────────────────────────────────────┤
│               │  Linux Commands (6 commands)             │
│  📁 All (44)  │                                          │
│  ★ Favs (5)   │  ┌────────────────────────────────────┐  │
│               │  │ Restart Nginx Web Server           │  │
│  📄 Linux     │  │ Gracefully restart Nginx service   │  │
│  📄 Git       │  │ sudo systemctl restart nginx       │  │
│  📄 Docker    │  │ [📋 Copy]  [▶ Run]   [✏️ Edit] [🗑️]│  │
│  📄 Laravel   │  └────────────────────────────────────┘  │
│  📄 React     │                                          │
│  📄 Node      │  ┌────────────────────────────────────┐  │
│  📄 MySQL     │  │ Live System Journal Logs           │  │
│  📄 SSH       │  │ journalctl -xe -u nginx --no-pager │  │
│               │  │ [📋 Copy]  [▶ Run]   [✏️ Edit] [🗑️]│  │
│  ➕ Add Cmd   │  └────────────────────────────────────┘  │
│  📂 Add Cat   │                                          │
└───────────────┴──────────────────────────────────────────┘
```

---

## 🛠️ Project Structure

```text
command-hub/
├── app.py                      # Main PySide6 application entry point
├── parser.py                   # TXT file parser & serializer (2-way sync)
├── models.py                   # Data models (Command, Category, Favorites)
├── install.sh                  # One-click desktop installer script
├── command-hub.desktop         # Linux Desktop launcher entry
├── create_icon.py              # Application icon generator
├── assets/
│   └── icon.png                # Application icon
├── ui/
│   ├── main_window.py          # Main application window & layout controller
│   ├── sidebar.py              # Category sidebar with search box & counters
│   ├── command_card.py         # Interactive command card component
│   ├── dialogs.py              # Modals for Add/Edit Command, Safety Warning, Terminal Console
│   └── styles.py               # Dark & Light QSS theme stylesheets
└── commands/                   # Plain text command database files
    ├── linux.txt
    ├── git.txt
    ├── docker.txt
    ├── laravel.txt
    ├── react.txt
    ├── node.txt
    ├── mysql.txt
    ├── ssh.txt
    └── custom.txt
```

---

## 📝 `.txt` Database Format

Commands are stored in human-readable Markdown-style `.txt` files inside `commands/`:

```text
# Git Commands

## Check Working Tree Status
# Description: Show modified, untracked, and staged files
git status

## Stage & Commit All Changes
# Description: Add all modified/new files and create a commit
git add . && git commit -m "Update codebase"
```

Simple line-by-line format is also supported:

```text
git status
git add .
git commit -m "update"
git push origin main
```

---

## 🚀 Installation & Setup

### Quick Installation (Linux)

1. **Clone the repository**:
   ```bash
   git clone git@github.com:prandeep10/command-hub-desktop-app.git
   cd command-hub-desktop-app
   ```

2. **Run the Automated Setup & Installer**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Launch & Pin to Taskbar**:
   - Open your application menu (<kbd>Super</kbd> / <kbd>Windows</kbd> key).
   - Search for **Command Hub**.
   - Right-click and choose **Pin to Taskbar / Dock**.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| <kbd>Ctrl</kbd> + <kbd>K</kbd> | Focus Search Input Bar |
| <kbd>Ctrl</kbd> + <kbd>N</kbd> | Add New Command Dialog |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd> | Add New Category Dialog |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Reload `.txt` Database |

---

## 📄 License

Open source under the [MIT License](LICENSE). Built for developers who value speed, minimalism, and focus.
