from __future__ import annotations


class VoiceTool:
    def listen(self) -> str:
        try:
            import speech_recognition as sr

            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
            return r.recognize_google(audio)
        except Exception as e:
            return f"[voice listen error: {e}]"

    def speak(self, text: str) -> None:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[voice speak error: {e}]")
