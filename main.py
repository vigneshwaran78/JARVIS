from __future__ import annotations

import argparse

from jarvis.agent import JarvisAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="JARVIS")
    parser.add_argument("--voice", action="store_true", help="enable voice I/O")
    parser.add_argument("--daemon", action="store_true", help="wake-word daemon (no stdin)")
    args = parser.parse_args()

    agent = JarvisAgent(voice=args.voice or args.daemon)
    print("JARVIS online. Type 'exit' to quit." + (" [voice]" if args.voice else "") + (" [daemon]" if args.daemon else ""))

    import sys

    if args.daemon or (args.voice and not sys.stdin.isatty()):
        print("JARVIS daemon: listening for 'Hey JARVIS'...")
        while True:
            try:
                heard = agent.voice_tool.listen() if agent.voice_tool else ""
            except Exception as e:
                print(f"listen error: {e}")
                continue
            if not heard:
                continue
            if "hey jarvis" not in heard.lower():
                continue
            print(f"Heard wake word: {heard}")
            agent.speak("Yes?")
            try:
                command = agent.voice_tool.listen() if agent.voice_tool else ""
            except Exception:
                command = ""
            if not command or command.lower() in {"exit", "quit"}:
                continue
            try:
                answer = agent.run(command)
                print(f"JARVIS: {answer}")
                agent.speak(answer)
            except Exception as error:
                print(f"Error: {error}")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            break
        if user_input.lower() in {"exit", "quit"}:
            print("JARVIS: Goodbye.")
            break
        if not user_input:
            continue
        try:
            answer = agent.run(user_input)
            print(f"\nJARVIS: {answer}")
            if args.voice:
                agent.speak(answer)
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
