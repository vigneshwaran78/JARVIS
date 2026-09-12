from __future__ import annotations


class VoiceTool:
    def listen(self, debug: bool = True) -> str:
        try:
            import speech_recognition as sr

            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            with sr.Microphone() as source:
                if debug:
                    print("Calibrating mic...")
                r.adjust_for_ambient_noise(source, duration=1)
                if debug:
                    print("Listening...")
                audio = r.listen(source, timeout=8, phrase_time_limit=5)
            text = r.recognize_google(audio, language="en-US")
            if debug:
                print(f"Heard: {text}")
            return text
        except Exception as e:
            if debug:
                print(f"[voice listen error: {e}]")
            return ""

    def speak(self, text: str) -> None:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[voice speak error: {e}]")
