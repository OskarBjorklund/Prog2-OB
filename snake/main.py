import tkinter as tk
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
speed = 100
space_size = 20
body_parts = 3
food_color = "#FF0000"
background_color = "#000000"

class Snake:
    
    def __init__(self, pos, color):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []
        self.vel = complex(0, 1)
        self.color = color

        for i in range(0, body_parts):
            self.coordinates.append(pos)
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=self.color, tag="snake")
            self.squares.append(square)
    
    def check_collision(self):
        x, y = self.coordinates[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        
        if self.coordinates[0] in self.coordinates[1:]:
            return True

        return False

    def change_velocity(self, new_vel: complex):
        if self.vel + new_vel:
            self.vel = new_vel

    def next_frame(self, canvas):
        c = complex(*self.coordinates[0]) + self.vel * space_size
        x, y = c.real, c.imag

        self.coordinates.insert(0, (x, y))

        square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=self.color)

        self.squares.insert(0, square)

    def move_end(self, canvas):
        self.coordinates.pop()
        canvas.delete(self.squares.pop())

class Food:

    def __init__(self):
        self.new()

    def new(self):
        self.coordinates = [
            random.randint(0, (GAME_WIDTH/space_size)-1) * space_size,
            random.randint(0, (GAME_HEIGHT/space_size)-1) * space_size
        ]
        x, y = self.coordinates
        canvas.delete("food")
        canvas.create_oval(x, y, x+space_size, y+space_size, fill=food_color, tag="food")

def next_turn():
    snake1.next_frame(canvas)
    snake2.next_frame(canvas)

    if snake1.coordinates[0] in snake2.coordinates:
        game_over("snake1")
        return

    elif snake2.coordinates[0] in snake1.coordinates:
        game_over("snake2")
        return

    if tuple(food.coordinates) == snake1.coordinates[0]:
        snake1_string_var.set(f"Blue: {len(snake1.coordinates)}")
        food.new()
    else:
        snake1.move_end(canvas)
    
    if tuple(food.coordinates) == snake2.coordinates[0]:
        snake2_string_var.set(f"Green: {len(snake2.coordinates)}")
        food.new()
    else:
        snake2.move_end(canvas)

    if snake1.check_collision():
        game_over("snake1")
    elif snake2.check_collision():
        game_over("snake2")
    else:
        window.after(speed, next_turn)

def change_direction(snake, new_vel):
    snake.change_velocity(new_vel)
    
def game_over(winner):
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 50), text="Game over!", fill="red", tag="gameover")
    start.grid(row=0, column=1)
    
    global snake1, snake2, food
    
    if winner == "snake2":
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 70, font=('consolas', 50), text="Blue won!", fill="blue", tag="gameover")
    elif winner == "snake1":
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 70, font=('consolas', 50), text="Green won!", fill="green", tag="gameover")
        
    snake1 = Snake([0, 0], "blue")
    snake2 = Snake([GAME_WIDTH-space_size, 0], "green")
    food = Food()

def start_game(*args):
    start.grid_forget()
    snake1_string_var.set(f"Blue: {snake1.body_size}")
    snake2_string_var.set(f"Green: {snake2.body_size}")
    canvas.delete("gameover")
    next_turn()

window = tk.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tk.Canvas(window, bg=background_color, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.grid(row=1, column=0, columnspan=3)

window.update()

window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height+y}+{x}+{y}")

snake1 = Snake([0, 0], "blue")
snake2 = Snake([GAME_WIDTH-space_size, 0], "green")
food = Food()

snake1_string_var = tk.StringVar()
snake2_string_var = tk.StringVar()

snake1_score_label = tk.Label(window, textvariable=snake1_string_var, font=("consolas", 20))
snake1_score_label.grid(row=0, column=0)
snake2_score_label = tk.Label(window, textvariable=snake2_string_var, font=("consolas", 20))
snake2_score_label.grid(row=0, column=2)
start = tk.Button(text="Start", font=("consolas", 20), command=start_game)
start.grid(row=0, column=1)

window.bind('<Left>', lambda event: change_direction(snake2, -1))
window.bind('<Right>', lambda event: change_direction(snake2, 1))
window.bind('<Up>', lambda event: change_direction(snake2, -1j))
window.bind('<Down>', lambda event: change_direction(snake2, 1j))

window.bind('a', lambda event: change_direction(snake1, -1))
window.bind('d', lambda event: change_direction(snake1, 1))
window.bind('w', lambda event: change_direction(snake1, -1j))
window.bind('s', lambda event: change_direction(snake1, 1j))

window.mainloop()