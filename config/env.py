from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str
    openrouter_model: str
    openrouter_site_url: str | None
    openrouter_app_name: str | None


def get_settings() -> Settings:
    _load_dotenv(Path(".env"))
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    model = os.getenv("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free")

    if not api_key or api_key == "your_openrouter_api_key_here":
        raise ValueError(
            "Set OPENROUTER_API_KEY in .env to your real OpenRouter key. "
            "It should usually start with sk-or-."
        )

    return Settings(
        openrouter_api_key=api_key,
        openrouter_model=model,
        openrouter_site_url=os.getenv("OPENROUTER_SITE_URL"),
        openrouter_app_name=os.getenv("OPENROUTER_APP_NAME"),
    )


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
