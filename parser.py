import json
import re
from pathlib import Path
from typing import List, Tuple, Set
from models import Command, Category

class CommandParser:
    """
    Parser and serializer for Command Hub .txt database files.
    Supports structured markdown format (# Category, ## Title, # Description, code)
    as well as simple plain line-by-line format.
    """

    @staticmethod
    def load_favorites(fav_file: Path) -> Set[str]:
        if not fav_file.exists():
            return set()
        try:
            data = json.loads(fav_file.read_text(encoding="utf-8"))
            return set(data.get("favorites", []))
        except Exception:
            return set()

    @staticmethod
    def save_favorites(fav_file: Path, favorites: Set[str]) -> None:
        fav_file.parent.mkdir(parents=True, exist_ok=True)
        data = {"favorites": list(favorites)}
        fav_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def parse_file(file_path: Path, favorites: Set[str]) -> Tuple[str, List[Command]]:
        """
        Parses a .txt file into a Category name and list of Command objects.
        """
        if not file_path.exists():
            return file_path.stem.capitalize(), []

        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        category_name = file_path.stem.replace("_", " ").replace("-", " ").capitalize()
        commands: List[Command] = []

        # Check for top level category header `# Category Name`
        first_non_empty = next((line.strip() for line in lines if line.strip()), None)
        if first_non_empty and first_non_empty.startswith("# ") and not first_non_empty.startswith("## "):
            category_name = first_non_empty[2:].strip()

        current_title = ""
        current_description = ""
        current_code_lines: List[str] = []

        def flush_command():
            nonlocal current_title, current_description, current_code_lines
            if not current_code_lines and not current_title:
                return

            code_text = "\n".join(current_code_lines).strip()
            if not code_text and not current_title:
                return

            # If no explicit title was provided (e.g. simple line format)
            if not current_title:
                current_title = code_text.splitlines()[0] if code_text else "Command"

            cmd_id = f"{file_path.stem}_{len(commands)+1}_{hash(current_title + code_text) & 0xffff:04x}"
            is_fav = cmd_id in favorites or f"{category_name}:{current_title}" in favorites

            cmd = Command(
                id=cmd_id,
                category=category_name,
                title=current_title,
                description=current_description.strip(),
                code=code_text,
                is_favorite=is_fav,
                file_path=file_path
            )
            commands.append(cmd)

            # Reset buffers
            current_title = ""
            current_description = ""
            current_code_lines = []

        for line in lines:
            stripped = line.strip()

            # Top-level category title
            if stripped.startswith("# ") and not stripped.startswith("## "):
                continue

            # Section header `## Command Title`
            if stripped.startswith("## "):
                flush_command()
                current_title = stripped[3:].strip()
                continue

            # Description line `# Description: ...` or `# comment`
            if stripped.startswith("#"):
                comment_content = stripped[1:].strip()
                if comment_content.lower().startswith("description:"):
                    current_description = comment_content[12:].strip()
                elif not current_description and not current_code_lines:
                    current_description = comment_content
                continue

            # Blank line: separates commands if no ## header is used
            if not stripped:
                if current_code_lines and not lines_have_heading_markers(lines):
                    flush_command()
                continue

            # Actual command line
            current_code_lines.append(line)

        flush_command()
        return category_name, commands

    @staticmethod
    def save_category_file(file_path: Path, category_name: str, commands: List[Command]) -> None:
        """
        Serializes commands back to a .txt file.
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# {category_name}", ""]

        for cmd in commands:
            lines.append(f"## {cmd.title}")
            if cmd.description:
                lines.append(f"# Description: {cmd.description}")
            for code_line in cmd.code.splitlines():
                lines.append(code_line)
            lines.append("") # Empty line separator

        file_path.write_text("\n".join(lines), encoding="utf-8")

def lines_have_heading_markers(lines: List[str]) -> bool:
    return any(line.strip().startswith("## ") for line in lines)
