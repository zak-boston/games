import tkinter as tk
from tkinter import ttk
import time

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Timer settings (in seconds)
        self.work_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        
        # State variables
        self.time_left = self.work_time
        self.is_running = False
        self.current_session = "Work"
        self.pomodoro_count = 0
        self.timer_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Session label
        self.session_label = tk.Label(
            self.root, 
            text="Work Session", 
            font=("Arial", 20, "bold"),
            fg="#d32f2f"
        )
        self.session_label.pack(pady=20)
        
        # Timer display
        self.timer_label = tk.Label(
            self.root,
            text="25:00",
            font=("Arial", 48, "bold"),
            fg="#333"
        )
        self.timer_label.pack(pady=10)
        
        # Pomodoro count
        self.count_label = tk.Label(
            self.root,
            text="Pomodoros: 0",
            font=("Arial", 12)
        )
        self.count_label.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Start/Pause button
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.toggle_timer,
            width=10,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            cursor="hand2"
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            width=10,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        self.reset_button.grid(row=0, column=1, padx=5)
        
        # Skip button
        self.skip_button = tk.Button(
            button_frame,
            text="Skip",
            command=self.skip_session,
            width=10,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            cursor="hand2"
        )
        self.skip_button.grid(row=0, column=2, padx=5)
        
    def toggle_timer(self):
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
            
    def start_timer(self):
        self.is_running = True
        self.start_button.config(text="Pause")
        self.countdown()
        
    def pause_timer(self):
        self.is_running = False
        self.start_button.config(text="Resume")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
    def countdown(self):
        if self.is_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.session_complete()
            
    def session_complete(self):
        self.is_running = False
        self.start_button.config(text="Start")
        
        if self.current_session == "Work":
            self.pomodoro_count += 1
            self.count_label.config(text=f"Pomodoros: {self.pomodoro_count}")
            
            if self.pomodoro_count % 4 == 0:
                self.start_break("Long Break", self.long_break)
            else:
                self.start_break("Short Break", self.short_break)
        else:
            self.start_work()
            
    def start_work(self):
        self.current_session = "Work"
        self.time_left = self.work_time
        self.session_label.config(text="Work Session", fg="#d32f2f")
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        
    def start_break(self, break_type, duration):
        self.current_session = break_type
        self.time_left = duration
        self.session_label.config(text=break_type, fg="#388e3c")
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        
    def reset_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.start_button.config(text="Start")
        self.start_work()
        
    def skip_session(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.time_left = 0
        self.session_complete()

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()