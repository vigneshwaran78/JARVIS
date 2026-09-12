from __future__ import annotations

import subprocess
import json


class KnowledgeTool:
    def search(self, query: str) -> str:
        return f"[knowledge] search '{query}' — wire to context7/playwright via MCP (placeholder). Use @context7 to fetch live docs."
