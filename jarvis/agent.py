from __future__ import annotations

import os

from jarvis.tools.knowledge import KnowledgeTool
from jarvis.tools.memory import MemoryTool
from jarvis.tools.system import SystemTool
from jarvis.tools.voice import VoiceTool


class JarvisAgent:
    def __init__(self, voice: bool = False) -> None:
        self.voice_enabled = voice
        self.memory = MemoryTool()
        self.knowledge = KnowledgeTool()
        self.system = SystemTool()
        self.voice_tool = VoiceTool() if voice else None

    def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)
        if user_input.lower().startswith("search "):
            result = self.knowledge.search(user_input[7:])
        elif user_input.lower().startswith("run "):
            result = self.system.run(user_input[4:])
        else:
            result = f"[JARVIS] You said: {user_input} (memory: {len(self.memory.history())} turns)"
        self.memory.add("assistant", result)
        return result

    def speak(self, text: str) -> None:
        if self.voice_tool:
            self.voice_tool.speak(text)
