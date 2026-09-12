from __future__ import annotations

import argparse

from jarvis.agent import JarvisAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="JARVIS")
    parser.add_argument("--voice", action="store_true", help="enable voice I/O")
    args = parser.parse_args()

    agent = JarvisAgent(voice=args.voice)
    print("JARVIS online. Type 'exit' to quit." + (" [voice]" if args.voice else ""))
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
