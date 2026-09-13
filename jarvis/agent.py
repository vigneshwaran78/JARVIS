from __future__ import annotations

from config.env import get_settings
from jarvis.tools.knowledge import KnowledgeTool
from jarvis.tools.memory import MemoryTool
from jarvis.tools.system import SystemTool
from jarvis.tools.voice import VoiceTool
from providers.openrouter_provider import OpenRouterProvider


SYSTEM_PROMPT = "You are JARVIS, a witty, concise, helpful AI assistant like Tony Stark's JARVIS. Be proactive, concise, and a bit witty."


class JarvisAgent:
    def __init__(self, voice: bool = False) -> None:
        settings = get_settings()
        self.provider = OpenRouterProvider(
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.openrouter_site_url,
            app_name=settings.openrouter_app_name,
        )
        self.voice_enabled = voice
        self.memory = MemoryTool()
        self.knowledge = KnowledgeTool()
        self.system = SystemTool()
        self.voice_tool = VoiceTool() if voice else None
        self._messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in self.memory.history():
            self._messages.append(m)

    def run(self, user_input: str) -> str:
        if user_input.lower().startswith("search "):
            result = self.knowledge.search(user_input[7:])
            self.memory.add("user", user_input)
            self.memory.add("assistant", result)
            return result
        if user_input.lower().startswith("run "):
            result = self.system.run(user_input[4:])
            self.memory.add("user", user_input)
            self.memory.add("assistant", result)
            return result

        self._messages.append({"role": "user", "content": user_input})
        self.memory.add("user", user_input)
        fallbacks = [
            self.provider.model,
            "cohere/north-mini-code:free",
            "liquid/lfm-2.5-2.6b:free",
        ]
        last_error = None
        for model in fallbacks:
            try:
                self.provider.model = model
                choice = self.provider.chat(self._messages)
                content = choice["message"]["content"] or ""
                self._messages.append({"role": "assistant", "content": content})
                self.memory.add("assistant", content)
                return content
            except RuntimeError as e:
                last_error = e
                if "429" in str(e) and model != fallbacks[-1]:
                    continue
                raise
        raise last_error or RuntimeError("All models rate-limited")

    def speak(self, text: str) -> None:
        if self.voice_tool:
            self.voice_tool.speak(text)
