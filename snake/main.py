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

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
             direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
             direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
             direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
             direction = new_direction
    

def check_collision(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= game_width:
        return True
    elif y < 0 or y >= game_height:
        return True
    
    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True
    
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="Game over!", fill="red", tag="gameover")



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

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
