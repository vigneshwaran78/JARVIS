from __future__ import annotations

import json
from pathlib import Path


class MemoryTool:
    def __init__(self, path: str = "memory/history.json") -> None:
        self.path = Path(path)
        self._data: list[dict] = []
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text())
            except Exception:
                self._data = []

    def add(self, role: str, content: str) -> None:
        self._data.append({"role": role, "content": content})
        self._data = self._data[-20:]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))

    def history(self) -> list[dict]:
        return self._data
