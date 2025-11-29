# typing_test.py
# A fun & useful typing speed test - perfect for your Tkinter toybox

import tkinter as tk
from tkinter import ttk
import random
import time

# Sample texts (you can add hundreds more or load from a file)
with open('sample_texts.txt','r', errors='ignore') as f:
    SAMPLE_TEXTS = f.readlines()

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.time_left = 60
        self.start_time = None
        self.timer_running = False

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_widgets()
        self.new_test()

    def create_widgets(self):
        # Header
        title = tk.Label(self.root, text="Typing Speed Test", font=("Helvetica", 28, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=(20, 10))

        # Sample text display
        self.sample_label = tk.Label(
            self.root,
            text="",
            font=("Consolas", 18),
            bg="#ffffff",
            fg="#333",
            wraplength=750,
            justify="left",
            relief="solid",
            borderwidth=2,
            padx=15,
            pady=15,
        )
        self.sample_label.pack(pady=10)

        # Entry
        self.entry = tk.Text(
            self.root,
            font=("Consolas", 18),
            height=6,
            wrap="word",
            undo=True,
            relief="solid",
            borderwidth=2,
        )
        self.entry.pack(padx=50, pady=10)
        self.entry.focus()

        # Stats
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=10)

        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", font=("Helvetica", 16), bg="#f0f0f0")
        self.wpm_label.pack(side="left", padx=20)

        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 100%", font=("Helvetica", 16), bg="#f0f0f0")
        self.accuracy_label.pack(side="left", padx=20)

        self.time_label = tk.Label(stats_frame, text="Time: 60s", font=("Helvetica", 16), bg="#f0f0f0", fg="red")
        self.time_label.pack(side="left", padx=20)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        self.start_btn = ttk.Button(btn_frame, text="Start / Reset", command=self.new_test)
        self.start_btn.pack(side="left", padx=10)

        # Bind events
        self.entry.bind("<KeyRelease>", self.on_type)

    def new_test(self):
        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.sample_label.config(text=self.sample_text)

        self.entry.delete("1.0", "end")
        self.entry.config(state="normal")

        self.time_left = 60
        self.timer_running = False
        self.start_time = None

        self.time_label.config(text="Time: 60s", fg="red")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")

        # Highlighting reset
        self.sample_label.config(fg="#333")
        self.entry.focus()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left = 60 - int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {max(0, self.time_left)}s")
            if self.time_left <= 0:
                self.end_test()
            else:
                self.root.after(1000, self.update_timer)

    def on_type(self, event=None):
        if not self.timer_running and len(self.entry.get("1.0", "end").strip()) > 0:
            self.start_timer()

        typed = self.entry.get("1.0", "end-1c")
        self.update_highlighting(typed)
        self.update_stats(typed)

        # End test if sample is fully typed correctly
        if typed == self.sample_text:
            self.end_test()

    def update_highlighting(self, typed):
        self.sample_label.tag_remove("correct", "1.0", "end")
        self.sample_label.tag_remove("wrong", "1.0", "end")

        for i, char in enumerate(typed):
            if i < len(self.sample_text) and char == self.sample_text[i]:
                self.sample_label.tag_add("correct", f"1.{i}", f"1.{i+1}")
            elif i < len(self.sample_text):
                self.sample_label.tag_add("wrong", f"1.{i}", f"1.{i+1}")

        self.sample_label.tag_config("correct", foreground="#2e8b57")
        self.sample_label.tag_config("wrong", foreground="#e74c3c", underline=True)

    def update_stats(self, typed):
        if self.start_time is None:
            return

        elapsed = max(time.time() - self.start_time, 0.01)
        words_typed = len(typed.split())
        wpm = int((words_typed / elapsed) * 60)

        # Accuracy
        correct_chars = sum(1 for i, c in enumerate(typed) if i < len(self.sample_text) and c == self.sample_text[i])
        accuracy = (correct_chars / len(typed) * 100) if typed else 100

        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")

    def end_test(self):
        self.timer_running = False
        self.entry.config(state="disabled")
        self.time_label.config(text="Time's up!", fg="#e74c3c")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()