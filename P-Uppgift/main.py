import tkinter as tk
import random
from error_handling import read_words_from_file, read_leaderboard, write_leaderboard

def setup_board(words, grid_size):
    num_pairs = grid_size * grid_size // 2
    selected_words = random.sample(words, num_pairs)
    game_values = selected_words * 2
    random.shuffle(game_values)
    return [game_values[i:i+grid_size] for i in range(0, len(game_values), grid_size)]

class MemoryGameUI:
    def __init__(self, root):
        self.root = root
        self.grid_size = 4
        self.root.title("Memory Game")
        self.words = read_words_from_file("memo.txt")
        self.leaderboard = read_leaderboard("highscore.txt")
        self.setup_game()
        self.launch_window()

    def setup_game(self):
        self.board = setup_board(self.words, self.grid_size)
        self.first_card = self.second_card = None
        self.attempts = 0
        self.buttons = [[tk.Button(self.root, text="", width=8, height=2, 
                                   command=lambda x=x, y=y: self.show_value(x, y))
                         for y in range(self.grid_size)] for x in range(self.grid_size)]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.buttons[x][y].grid(row=x, column=y)

    def show_value(self, x, y):
        if self.buttons[x][y]['text']:
            return  # Do nothing if the card is already matched

        if self.first_card is None:
            self.first_card = (x, y)
            self.buttons[x][y].config(text=self.board[x][y])
        elif self.second_card is None and (x, y) != self.first_card:
            self.second_card = (x, y)
            self.buttons[x][y].config(text=self.board[x][y])
            self.attempts += 1
            self.root.after(1000, self.check_match)

    def check_match(self):
        x1, y1 = self.first_card
        x2, y2 = self.second_card
        if self.board[x1][y1] != self.board[x2][y2]:
            self.buttons[x1][y1].config(text="")
            self.buttons[x2][y2].config(text="")
        else:
            if all(button['text'] != '' for row in self.buttons for button in row):
                self.leaderboard.append(self.attempts)
                self.leaderboard.sort()
                write_leaderboard("highscore.txt", self.leaderboard)
                self.show_end_game_window()
                self.root.withdraw()
        self.first_card = self.second_card = None

    def show_end_game_window(self):
        end_game_window = tk.Toplevel(self.root)
        end_game_window.title("Game Over")

        tk.Label(end_game_window, text=f"Your Score: {self.attempts}").pack()
        tk.Label(end_game_window, text="Leaderboard:").pack()

        for i, score in enumerate(self.leaderboard[:5], start=1):
            tk.Label(end_game_window, text=f"{i}. {score}").pack()

        tk.Button(end_game_window, text="Play Again", command=lambda: [end_game_window.destroy(), self.restart_game()]).pack()
        tk.Button(end_game_window, text="Quit Game", command=self.root.destroy).pack()

    def restart_game(self):
        self.setup_game()
        self.root.deiconify()

    def launch_window(self):
        launch_win = tk.Toplevel()
        launch_win.title("Welcome to Memory Game")

        tk.Label(launch_win, text="Leaderboard:").pack()
        for i, score in enumerate(self.leaderboard[:5], start=1):
            tk.Label(launch_win, text=f"{i}. {score}").pack()

        tk.Button(launch_win, text="Play", command=lambda: [launch_win.destroy(), self.root.deiconify()]).pack()
        tk.Button(launch_win, text="Quit", command=self.root.destroy).pack()

        self.root.withdraw()

root = tk.Tk()
game_ui = MemoryGameUI(root)
root.mainloop()