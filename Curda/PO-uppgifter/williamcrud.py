import tkinter as tk
import random

class GridGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("5x5 Grid of Buttons")
        self.buttons = []  # Store buttons in a list

    def button_click(self, row, col):
        clicked_button = self.buttons[row * 5 + col]  # Get the clicked button using its position in the list
        clicked_button.grid_forget()  # Remove the clicked button
        random_number = random.randint(1, 100)  # Generate a random number
        label = tk.Label(self.root, text=str(random_number))
        label.grid(row=row, column=col)  # Display random number in place of the clicked button

    def create_buttons(self):
        for i in range(5):
            for j in range(5):
                button = tk.Button(self.root, text=f"Button {i}-{j}",
                                   command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)  # Add button to the list

def main():
    root = tk.Tk()
    app = GridGUI(root)
    app.create_buttons()
    root.mainloop()

if __name__ == "__main__":
    main()
