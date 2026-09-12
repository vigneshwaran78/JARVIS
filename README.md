# JARVIS

Stark-inspired AI assistant — voice, system control, proactive memory, knowledge+web.

## Stack

* `jarvis/agent.py` — orchestrator (OpenRouter)
* `jarvis/tools/voice.py` — STT (whisper) + TTS (pyttsx3/elevenlabs) stubs
* `jarvis/tools/system.py` — whitelisted system commands
* `jarvis/tools/memory.py` — persistent JSON memory (survives restarts)
* `jarvis/tools/knowledge.py` — web search/fetch via context7/playwright

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set OPENROUTER_API_KEY, OPENROUTER_MODEL
python main.py
# voice: python main.py --voice
```

See `opencode.json` for MCP servers (github, filesystem, memory, sequential-thinking, playwright, context7).
