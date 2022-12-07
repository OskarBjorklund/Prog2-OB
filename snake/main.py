from tkinter import *
import random

game_width = 500
game_height = 500
speed = 50
space_size = 20
body_parts = 3
snake_color = "#00FF00"
food_color = "#FF0000"
background_color = "#000000"

class Snake:
    
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0 ])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (game_width/space_size)-1) * space_size
        y = random.randint(0, (game_height/space_size)-1) * space_size

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tag="food")

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= space_size
    elif direction == "down":
        y += space_size
    elif direction == "left":
        x -= space_size
    elif direction == "right":
        x += space_size

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)

    window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    pass

def check_collision():
    pass

def game_over():
    pass

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=background_color, width=game_width, height=game_height)
canvas.pack()

window.update()

window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()

window.mainloop()
