from __future__ import annotations

import json
from pathlib import Path
from typing import Final


MAX_HISTORY: Final = 20


class MemoryTool:
    def __init__(self, path: str = "memory/history.json", max_history: int = MAX_HISTORY) -> None:
        self.path = Path(path)
        self.max_history = max_history
        self._data: list[dict] = []
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, list):
                    self._data = [
                        item
                        for item in loaded
                        if isinstance(item, dict)
                        and item.get("role") in {"user", "assistant"}
                        and isinstance(item.get("content"), str)
                    ][-self.max_history :]
            except (OSError, json.JSONDecodeError):
                self._data = []

    def add(self, role: str, content: str) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("Memory role must be 'user' or 'assistant'.")
        self._data.append({"role": role, "content": content})
        self._data = self._data[-self.max_history :]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary_path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
        temporary_path.replace(self.path)

    def history(self) -> list[dict]:
        return list(self._data)

    def clear(self) -> None:
        self._data = []
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("[]", encoding="utf-8")
