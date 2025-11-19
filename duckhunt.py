import tkinter as tk
import random
import math

class Duck:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.size = 40
        self.x = random.randint(50, width - 50)
        self.y = height - 100
        self.speed = random.uniform(2, 4)
        self.angle = random.uniform(30, 150)
        self.vx = self.speed * math.cos(math.radians(self.angle))
        self.vy = -self.speed * math.sin(math.radians(self.angle))
        self.alive = True
        self.hit = False
        self.fall_speed = 0
        
        # Draw duck (simple shape)
        self.body = canvas.create_oval(
            self.x - self.size//2, self.y - self.size//2,
            self.x + self.size//2, self.y + self.size//2,
            fill='brown', outline='black', width=2
        )
        self.head = canvas.create_oval(
            self.x + self.size//4, self.y - self.size//2 - 10,
            self.x + self.size//2 + 5, self.y - self.size//4,
            fill='darkgreen', outline='black', width=2
        )
        self.wing = canvas.create_polygon(
            self.x - self.size//2, self.y,
            self.x - self.size - 10, self.y - 5,
            self.x - self.size//2, self.y + 10,
            fill='brown', outline='black', width=2
        )
        
    def move(self):
        if self.hit:
            # Duck is falling
            self.fall_speed += 0.5
            self.y += self.fall_speed
            if self.y > self.height:
                self.alive = False
        else:
            # Normal flight
            self.x += self.vx
            self.y += self.vy
            
            # Bounce off walls
            if self.x <= self.size or self.x >= self.width - self.size:
                self.vx = -self.vx
            if self.y <= self.size:
                self.vy = -self.vy
                
            # Escape if duck reaches top
            if self.y < -50:
                self.alive = False
        
        # Update duck position
        self.canvas.coords(self.body,
            self.x - self.size//2, self.y - self.size//2,
            self.x + self.size//2, self.y + self.size//2
        )
        self.canvas.coords(self.head,
            self.x + self.size//4, self.y - self.size//2 - 10,
            self.x + self.size//2 + 5, self.y - self.size//4
        )
        self.canvas.coords(self.wing,
            self.x - self.size//2, self.y,
            self.x - self.size - 10, self.y - 5,
            self.x - self.size//2, self.y + 10
        )
        
    def check_hit(self, click_x, click_y):
        # Check if click is within duck's bounds
        distance = math.sqrt((click_x - self.x)**2 + (click_y - self.y)**2)
        if distance <= self.size and not self.hit:
            self.hit = True
            self.canvas.itemconfig(self.body, fill='red')
            return True
        return False
    
    def remove(self):
        self.canvas.delete(self.body)
        self.canvas.delete(self.head)
        self.canvas.delete(self.wing)

class DuckHuntGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Duck Hunt")
        self.width = 800
        self.height = 600
        
        # Game state
        self.score = 0
        self.round = 1
        self.ducks_per_round = 10
        self.ducks_shot = 0
        self.ducks_missed = 0
        self.shots = 3
        self.ducks = []
        self.game_active = False
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='skyblue', cursor='none')
        self.canvas.pack()
        
        # Draw ground
        self.canvas.create_rectangle(0, self.height - 80, self.width, self.height, fill='green', outline='darkgreen')
        self.canvas.create_rectangle(0, self.height - 100, self.width, self.height - 80, fill='brown')
        
        # Score display
        self.score_text = self.canvas.create_text(
            10, 10, text=f"Score: {self.score}", 
            font=('Arial', 16, 'bold'), fill='white', anchor='nw'
        )
        self.round_text = self.canvas.create_text(
            10, 35, text=f"Round: {self.round}", 
            font=('Arial', 14), fill='white', anchor='nw'
        )
        self.shots_text = self.canvas.create_text(
            10, 60, text=f"Shots: {self.shots}", 
            font=('Arial', 14), fill='white', anchor='nw'
        )
        self.duck_text = self.canvas.create_text(
            10, 85, text=f"Ducks: {self.ducks_shot}/{self.ducks_per_round}", 
            font=('Arial', 14), fill='white', anchor='nw'
        )
        
        # Crosshair (cursor)
        self.crosshair_h = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_v = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_circle = self.canvas.create_oval(0, 0, 0, 0, outline='red', width=2)
        
        # Start button
        self.start_button = tk.Button(
            root, text="Start Game", font=('Arial', 16, 'bold'),
            command=self.start_game, bg='orange', fg='white'
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor='center')
        
        # Bind events
        self.canvas.bind('<Motion>', self.update_crosshair)
        self.canvas.bind('<Button-1>', self.shoot)
        
        self.running = True
        self.game_loop()
        
    def update_crosshair(self, event):
        x, y = event.x, event.y
        size = 15
        
        # Update crosshair lines
        self.canvas.coords(self.crosshair_h, x - size, y, x + size, y)
        self.canvas.coords(self.crosshair_v, x, y - size, x, y + size)
        self.canvas.coords(self.crosshair_circle, x - size, y - size, x + size, y + size)
        
    def shoot(self, event):
        if not self.game_active or self.shots <= 0:
            return
            
        self.shots -= 1
        self.update_display()
        
        # Check if any duck was hit
        hit = False
        for duck in self.ducks:
            if not duck.hit and duck.check_hit(event.x, event.y):
                hit = True
                self.score += 100
                self.ducks_shot += 1
                break
        
        # Flash effect
        if hit:
            self.canvas.config(bg='white')
            self.root.after(50, lambda: self.canvas.config(bg='skyblue'))
        
        self.update_display()
        
        # Check if out of shots
        if self.shots <= 0:
            self.end_wave()
    
    def start_game(self):
        self.start_button.place_forget()
        self.game_active = True
        self.spawn_duck()
        
    def spawn_duck(self):
        if len(self.ducks) < 2 and (self.ducks_shot + self.ducks_missed) < self.ducks_per_round:
            duck = Duck(self.canvas, self.width, self.height)
            self.ducks.append(duck)
            self.shots = 3
            self.update_display()
    
    def end_wave(self):
        # Clear all ducks
        for duck in self.ducks:
            duck.remove()
        self.ducks.clear()
        
        # Check progress
        if self.ducks_shot >= self.ducks_per_round * 0.6:  # Need 60% accuracy
            self.round += 1
            self.ducks_shot = 0
            self.ducks_missed = 0
            self.game_active = True
            self.root.after(1000, self.spawn_duck)
        else:
            self.game_over()
        
        self.update_display()
    
    def game_over(self):
        self.game_active = False
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Game Over!\nFinal Score: {self.score}",
            font=('Arial', 32, 'bold'), fill='red'
        )
        self.start_button.config(text="Play Again", command=self.reset_game)
        self.start_button.place(relx=0.5, rely=0.6, anchor='center')
    
    def reset_game(self):
        self.score = 0
        self.round = 1
        self.ducks_shot = 0
        self.ducks_missed = 0
        self.shots = 3
        for duck in self.ducks:
            duck.remove()
        self.ducks.clear()
        self.canvas.delete('all')
        
        # Redraw static elements
        self.canvas.create_rectangle(0, self.height - 80, self.width, self.height, fill='green', outline='darkgreen')
        self.canvas.create_rectangle(0, self.height - 100, self.width, self.height - 80, fill='brown')
        
        self.score_text = self.canvas.create_text(10, 10, text=f"Score: {self.score}", font=('Arial', 16, 'bold'), fill='white', anchor='nw')
        self.round_text = self.canvas.create_text(10, 35, text=f"Round: {self.round}", font=('Arial', 14), fill='white', anchor='nw')
        self.shots_text = self.canvas.create_text(10, 60, text=f"Shots: {self.shots}", font=('Arial', 14), fill='white', anchor='nw')
        self.duck_text = self.canvas.create_text(10, 85, text=f"Ducks: {self.ducks_shot}/{self.ducks_per_round}", font=('Arial', 14), fill='white', anchor='nw')
        
        self.crosshair_h = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_v = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_circle = self.canvas.create_oval(0, 0, 0, 0, outline='red', width=2)
        
        self.start_game()
    
    def update_display(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.round_text, text=f"Round: {self.round}")
        self.canvas.itemconfig(self.shots_text, text=f"Shots: {self.shots}")
        self.canvas.itemconfig(self.duck_text, text=f"Ducks: {self.ducks_shot}/{self.ducks_per_round}")
    
    def game_loop(self):
        if self.game_active:
            # Move all ducks
            for duck in self.ducks[:]:
                duck.move()
                if not duck.alive:
                    if not duck.hit:
                        self.ducks_missed += 1
                    duck.remove()
                    self.ducks.remove(duck)
                    
                    # Spawn next duck if available
                    if (self.ducks_shot + self.ducks_missed) < self.ducks_per_round:
                        self.spawn_duck()
                    elif len(self.ducks) == 0:
                        self.end_wave()
            
            self.update_display()
        
        if self.running:
            self.root.after(30, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = DuckHuntGame(root)
    root.mainloop()