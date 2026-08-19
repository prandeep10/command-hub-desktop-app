import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class Command:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    category: str = "General"
    title: str = ""
    description: str = ""
    code: str = ""
    is_favorite: bool = False
    file_path: Optional[Path] = None

    def matches_search(self, query: str) -> bool:
        if not query:
            return True
        q = query.lower().strip()
        return (
            q in self.title.lower() or
            q in self.description.lower() or
            q in self.code.lower() or
            q in self.category.lower()
        )

@dataclass
class Category:
    name: str
    filename: str
    file_path: Path
    count: int = 0
