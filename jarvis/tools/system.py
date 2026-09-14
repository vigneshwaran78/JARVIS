from __future__ import annotations

import subprocess
import shlex


ALLOWED_COMMANDS = frozenset({"ls", "pwd", "echo", "cat", "open", "say"})
MAX_OUTPUT_CHARS = 4_000


class SystemTool:
    def run(self, command: str) -> str:
        try:
            args = shlex.split(command)
        except ValueError as error:
            return f"Invalid command: {error}"

        if not args:
            return "Blocked: no command provided"
        if args[0] not in ALLOWED_COMMANDS:
            return f"Blocked: '{args[0]}' not in allowed {tuple(sorted(ALLOWED_COMMANDS))}"

        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except FileNotFoundError:
            return f"Error: command not found: {args[0]}"
        except subprocess.TimeoutExpired:
            return "Error: command timed out after 10 seconds"
        except OSError as error:
            return f"Error: {error}"

        output = result.stdout or result.stderr
        if result.returncode:
            return f"Error (exit {result.returncode}): {output[:MAX_OUTPUT_CHARS]}"
        return output[:MAX_OUTPUT_CHARS]
