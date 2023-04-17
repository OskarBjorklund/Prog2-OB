import tkinter as tk
from tkinter import messagebox

class MyGui:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Login')

        #Login

        #Labels
        self.l1 = tk.Label(self.root, text = "Username:", font = ("Arial", 10))
        self.l2 = tk.Label(self.root, text = "Password:", font = ("Arial", 10))
        self.l3 = tk.Label(self.root, text = "Invalid login. Check you password.", font = ("Arial", 10),  fg = "red")
        self.l4 = tk.Label(self.root, text = "Don't have an account?", font = ("Arial", 10))

        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2,)
        self.l4.grid(row = 4, column = 0, sticky = "W", pady = 2)

        #Textboxes
        self.e1 = tk.Entry(self.root, font = ("Arial", 10))
        self.e2 = tk.Entry(self.root, font = ("Arial", 10))

        self.e1.grid(row = 0, column = 1, pady = 2)
        self.e2.grid(row = 1, column = 1, pady = 2)

        #Buttons
        self.btn1 = tk.Button(self.root, text = "Login", font = ("Arial", 10), command=self.login)
        self.btn2 = tk.Button(self.root, text = "Register", font = ("Arial", 10), command=self.register)

        self.btn1.grid(row = 2, column = 0, pady = 2, columnspan = 2)
        self.btn2.grid(row = 4, column = 1, pady = 2)



        #Register

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def login(self):
        pass
        #Invalid login

    def register(self):
        pass

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.root.destroy()


MyGui()