from __future__ import annotations

import tkinter as tk

from jarvis.agent import JarvisAgent


class JarvisBubble:
    def __init__(self) -> None:
        self.agent = JarvisAgent(voice=True)
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"60x60+{sw-84}+{sh-84}")
        self.root.configure(bg="#131314")

        self.bubble = tk.Button(
            self.root,
            text="J",
            font=("Helvetica", 20, "bold"),
            bg="#8ab4f8",
            fg="#202124",
            bd=0,
            activebackground="#aecbfa",
            command=self.toggle_chat,
        )
        self.bubble.pack(fill="both", expand=True)

        self.bubble.bind("<Button-1>", lambda e: self.toggle_chat())
        self.bubble.bind("<B1-Motion>", self.drag)
        self.chat_win: tk.Toplevel | None = None
        self.rgb_colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#8b00ff"]
        self.rgb_idx = 0
        self._animate_bubble()

    def _animate_bubble(self) -> None:
        self.bubble.configure(bg=self.rgb_colors[self.rgb_idx % len(self.rgb_colors)])
        self.rgb_idx += 1
        self.root.after(300, self._animate_bubble)

    def drag(self, event: tk.Event) -> None:
        self.root.geometry(f"+{event.x_root-30}+{event.y_root-30}")

    def toggle_chat(self) -> None:
        if self.chat_win and self.chat_win.winfo_exists():
            self.chat_win.destroy()
            self.chat_win = None
            return
        self.chat_win = tk.Toplevel(self.root)
        self.chat_win.title("JARVIS — Gemini RGB")
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.chat_win.geometry(f"366x466+{sw-387}+{sh-547}")
        self.chat_win.configure(bg="#ff0000")
        self.chat_win.attributes("-topmost", True)

        rgb_frame = tk.Frame(self.chat_win, bg="#ff0000")
        rgb_frame.pack(fill="both", expand=True, padx=3, pady=3)

        inner = tk.Frame(rgb_frame, bg="#131314")
        inner.pack(fill="both", expand=True)

        def animate_border(idx=[0]):
            c = self.rgb_colors[idx[0] % len(self.rgb_colors)]
            self.chat_win.configure(bg=c)
            rgb_frame.configure(bg=c)
            idx[0] += 1
            if self.chat_win.winfo_exists():
                self.chat_win.after(200, lambda: animate_border(idx))
        animate_border()

        header = tk.Frame(inner, bg="#1e1f20")
        header.pack(fill="x")
        tk.Label(header, text="JARVIS", bg="#1e1f20", fg="#e8eaed", font=("Helvetica", 10, "bold")).pack(side="left", padx=12, pady=8)
        tk.Label(header, text="Gemini • JARVIS", bg="#1e1f20", fg="#9aa0a6", font=("Helvetica", 8)).pack(side="right", padx=12)

        msgs = tk.Text(inner, bg="#131314", fg="#e8eaed", wrap="word", state="disabled", bd=0, padx=12, pady=12, font=("Helvetica", 10))
        msgs.pack(fill="both", expand=True)
        msgs.tag_configure("user", background="#8ab4f8", foreground="#202124", lmargin1=80, lmargin2=80, rmargin=8, spacing1=6, spacing3=6)
        msgs.tag_configure("assistant", background="#2d2e30", foreground="#e8eaed", lmargin1=8, lmargin2=8, rmargin=40, spacing1=6, spacing3=6)

        input_frame = tk.Frame(inner, bg="#131314")
        input_frame.pack(fill="x", padx=12, pady=12)
        entry = tk.Entry(input_frame, bg="#1e1f20", fg="#e8eaed", insertbackground="white", bd=0, relief="flat", font=("Helvetica", 11))
        entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0,6))
        entry.focus()

        def voice_listen():
            entry.delete(0, "end")
            entry.insert(0, "Listening...")
            msgs.configure(state="normal")
            msgs.insert("end", "🎤 Listening...\n", "assistant")
            msgs.configure(state="disabled")
            msgs.see("end")
            self.root.update()
            try:
                text = self.agent.voice_tool.listen()
                entry.delete(0, "end")
                if text and "voice listen error" not in text.lower():
                    entry.insert(0, text)
                    send()
                else:
                    entry.delete(0, "end")
                    msgs.configure(state="normal")
                    msgs.insert("end", f"{text}\n", "assistant")
                    msgs.configure(state="disabled")
            except Exception as e:
                entry.delete(0, "end")
                msgs.configure(state="normal")
                msgs.insert("end", f"Voice error: {e}\n", "assistant")
                msgs.configure(state="disabled")

        mic_btn = tk.Button(input_frame, text="🎤", bg="#1e1f20", fg="#8ab4f8", bd=0, font=("Helvetica", 12), width=3, command=voice_listen, activebackground="#2d2e30")
        mic_btn.pack(side="left", padx=(0,6))
        send_btn = tk.Button(input_frame, text="▲", bg="#8ab4f8", fg="#202124", bd=0, font=("Helvetica", 10, "bold"), width=3, command=lambda: send())
        send_btn.pack(side="right")

        def send(event=None):
            text = entry.get().strip()
            if not text or text == "Listening...":
                return
            msgs.configure(state="normal")
            msgs.insert("end", f"{text}\n", "user")
            try:
                reply = self.agent.run(text)
            except Exception as e:
                reply = f"Error: {e}"
            msgs.insert("end", f"{reply}\n", "assistant")
            msgs.configure(state="disabled")
            msgs.see("end")
            entry.delete(0, "end")
            try:
                self.agent.speak(reply)
            except Exception:
                pass

        entry.bind("<Return>", send)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    JarvisBubble().run()
