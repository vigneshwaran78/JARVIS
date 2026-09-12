from __future__ import annotations

import tkinter as tk

from jarvis.agent import JarvisAgent


class JarvisBubble:
    def __init__(self) -> None:
        self.agent = JarvisAgent()
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("60x60+1600+800")
        self.root.configure(bg="#1a1a2e")

        self.bubble = tk.Button(
            self.root,
            text="J",
            font=("Helvetica", 20, "bold"),
            bg="#7c3aed",
            fg="white",
            bd=0,
            activebackground="#6d28d9",
            command=self.toggle_chat,
        )
        self.bubble.pack(fill="both", expand=True)

        self.bubble.bind("<Button-1>", lambda e: self.toggle_chat())
        self.bubble.bind("<B1-Motion>", self.drag)
        self.chat_win: tk.Toplevel | None = None

    def drag(self, event: tk.Event) -> None:
        self.root.geometry(f"+{event.x_root-30}+{event.y_root-30}")

    def toggle_chat(self) -> None:
        if self.chat_win and self.chat_win.winfo_exists():
            self.chat_win.destroy()
            self.chat_win = None
            return
        self.chat_win = tk.Toplevel(self.root)
        self.chat_win.title("JARVIS")
        self.chat_win.geometry("360x460+1240+400")
        self.chat_win.configure(bg="#1a1a2e")
        self.chat_win.attributes("-topmost", True)

        msgs = tk.Text(self.chat_win, bg="#1a1a2e", fg="white", wrap="word", state="disabled")
        msgs.pack(fill="both", expand=True, padx=8, pady=8)

        entry = tk.Entry(self.chat_win, bg="#0f0f1e", fg="white", insertbackground="white")
        entry.pack(fill="x", padx=8, pady=8)
        entry.focus()

        def send(event=None):
            text = entry.get().strip()
            if not text:
                return
            msgs.configure(state="normal")
            msgs.insert("end", f"You: {text}\n")
            try:
                reply = self.agent.run(text)
            except Exception as e:
                reply = f"Error: {e}"
            msgs.insert("end", f"JARVIS: {reply}\n\n")
            msgs.configure(state="disabled")
            msgs.see("end")
            entry.delete(0, "end")

        entry.bind("<Return>", send)
        tk.Button(self.chat_win, text="Send", bg="#7c3aed", fg="white", bd=0, command=send).pack(pady=4)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    JarvisBubble().run()
