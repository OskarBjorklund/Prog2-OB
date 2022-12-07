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

        

class Food:

    def __init__(self):

        x = random.randint(0, (game_width/space_size)-1) * space_size
        y = random.randint(0, (game_height/space_size)-1) * space_size

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tag="food")

def next_turn():
    pass

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
