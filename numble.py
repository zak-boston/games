import tkinter as tk
from tkinter import messagebox
import random


class NumbleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Numble")
        self.root.geometry("550x750")
        self.root.configure(bg="#c6f6d5")  # Light green background
        
        # Game state
        self.digit_count = 4
        self.par_score = 7
        self.target_number = ""
        self.guess_history = []
        self.game_over = False
        self.game_won = False
        self.show_symbol_positions = False
        self.allow_repeating_digits = False
        
        # Game modes
        self.difficulty_mode = "standard"  # easy, standard, hard
        self.speed_mode = False
        self.timer_seconds = 30
        self.timer_running = False
        self.timer_id = None
        
        # Stats
        self.stats = {
            'games_played': 0,
            'games_won': 0,
            'current_streak': 0,
            'best_streak': 0,
            'total_guesses': 0,
            'best_score': float('inf')
        }
        
        # Load stats if available
        self.load_stats()
        
        self.setup_ui()
        self.reset_game()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Numble", 
            font=("Arial", 32, "bold"),
            bg="#c6f6d5",
            fg="#22543d"
        )
        title_label.pack(pady=15)
        
        # Game mode selection frame
        mode_frame = tk.Frame(self.root, bg="#9ae6b4", bd=2, relief=tk.RIDGE)
        mode_frame.pack(padx=20, pady=5, fill=tk.X)
        
        tk.Label(
            mode_frame,
            text="Game Mode:",
            font=("Arial", 10, "bold"),
            bg="#9ae6b4",
            fg="#22543d"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.difficulty_var = tk.StringVar(value="standard")
        difficulties = [("Easy", "easy"), ("Standard", "standard"), ("Hard", "hard")]
        for i, (text, value) in enumerate(difficulties):
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                command=self.change_difficulty_mode,
                font=("Arial", 9),
                bg="#9ae6b4",
                fg="#22543d",
                selectcolor="#c6f6d5",
                activebackground="#9ae6b4"
            ).grid(row=0, column=i+1, padx=5, pady=5)
        
        # Speed mode checkbox
        self.speed_var = tk.BooleanVar()
        tk.Checkbutton(
            mode_frame,
            text="Speed Mode (30s)",
            variable=self.speed_var,
            command=self.toggle_speed_mode,
            font=("Arial", 9),
            bg="#9ae6b4",
            fg="#22543d",
            selectcolor="#c6f6d5",
            activebackground="#9ae6b4"
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Repeating digits checkbox
        self.repeating_var = tk.BooleanVar()
        tk.Checkbutton(
            mode_frame,
            text="Allow Repeating Digits",
            variable=self.repeating_var,
            command=self.toggle_repeating_digits,
            font=("Arial", 9),
            bg="#9ae6b4",
            fg="#22543d",
            selectcolor="#c6f6d5",
            activebackground="#9ae6b4"
        ).grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Timer display (only visible in speed mode)
        self.timer_frame = tk.Frame(self.root, bg="#c6f6d5")
        self.timer_label = tk.Label(
            self.timer_frame,
            text="Time: 30s",
            font=("Arial", 16, "bold"),
            bg="#c6f6d5",
            fg="#22543d"
        )
        self.timer_label.pack()
        
        # Instructions frame
        instructions_frame = tk.Frame(self.root, bg="#9ae6b4", bd=2, relief=tk.RIDGE)
        instructions_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.instructions_text = tk.Label(
            instructions_frame,
            text="",
            font=("Arial", 10),
            bg="#9ae6b4",
            fg="#22543d",
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        self.instructions_text.pack()
        self.update_instructions()
        
        # Symbol position checkbox
        checkbox_frame = tk.Frame(self.root, bg="#c6f6d5")
        checkbox_frame.pack(pady=5)
        
        self.show_positions_var = tk.BooleanVar()
        self.position_checkbox = tk.Checkbutton(
            checkbox_frame,
            text="Show symbol positions",
            variable=self.show_positions_var,
            command=self.toggle_symbol_positions,
            font=("Arial", 10),
            bg="#c6f6d5",
            fg="#22543d",
            selectcolor="#9ae6b4",
            activebackground="#c6f6d5",
            cursor="hand2"
        )
        self.position_checkbox.pack()
        
        # Difficulty controls
        difficulty_frame = tk.Frame(self.root, bg="#c6f6d5")
        difficulty_frame.pack(pady=10)
        
        tk.Button(
            difficulty_frame,
            text="-",
            command=self.decrease_difficulty,
            font=("Arial", 12, "bold"),
            bg="#2f855a",
            fg="white",
            width=3,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_label = tk.Label(
            difficulty_frame,
            text=f"{self.digit_count} digits",
            font=("Arial", 12),
            bg="#c6f6d5",
            fg="#22543d"
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            difficulty_frame,
            text="+",
            command=self.increase_difficulty,
            font=("Arial", 12, "bold"),
            bg="#2f855a",
            fg="white",
            width=3,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#c6f6d5")
        input_frame.pack(pady=20)
        
        self.entry = tk.Entry(
            input_frame,
            font=("Courier", 18),
            width=15,
            justify=tk.CENTER
        )
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda e: self.check_guess())
        self.entry.bind('<KeyRelease>', self.on_entry_change)
        
        self.guess_button = tk.Button(
            input_frame,
            text="Guess",
            command=self.check_guess,
            font=("Arial", 12, "bold"),
            bg="#2f855a",
            fg="white",
            width=8,
            cursor="hand2"
        )
        self.guess_button.pack(side=tk.LEFT, padx=5)
        
        # Error label
        self.error_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg="#c6f6d5",
            fg="red"
        )
        self.error_label.pack()
        
        # Game result frame
        self.result_frame = tk.Frame(self.root, bg="#c6f6d5")
        self.result_frame.pack(pady=10)
        
        # Guess history frame
        history_label = tk.Label(
            self.root,
            text="Your Guesses:",
            font=("Arial", 14, "bold"),
            bg="#c6f6d5",
            fg="#22543d"
        )
        history_label.pack(pady=(20, 5))
        
        # Scrollable history
        history_container = tk.Frame(self.root, bg="#c6f6d5")
        history_container.pack(padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            history_container,
            font=("Courier", 12),
            bg="#2f855a",
            fg="white",
            state=tk.DISABLED,
            height=8,
            yscrollcommand=scrollbar.set
        )
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Stats button
        tk.Button(
            self.root,
            text="View Stats",
            command=self.show_stats,
            font=("Arial", 10),
            bg="#2f855a",
            fg="white",
            cursor="hand2"
        ).pack(pady=10)
    
    def generate_target_number(self):
        if self.allow_repeating_digits:
            # Allow any digits including repeats
            return ''.join(str(random.randint(0, 9)) for _ in range(self.digit_count))
        else:
            # No repeating digits
            digits = list(range(10))
            random.shuffle(digits)
            return ''.join(map(str, digits[:self.digit_count]))
    
    def reset_game(self):
        self.stop_timer()
        self.target_number = self.generate_target_number()
        self.guess_history = []
        self.game_over = False
        self.game_won = False
        self.timer_seconds = 30
        self.entry.delete(0, tk.END)
        self.error_label.config(text="")
        
        # Clear result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Clear history
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "No guesses yet...\n")
        self.history_text.config(state=tk.DISABLED)
        
        self.entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        
        if self.speed_mode:
            self.start_timer()
        
        print(f"Debug - Target number: {self.target_number}")
    
    def change_difficulty_mode(self):
        self.difficulty_mode = self.difficulty_var.get()
        self.update_instructions()
        self.update_history_display()
        
        # Update position checkbox visibility
        if self.difficulty_mode == "hard":
            self.position_checkbox.config(state=tk.DISABLED)
            self.show_positions_var.set(False)
            self.show_symbol_positions = False
        else:
            self.position_checkbox.config(state=tk.NORMAL)
    
    def toggle_speed_mode(self):
        self.speed_mode = self.speed_var.get()
        if self.speed_mode:
            self.timer_frame.pack(before=self.root.winfo_children()[2], pady=10)
            if not self.game_over:
                self.start_timer()
        else:
            self.timer_frame.pack_forget()
            self.stop_timer()
    
    def toggle_repeating_digits(self):
        self.allow_repeating_digits = self.repeating_var.get()
        self.update_instructions()
        self.reset_game()
    
    def start_timer(self):
        if not self.timer_running and not self.game_over:
            self.timer_running = True
            self.update_timer()
    
    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def update_timer(self):
        if not self.timer_running or self.game_over:
            return
        
        if self.timer_seconds > 0:
            self.timer_label.config(text=f"Time: {self.timer_seconds}s")
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            # Time's up! Auto-submit current guess
            self.check_guess()
    
    def on_entry_change(self, event):
        # Reset timer when user types (only in speed mode)
        if self.speed_mode and not self.game_over:
            self.stop_timer()
            self.timer_seconds = 30
            self.start_timer()
    
    def check_guess(self):
        if self.game_over:
            return
        
        guess = self.entry.get().strip()
        
        # Validate guess
        if len(guess) != self.digit_count:
            self.error_label.config(text=f"Please enter exactly {self.digit_count} digits.")
            if self.speed_mode:
                self.timer_seconds = 30  # Reset timer on error
            return
        
        if not guess.isdigit():
            self.error_label.config(text="Please enter only numbers.")
            if self.speed_mode:
                self.timer_seconds = 30  # Reset timer on error
            return
        
        if not self.allow_repeating_digits and len(set(guess)) != len(guess):
            self.error_label.config(text="Your guess cannot contain repeated digits.")
            if self.speed_mode:
                self.timer_seconds = 30  # Reset timer on error
            return
        
        # Clear error
        self.error_label.config(text="")
        
        # Calculate feedback based on mode
        feedback_result = self.calculate_feedback(guess)
        
        # Add to history
        self.guess_history.append(feedback_result)
        
        # Update history display
        self.update_history_display()
        
        # Clear entry and reset timer
        self.entry.delete(0, tk.END)
        if self.speed_mode:
            self.timer_seconds = 30
        
        # Check if won
        if feedback_result['correct_positions'] == self.digit_count:
            self.game_won = True
            self.game_over = True
            self.stop_timer()
            self.update_stats(len(self.guess_history))
            self.show_win_screen()
    
    def calculate_feedback(self, guess):
        """Calculate feedback based on current game mode and settings"""
        correct_positions = 0
        position_feedback = [''] * self.digit_count
        
        if self.allow_repeating_digits:
            # With repeating digits: match each target digit to exactly one guess digit
            target_list = list(self.target_number)
            guess_list = list(guess)
            matched_target = [False] * self.digit_count
            matched_guess = [False] * self.digit_count
            
            # First pass: exact matches
            for i in range(self.digit_count):
                if guess_list[i] == target_list[i]:
                    correct_positions += 1
                    position_feedback[i] = '🔒'
                    matched_target[i] = True
                    matched_guess[i] = True
            
            # Second pass: wrong position matches
            correct_digits = 0
            for i in range(self.digit_count):
                if not matched_guess[i]:
                    for j in range(self.digit_count):
                        if not matched_target[j] and guess_list[i] == target_list[j]:
                            correct_digits += 1
                            position_feedback[i] = '🔓'
                            matched_target[j] = True
                            break
        else:
            # Without repeating digits: simpler logic
            correct_digits = 0
            for i in range(self.digit_count):
                if guess[i] == self.target_number[i]:
                    correct_positions += 1
                    position_feedback[i] = '🔒'
                elif guess[i] in self.target_number:
                    correct_digits += 1
                    position_feedback[i] = '🔓'
        
        # Create feedback string based on difficulty mode
        if self.difficulty_mode == "hard":
            feedback = str(correct_positions)
        elif self.difficulty_mode == "easy":
            feedback = ''.join(position_feedback)
            # Fill empty positions with underscore
            feedback = ' '.join(position_feedback[i] if position_feedback[i] else '_' for i in range(self.digit_count))
        else:  # standard
            feedback = "🔒" * correct_positions + "🔓" * correct_digits
            if not feedback:
                feedback = "No matches"
        
        return {
            'guess': guess,
            'feedback': feedback,
            'position_feedback': position_feedback,
            'correct_positions': correct_positions
        }
    
    def update_history_display(self):
        """Re-render all history entries based on current display mode"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for i, item in enumerate(self.guess_history, 1):
            # Recalculate display based on current mode settings
            if self.difficulty_mode == "easy":
                # Easy mode always shows positions
                display = ' '.join(item['position_feedback'][j] if item['position_feedback'][j] else '_' 
                                  for j in range(self.digit_count))
                self.history_text.insert(tk.END, f"{i}. {item['guess']}  →  {display}\n")
            elif self.difficulty_mode == "hard":
                # Hard mode only shows count - recalculate from position_feedback
                correct_count = sum(1 for symbol in item['position_feedback'] if symbol == '🔒')
                self.history_text.insert(tk.END, f"{i}. {item['guess']}  →  {correct_count}\n")
            elif self.show_symbol_positions:
                # Standard mode with position display
                position_display = ' '.join(item['position_feedback'][j] if item['position_feedback'][j] else '·' 
                                           for j in range(self.digit_count))
                self.history_text.insert(tk.END, f"{i}. {item['guess']}  →  {position_display}\n")
            else:
                # Standard mode without position display - recalculate sorted symbols
                locks = sum(1 for symbol in item['position_feedback'] if symbol == '🔒')
                unlocks = sum(1 for symbol in item['position_feedback'] if symbol == '🔓')
                sorted_feedback = "🔒" * locks + "🔓" * unlocks
                if not sorted_feedback:
                    sorted_feedback = "No matches"
                self.history_text.insert(tk.END, f"{i}. {item['guess']}  →  {sorted_feedback}\n")
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)
    
    def show_win_screen(self):
        self.entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        
        # Clear result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Win message
        tk.Label(
            self.result_frame,
            text="You Win! 🎉",
            font=("Arial", 20, "bold"),
            bg="#c6f6d5",
            fg="#22543d"
        ).pack()
        
        # Score message
        score_msg = self.get_score_message(len(self.guess_history))
        tk.Label(
            self.result_frame,
            text=score_msg,
            font=("Arial", 12),
            bg="#c6f6d5",
            fg="#22543d"
        ).pack()
        
        # Play again button
        tk.Button(
            self.result_frame,
            text="Play Again",
            command=self.reset_game,
            font=("Arial", 12, "bold"),
            bg="#2f855a",
            fg="white",
            cursor="hand2"
        ).pack(pady=10)
    
    def get_score_message(self, guess_count):
        diff = guess_count - self.par_score
        
        if diff <= -4:
            term = "Albatross+"
        elif diff == -3:
            term = "Eagle"
        elif diff == -2:
            term = "Double Birdie"
        elif diff == -1:
            term = "Birdie"
        elif diff == 0:
            term = "Par"
        elif diff == 1:
            term = "Bogey"
        elif diff == 2:
            term = "Double Bogey"
        else:
            term = "Triple+ Bogey"
        
        return f"Solved in {guess_count} guesses ({term})"
    
    def update_stats(self, guess_count):
        self.stats['games_played'] += 1
        self.stats['games_won'] += 1
        self.stats['current_streak'] += 1
        self.stats['best_streak'] = max(self.stats['current_streak'], self.stats['best_streak'])
        self.stats['total_guesses'] += guess_count
        self.stats['best_score'] = min(self.stats['best_score'], guess_count)
    
    def show_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Your Stats")
        stats_window.geometry("350x300")
        stats_window.configure(bg="#9ae6b4")
        
        tk.Label(
            stats_window,
            text="Your Stats",
            font=("Arial", 18, "bold"),
            bg="#9ae6b4",
            fg="#22543d"
        ).pack(pady=15)
        
        stats_frame = tk.Frame(stats_window, bg="#9ae6b4")
        stats_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        stats_to_show = [
            ("Games Played", self.stats['games_played']),
            ("Games Won", self.stats['games_won']),
            ("Win %", f"{round((self.stats['games_won'] / self.stats['games_played'] * 100) if self.stats['games_played'] > 0 else 0)}%"),
            ("Current Streak", self.stats['current_streak']),
            ("Best Streak", self.stats['best_streak']),
            ("Avg. Guesses", f"{self.stats['total_guesses'] / self.stats['games_won']:.1f}" if self.stats['games_won'] > 0 else "-"),
            ("Best Score", self.stats['best_score'] if self.stats['best_score'] < float('inf') else "-")
        ]
        
        for i, (label, value) in enumerate(stats_to_show):
            row = i // 2
            col = i % 2
            
            stat_box = tk.Frame(stats_frame, bg="#c6f6d5", bd=2, relief=tk.RIDGE)
            stat_box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            tk.Label(
                stat_box,
                text=label,
                font=("Arial", 9),
                bg="#c6f6d5",
                fg="#4a5568"
            ).pack(pady=(5, 0))
            
            tk.Label(
                stat_box,
                text=str(value),
                font=("Arial", 16, "bold"),
                bg="#c6f6d5",
                fg="#22543d"
            ).pack(pady=(0, 5))
        
        for i in range(2):
            stats_frame.columnconfigure(i, weight=1)
        
        tk.Button(
            stats_window,
            text="Close",
            command=stats_window.destroy,
            font=("Arial", 10, "bold"),
            bg="#2f855a",
            fg="white",
            cursor="hand2"
        ).pack(pady=10)
    
    def increase_difficulty(self):
        if self.digit_count < 6:
            self.digit_count += 1
            self.difficulty_label.config(text=f"{self.digit_count} digits")
            self.update_instructions()
            self.reset_game()
    
    def decrease_difficulty(self):
        if self.digit_count > 3:
            self.digit_count -= 1
            self.difficulty_label.config(text=f"{self.digit_count} digits")
            self.update_instructions()
            self.reset_game()
    
    def update_instructions(self):
        repeat_text = "with" if not self.allow_repeating_digits else "allowing"
        
        if self.difficulty_mode == "easy":
            mode_text = "• Position of each symbol is shown directly"
        elif self.difficulty_mode == "hard":
            mode_text = "• Only shows count of correct positions (no symbols)"
        else:
            mode_text = "• 🔒 = correct digit in correct position\n• 🔓 = correct digit in wrong position"
        
        instructions = f"""How to play:
• Guess the {self.digit_count}-digit number {repeat_text} repeating digits
{mode_text}
• Par score is {self.par_score} guesses"""
        
        self.instructions_text.config(text=instructions)
    
    def toggle_symbol_positions(self):
        self.show_symbol_positions = self.show_positions_var.get()
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    game = NumbleGame(root)
    root.mainloop()