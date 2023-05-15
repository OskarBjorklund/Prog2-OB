import socket as sock
import tkinter as tk
import pickle, threading
from tkinter import messagebox, ttk

FONT = ("Arial", 10)	
HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822
FORMAT = "utf-8"


class StartGui:

    def __init__(self, client, socket):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.resizable(width=False, height=False)
        self.root.geometry("{}x{}".format(400, 200))
        self.client = client
        self.socket = socket
        self.login_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def login_gui(self):
        #Login
        self.log_frame = tk.Frame(self.root)

        #Labels
        self.l1 = tk.Label(self.log_frame, text = "Username:", font = FONT)
        self.l2 = tk.Label(self.log_frame, text = "Password:", font = FONT)
        self.l3 = tk.Label(self.log_frame, text = "Don't have an account?", font = FONT)
        self.l4 = tk.Label(self.log_frame, font = FONT)

        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 4, column = 0, sticky = "W", pady = 2)
        self.l4.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2)


        #Textboxes
        self.pass_str = tk.StringVar()

        self.e1 = tk.Entry(self.log_frame, font = FONT)
        self.e2 = tk.Entry(self.log_frame, font = FONT, show = "*", textvariable = self.pass_str)

        self.e1.grid(row = 0, column = 1, pady = 2, sticky = "W")
        self.e2.grid(row = 1, column = 1, pady = 2, sticky = "W")

        #Buttons
        self.btn1 = tk.Button(self.log_frame, text = "Login", font = FONT, command = self.login)
        self.btn2 = tk.Button(self.log_frame, text = "Register", font = FONT, command = lambda: self.hide_interface(True))

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
        self.l1 = tk.Label(self.reg_frame, text = "Username:", font = FONT)
        self.l2 = tk.Label(self.reg_frame, text = "Password:", font = FONT)
        self.l3 = tk.Label(self.reg_frame, text = "Confirm Password:", font = FONT)
        self.l4 = tk.Label(self.reg_frame, text = "Already have an account?", font = FONT)
        self.l5 = tk.Label(self.reg_frame, font = FONT)
        
        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 2, column = 0, sticky = "W", pady = 2)
        self.l4.grid(row = 5, column = 0, sticky = "W", pady = 2)
        self.l5.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2)

        #Textboxes
        self.pass_str = tk.StringVar()
        self.con_pass_str = tk.StringVar()
        
        self.e1 = tk.Entry(self.reg_frame, font = FONT)
        self.e2 = tk.Entry(self.reg_frame, font = FONT, show = "*", textvariable = self.pass_str)
        self.e3 = tk.Entry(self.reg_frame, font = FONT, show = "*", textvariable = self.con_pass_str)

        self.e1.grid(row = 0, column = 1, pady = 2, sticky = "W",)
        self.e2.grid(row = 1, column = 1, pady = 2, sticky = "W",)
        self.e3.grid(row = 2, column = 1, pady = 2, sticky = "W",)

        #Buttons
        self.btn1 = tk.Button(self.reg_frame, text = "Register", font = FONT, command = self.register)
        self.btn2 = tk.Button(self.reg_frame, text = "Login", font = FONT, command = lambda: self.hide_interface(False))

        self.btn1.grid(row = 4, column = 0, pady = 2, columnspan = 2)
        self.btn2.grid(row = 5, column = 1, pady = 2)

        #Checkboxes
        self.pass_int = tk.IntVar(value=0)

        self.c1 = tk.Checkbutton(self.reg_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(False))
        self.c1.grid(row = 1, column = 2, sticky = "W") 

        self.reg_frame.pack()

    def login(self):
        list_str = ("1", self.e1.get(), self.e2.get())
        self.client.send_info(list_str)

        login_info = self.client.recv_info().split("§")

        if login_info[0] == "1":
            self.root.destroy()
            self.forum = ForumGui(self.client, login_info[1], self.socket)
        else:
            self.l4.configure(text = "Invalid login. Check you password.", fg = "red")
    
    def register(self):
        if self.e2.get() != self.e3.get():
            self.l5.configure(text = "Passwords don't match.", fg = "red")
        else:
            list_str = ("0", self.e1.get(), self.e2.get()) #False = New user
            self.client.send_info(list_str)
            
            if self.client.recv_info() == "1": #1 = True, something wrong happend with the registration
                if len(self.e1.get()) < 1: #Username too short.
                    self.l5.configure(text = "Username must atleast be 1 character.", fg = "red")
                elif len(self.e2.get()) < 1: #Password too short.
                    self.l5.configure(text = "Password must atleast be 1 character.", fg = "red")
                else: #Username already in use.
                    self.l5.configure(text = "Username already in use.", fg = "red")
            else:
                self.l5.configure(text = "Account created.", fg = "green")

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
            self.socket.shutdown(sock.SHUT_RDWR)
            self.socket.close()
            self.root.destroy()

class ForumGui:

    def __init__(self, current_user, display_name, socket):
        self.root = tk.Tk()
        self.root.geometry("830x500")
        self.root.resizable(False, False)
        self.root.title("Forum")
        self.current_user = current_user
        self.display_name = display_name
        self.socket = socket

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.start_screen()
        self.start_thread()
        self.root.mainloop()

    def update(self):
        while True:
            posts = convert_str(self.current_user.recv_info())
            self.clear_tree()
            for i in posts[::-1]:
                self.post_tree.insert("", "end", values = i)
                self.post_tree.bind("<Double-1>", self.double_click)
    
    def clear_tree(self):
        for item in self.post_tree.get_children():
            self.post_tree.delete(item)

    def double_click(self, event):
        item = self.post_tree.selection()
        for i in item:
            print("You clicked on", self.post_tree.item(i, "values")[0])
            
    def logout(self):
        self.root.destroy()
        create_client()

    def post(self):
        list_str = (self.display_name, self.title_entry.get(), self.text_entry.get())
        self.current_user.send_info(list_str)

    def start_screen(self):
        self.wrapper = tk.LabelFrame(self.root)
        self.post_list = tk.LabelFrame(self.root)

        self.wrapper.pack(fill = "both", expand = "yes", padx = 10, pady = 10)
        self.post_list.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

        self.username_display = tk.Label(self.wrapper, text = f"Logged in as {self.display_name}", font = FONT)
        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.title_label = tk.Label(self.wrapper, text = "Title:", font = FONT)
        self.text_label = tk.Label(self.wrapper, text = "Message:", font = FONT)
        self.title_entry = tk.Entry(self.wrapper)
        self.text_entry = tk.Entry(self.wrapper)

        self.title_label.place(x = 485, y = 5)
        self.text_label.place(x = 650, y = 5)
        self.title_entry.place(x = 435, y = 35, width = 150)
        self.text_entry.place(x = 595, y = 35, width = 200, height = 100)

        self.post_btn = tk.Button(self.wrapper, font = FONT, text = "Make new post", bg = "lime", fg = "white", command = self.post)
        self.post_btn.place(x = 435, y = 95)

        self.logout_btn = tk.Button(self.wrapper, text = "Logout", command = self.logout)
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.post_tree = ttk.Treeview(self.post_list, columns = (1, 2, 3 ,4), show = "headings", height = "6")
        self.post_tree.pack()

        self.post_tree.heading(1, text = "Title")
        self.post_tree.heading(2, text = "Date")
        self.post_tree.heading(3, text = "Author")
        self.post_tree.heading(4, text = "Answers")

    def post_screen(self, post):
        pass

    def start_thread(self):
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.socket.shutdown(sock.SHUT_RDWR)
            self.socket.close()
            self.root.destroy()

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.connected = True
        
        self.login_gui = StartGui(self, self.socket)
    
    def send_info(self, credentials):
        self.socket.send(("§".join(credentials)).encode(FORMAT))
        
    def recv_info(self):
        while self.connected:
            msg = self.socket.recv(1024).decode(FORMAT)
            return msg
    
def convert_str(recv_str):
    post_list = recv_str.split("§")

    for i, posts in enumerate(post_list):
        post_list[i] = post_list[i].split("¤")
    return post_list

def create_client():
    client = Client()

create_client()