from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


class RequestLogger:
    def __init__(self, log_dir: str = "logs/requests") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def create_log(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> Path:
        log_path = self._new_log_path()
        log_data = {
            "started_at": _now(),
            "method": method,
            "url": url,
            "headers": _redact_headers(headers),
            "request": payload,
            "response": None,
            "error": None,
        }
        self._write(log_path, log_data)
        return log_path

    def save_response(self, log_path: Path, status_code: int, response: dict[str, Any]) -> None:
        log_data = self._read(log_path)
        log_data["finished_at"] = _now()
        log_data["status_code"] = status_code
        log_data["response"] = response
        self._write(log_path, log_data)

    def save_error(self, log_path: Path, status_code: int | None, error: str) -> None:
        log_data = self._read(log_path)
        log_data["finished_at"] = _now()
        log_data["status_code"] = status_code
        log_data["error"] = error
        self._write(log_path, log_data)

    def _new_log_path(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return self.log_dir / f"{timestamp}-{uuid4().hex[:8]}.json"

    def _read(self, log_path: Path) -> dict[str, Any]:
        return json.loads(log_path.read_text(encoding="utf-8"))

    def _write(self, log_path: Path, data: dict[str, Any]) -> None:
        log_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _redact_headers(headers: dict[str, str]) -> dict[str, str]:
    redacted = dict(headers)
    if "Authorization" in redacted:
        redacted["Authorization"] = "Bearer ***"
    return redacted


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")

