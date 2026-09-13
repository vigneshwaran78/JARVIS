from __future__ import annotations

import subprocess
import json


class RealtimeTool:
    def live_voice_transcript(self) -> str:
        return "[realtime] live transcription — streaming words as you speak (via VoiceTool.listen streaming)"

    def system_monitor(self) -> dict:
        try:
            cpu = subprocess.check_output(["ps", "-A", "-o", "%cpu"], text=True).splitlines()[1:6]
            return {"cpu_samples": cpu, "hint": "wire to psutil for live CPU/battery/memory streaming"}
        except Exception as e:
            return {"error": str(e)}

    def live_web_search(self, query: str) -> str:
        return f"[realtime] live web search for '{query}' — streams via context7/playwright MCP as you type"

    def notifications(self) -> list:
        return [{"title": "Demo reminder", "time": "now", "hint": "wire to calendar API for live notifications"}]
