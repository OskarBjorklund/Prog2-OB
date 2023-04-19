import tkinter as tk
from tkinter import messagebox

class MyGui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.resizable(width=False, height=False)
        self.root.geometry("{}x{}".format(300, 150))

        self.login_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def login_gui(self):
        #Login
        self.log_frame = tk.Frame(self.root)

        #Labels
        self.l1 = tk.Label(self.log_frame, text = "Username:", font = ("Arial", 10)).grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2 = tk.Label(self.log_frame, text = "Password:", font = ("Arial", 10)).grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3 = tk.Label(self.log_frame, text = "Invalid login. Check you password.", font = ("Arial", 10),  fg = "red").grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2,)
        self.l4 = tk.Label(self.log_frame, text = "Don't have an account?", font = ("Arial", 10)).grid(row = 4, column = 0, sticky = "W", pady = 2)

        self.log_frame.grid_forget(self.l3)
        #Textboxes
        self.e1 = tk.Entry(self.log_frame, font = ("Arial", 10)).grid(row = 0, column = 1, pady = 2, sticky = "W",)
        self.e2 = tk.Entry(self.log_frame, font = ("Arial", 10)).grid(row = 1, column = 1, pady = 2, sticky = "W",)

        #Buttons
        self.btn1 = tk.Button(self.log_frame, text = "Login", font = ("Arial", 10), command = self.login).grid(row = 2, column = 0, pady = 2, columnspan = 2)
        self.btn2 = tk.Button(self.log_frame, text = "Register", font = ("Arial", 10), command = lambda: self.hide_interface(True)).grid(row = 4, column = 1, pady = 2)

        self.log_frame.pack()

    def register_gui(self):
        #Register
        self.reg_frame = tk.Frame(self.root)

        #Labels
        self.l1 = tk.Label(self.reg_frame, text = "Username:", font = ("Arial", 10)).grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2 = tk.Label(self.reg_frame, text = "Password:", font = ("Arial", 10)).grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3 = tk.Label(self.reg_frame, text = "Confirm Password:", font = ("Arial", 10)).grid(row = 2, column = 0, sticky = "W", pady = 2)
        self.l4 = tk.Label(self.reg_frame, text = "Already have an account?", font = ("Arial", 10)).grid(row = 4, column = 0, sticky = "W", pady = 2)

        #Textboxes
        self.e1 = tk.Entry(self.reg_frame, font = ("Arial", 10)).grid(row = 0, column = 1, pady = 2, sticky = "W",)
        self.e2 = tk.Entry(self.reg_frame, font = ("Arial", 10)).grid(row = 1, column = 1, pady = 2, sticky = "W",)
        self.e3 = tk.Entry(self.reg_frame, font = ("Arial", 10)).grid(row = 2, column = 1, pady = 2, sticky = "W",)

        #Buttons
        self.btn1 = tk.Button(self.reg_frame, text = "Register", font = ("Arial", 10), command = self.login).grid(row = 3, column = 0, pady = 2, columnspan = 2)
        self.btn2 = tk.Button(self.reg_frame, text = "Login", font = ("Arial", 10), command = lambda: self.hide_interface(False)).grid(row = 4, column = 1, pady = 2)

        self.reg_frame.pack()

    def login(self):
        pass

    def register(self):
        pass

    def hide_interface(self, state):
        if state == True:
            self.log_frame.pack_forget()
            print("working")
            self.register_gui()
        else:
            self.reg_frame.pack_forget()
            self.login_gui()

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.root.destroy()


MyGui()