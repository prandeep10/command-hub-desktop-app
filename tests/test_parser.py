import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from parser import CommandParser
from models import Command

def test_parser():
    commands_dir = root_dir / "commands"
    fav_file = commands_dir / "favorites.json"

    favorites = CommandParser.load_favorites(fav_file)
    print(f"Loaded {len(favorites)} favorites.")

    txt_files = list(commands_dir.glob("*.txt"))
    print(f"Found {len(txt_files)} command files.")
    assert len(txt_files) >= 9, "Expected at least 9 starter .txt files"

    total_cmds = 0
    for txt_file in txt_files:
        cat_name, cmds = CommandParser.parse_file(txt_file, favorites)
        print(f"File: {txt_file.name} -> Category: '{cat_name}' ({len(cmds)} commands)")
        total_cmds += len(cmds)
        assert len(cmds) > 0, f"Expected commands in {txt_file.name}"

    print(f"Total commands parsed across all files: {total_cmds}")

    # Test serializer round-trip on dummy file
    dummy_file = commands_dir / "test_temp.txt"
    test_commands = [
        Command(title="Test Cmd 1", description="Desc 1", code="echo 'hello'"),
        Command(title="Test Cmd 2", description="Desc 2", code="ls -la")
    ]
    CommandParser.save_category_file(dummy_file, "TestTemp", test_commands)
    assert dummy_file.exists(), "Dummy file creation failed"

    cat_name_read, cmds_read = CommandParser.parse_file(dummy_file, favorites)
    assert cmds_read[0].title == "Test Cmd 1"
    assert cmds_read[0].code == "echo 'hello'"

    # Cleanup dummy file
    if dummy_file.exists():
        dummy_file.unlink()
    print("✅ All Parser unit tests passed successfully!")

if __name__ == "__main__":
    test_parser()
