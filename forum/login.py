import tkinter as tk
from tkinter import messagebox

font = ("Arial", 10)	

class StartGui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.resizable(width=False, height=False)
        self.root.geometry("{}x{}".format(400, 200))

        self.login_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def login_gui(self):
        #Login
        self.log_frame = tk.Frame(self.root)

        #Labels
        self.l1 = tk.Label(self.log_frame, text = "Username:", font = font)
        self.l2 = tk.Label(self.log_frame, text = "Password:", font = font)
        self.l3 = tk.Label(self.log_frame, text = "Don't have an account?", font = font)

        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 4, column = 0, sticky = "W", pady = 2)

        #Textboxes
        self.pass_str = tk.StringVar()

        self.e1 = tk.Entry(self.log_frame, font = font)
        self.e2 = tk.Entry(self.log_frame, font = font, show = "*", textvariable = self.pass_str)

        self.e1.grid(row = 0, column = 1, pady = 2, sticky = "W")
        self.e2.grid(row = 1, column = 1, pady = 2, sticky = "W")

        #Buttons
        self.btn1 = tk.Button(self.log_frame, text = "Login", font = font, command = self.login)
        self.btn2 = tk.Button(self.log_frame, text = "Register", font = font, command = lambda: self.hide_interface(True))

        self.btn1.grid(row = 2, column = 0, pady = 2, columnspan = 2)
        self.btn2.grid(row = 4, column = 1, pady = 2)

        #Checkboxes
        self.pass_int = tk.IntVar(value=0)
        self.c1 = tk.Checkbutton(self.log_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(True))
        self.c1.grid(row = 1, column = 2, sticky = "W") 

        self.log_frame.pack()

    def register_gui(self):
        #Register
        self.reg_frame = tk.Frame(self.root)

        #Labels
        self.l1 = tk.Label(self.reg_frame, text = "Username:", font = font)
        self.l2 = tk.Label(self.reg_frame, text = "Password:", font = font)
        self.l3 = tk.Label(self.reg_frame, text = "Confirm Password:", font = font)
        self.l4 = tk.Label(self.reg_frame, text = "Already have an account?", font = font)

        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 2, column = 0, sticky = "W", pady = 2)
        self.l4.grid(row = 5, column = 0, sticky = "W", pady = 2)

        #Textboxes
        self.pass_str = tk.StringVar()
        self.con_pass_str = tk.StringVar()
        
        self.e1 = tk.Entry(self.reg_frame, font = font)
        self.e2 = tk.Entry(self.reg_frame, font = font, show = "*", textvariable = self.pass_str)
        self.e3 = tk.Entry(self.reg_frame, font = font, show = "*", textvariable = self.con_pass_str)

        self.e1.grid(row = 0, column = 1, pady = 2, sticky = "W",)
        self.e2.grid(row = 1, column = 1, pady = 2, sticky = "W",)
        self.e3.grid(row = 2, column = 1, pady = 2, sticky = "W",)

        #Buttons
        self.btn1 = tk.Button(self.reg_frame, text = "Register", font = font, command = self.register)
        self.btn2 = tk.Button(self.reg_frame, text = "Login", font = font, command = lambda: self.hide_interface(False))

        self.btn1.grid(row = 4, column = 0, pady = 2, columnspan = 2)
        self.btn2.grid(row = 5, column = 1, pady = 2)

        #Checkboxes
        self.pass_int = tk.IntVar(value=0)

        self.c1 = tk.Checkbutton(self.reg_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(False))
        self.c1.grid(row = 1, column = 2, sticky = "W") 

        self.reg_frame.pack()

    def login(self):
        self.l4 = tk.Label(self.log_frame, text = "Invalid login. Check you password.", font = font,  fg = "red")
        self.l4.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2,)

    def register(self):
        if self.e2.get() != self.e3.get():
            self.l5 = tk.Label(self.reg_frame, text = "Passwords don't match.", font = font,  fg = "red")
            self.l5.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2)

    def pass_show(self, state):
            if state == True:
                self.e2.config(show="*"*(not self.pass_int.get()))
            else:
                self.e2.config(show="*"*(not self.pass_int.get()))
                self.e3.config(show="*"*(not self.pass_int.get()))

    def hide_interface(self, state):
        if state == True:
            self.log_frame.pack_forget()
            self.register_gui()
        else:
            self.reg_frame.pack_forget()
            self.login_gui()

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.root.destroy()

StartGui()