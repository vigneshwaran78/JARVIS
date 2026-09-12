from __future__ import annotations

import subprocess


ALLOWED_PREFIXES = ("ls", "pwd", "echo", "cat", "open", "say")


class SystemTool:
    def run(self, command: str) -> str:
        if not any(command.strip().startswith(p) for p in ALLOWED_PREFIXES):
            return f"Blocked: '{command}' not in allowed {ALLOWED_PREFIXES}"
        try:
            out = subprocess.check_output(command, shell=True, timeout=10, text=True)
            return out[:4000]
        except Exception as e:
            return f"Error: {e}"
