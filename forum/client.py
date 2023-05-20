import socket as sock
import tkinter as tk
import pickle
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
        self.btn2 = tk.Button(self.log_frame, text = "Register", font = FONT, command = lambda: self.switch_interface(True))

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
        self.btn2 = tk.Button(self.reg_frame, text = "Login", font = FONT, command = lambda: self.switch_interface(False))

        self.btn1.grid(row = 4, column = 0, pady = 2, columnspan = 2)
        self.btn2.grid(row = 5, column = 1, pady = 2)

        #Checkboxes
        self.pass_int = tk.IntVar(value=0)

        self.c1 = tk.Checkbutton(self.reg_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(False))
        self.c1.grid(row = 1, column = 2, sticky = "W") 

        self.reg_frame.pack()

    def login(self):
        self.client.send_info(["1", self.e1.get(), self.e2.get()]) #1 = True, new user

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
            self.client.send_info(["0", self.e1.get(), self.e2.get()]) #False = New user
            
            if self.client.recv_info() == "1": #1 = True, something wrong happend with the registration
                if len(self.e1.get()) < 1: #Username too short.
                    self.l5.configure(text = "Username must atleast be 1 character.", fg = "red")
                elif len(self.e2.get()) < 1: #Password too short.
                    self.l5.configure(text = "Password must atleast be 1 character.", fg = "red")
                else: #Username already in use.
                    self.l5.configure(text = "Username already in use.", fg = "red")
            else:
                self.l5.configure(text = "Account created.", fg = "green")
                self.e1.delete(0, "end")
                self.e2.delete(0, "end")
                self.e3.delete(0, "end")

    def pass_show(self, state):
            if state == True:
                self.e2.config(show="*"*(not self.pass_int.get()))
            else:
                self.e2.config(show="*"*(not self.pass_int.get()))
                self.e3.config(show="*"*(not self.pass_int.get()))

    def switch_interface(self, state):
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
        self.root.mainloop()

    def update_post_list_frame(self):
        self.current_user.send_info(["4"])
        posts = self.current_user.recv_info()
        if posts != "0":
            self.clear_tree(self.post_tree)
            self.create_tree(self.post_tree, convert_str(posts), True)
        else:
            self.clear_tree(self.post_tree)

    def update_comment_list(self, post):
        self.current_user.send_info(["6", post])
        comments = self.current_user.recv_info()
        if comments != "0":
            self.clear_tree(self.comment_tree)
            self.create_tree(self.comment_tree, convert_str(comments), False)
        else:
            self.clear_tree(self.comment_tree)

    def create_tree(self, tree, branches, accesible):
        #Inserts comments or posts into selected tree. Accisible grants double_click ability.
        for i in branches[::-1]:
            tree.insert("", "end", values = i)
            if accesible == True:
                tree.bind("<Double-1>", self.double_click)
    
    def clear_tree(self, tree):
        #Removes all items in a tree
        for item in tree.get_children():
            tree.delete(item)

    def double_click(self, event):
        #Calls switch_interface if selected post is pressed again
        item = self.post_tree.selection()
        for i in item:
            self.switch_interface(True, self.post_tree.item(i, "values")[0])
            
    def logout(self):
        #Destroys root and goes back to login window
        self.root.destroy()
        create_client()

    def post(self):
        if len(self.title_entry.get()) > 0 and len(self.title_entry.get()) < 30 and len(self.post_text.get("1.0", "end")) > 1:
            self.current_user.send_info(["2", self.display_name, self.title_entry.get(), self.post_text.get("1.0", "end")])
            if self.current_user.recv_info() == "1": #True, post already exists
                print("Occipid")
                self.post_error.configure(text = "Title already exists")
            else:
                print("GOOD")
                self.post_error.configure(text = "")
        else:
            self.post_error.configure(text = "Title or text too long or short")
        self.title_entry.delete(0, "end")
        self.post_text.delete("1.0", "end")
        self.update_post_list_frame()

    def comment(self, post):
        if len(self.comment_text.get("1.0", "end")) > 1 and len(self.comment_text.get("1.0", "end")) < 125:
            self.current_user.send_info(["5", self.display_name, self.comment_text.get("1.0", "end"), post])
            self.comment_error.configure(text = "")
        else:
            self.comment_error.configure(text = "Text too short or long")
        self.comment_text.delete("1.0", "end")
        self.update_comment_list(post)
    
    def update_post_text(self, title):
        self.post_text.configure(state="normal")
        self.current_user.send_info(["3", title])
        text = convert_str(self.current_user.recv_info())
        self.post_text.insert(tk.END, text[1][0])
        self.post_text.configure(state="disabled")

    def switch_interface(self, state, post):
        if state == True: #True = In startscreen
            self.wrapper.forget()
            self.post_list_frame.forget()
            self.post_screen(post)
        else: #False, in postscreen
            self.post_frame.forget()
            self.comment_frame.forget()
            self.start_screen()

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.socket.shutdown(sock.SHUT_RDWR)
            self.socket.close()
            self.root.destroy()

    def start_screen(self):
        #Frames
        self.wrapper = tk.LabelFrame(self.root)
        self.post_list_frame = tk.LabelFrame(self.root)

        self.wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
        self.post_list_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        #User preview
        self.username_display = tk.Label(self.wrapper, text = f"Logged in as {self.display_name}", font = FONT)
        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.logout_btn = tk.Button(self.wrapper, text = "Logout",font = FONT, command = self.logout)
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)

        #New post
        self.title_label = tk.Label(self.wrapper, text = "Title:", font = FONT)
        self.text_label = tk.Label(self.wrapper, text = "Message:", font = FONT)
        self.title_entry = tk.Entry(self.wrapper, font = FONT)
        self.post_text = tk.Text(self.wrapper, font = FONT, wrap = "word")
        self.post_error = tk.Label(self.wrapper, font = FONT, fg = "red")

        self.title_label.place(x = 485, y = 5)
        self.text_label.place(x = 650, y = 5)
        self.title_entry.place(x = 435, y = 35, width = 150)
        self.post_text.place(x = 595, y = 35, width = 200, height = 100)
        self.post_error.place(x = 425, y = 65)

        self.post_btn = tk.Button(self.wrapper, font = FONT, text = "Make new post", bg = "lime", fg = "white", command = self.post)
        self.post_btn.place(x = 435, y = 95)

        #Refresh
        self.post_refresh_btn = tk.Button(self.wrapper, font = FONT, text = "Refresh", command = self.update_post_list_frame)
        self.post_refresh_btn.place(x = 15, y = 135)

        #Prevent automatic resizing
        self.post_list_frame.pack_propagate(0) 

        #List of previewed posts
        self.post_tree = ttk.Treeview(self.post_list_frame)
        self.post_tree["columns"] = ("Title", "Date", "Author", "Answers")

        self.post_tree.column("#0", width=0, stretch=tk.NO)  #Set width to 0 to make it invisible
        self.post_tree.column("Title", width=100)
        self.post_tree.column("Date", width=100)
        self.post_tree.column("Author", width=100)
        self.post_tree.column("Answers", width=100)

        self.post_tree.heading("Title", text="Title")
        self.post_tree.heading("Date", text="Date")
        self.post_tree.heading("Author", text="Author")
        self.post_tree.heading("Answers", text="Answers")

        self.post_tree["displaycolumns"] = ("Title", "Date", "Author", "Answers")

        style = ttk.Style()
        style.configure("Treeview", fieldbackground="white")
        style.configure("Treeview.Heading", font = FONT)
        style.configure("Treeview.Cell", wraplength=100)  #Adjust the wrap length here

        row_height = 75  #Adjust the row height here

        self.post_tree.configure(style="Custom.Treeview")
        style.configure("Custom.Treeview", rowheight=row_height)

        self.post_tree.pack(fill="both", expand="yes")

        self.update_post_list_frame()

    def post_screen(self, post):
        #Frames
        self.post_frame = tk.LabelFrame(self.root)
        self.comment_frame = tk.LabelFrame(self.root)

        self.post_frame.pack(fill="both", expand="yes", padx=10, pady=10)
        self.comment_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        #User preview
        self.username_display = tk.Label(self.post_frame, text = f"Logged in as {self.display_name}", font = FONT)
        self.logout_btn = tk.Button(self.post_frame, text = "Logout", font = FONT, command = self.logout)
        self.back_btn = tk.Button(self.post_frame, text = "Back", font = FONT, command = lambda: self.switch_interface(False, None))

        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.back_btn.grid(row = 0, column = 2, padx = 5, pady = 5)

        #Post Preview
        self.post_title = tk.Label(self.post_frame, text = post, font = ("arial", 15))
        self.post_text = tk.Text(self.post_frame, font = FONT, state = "disabled", wrap = "word")
        
        self.post_title.place(x = 415-(len(post)*5), y = 20)
        self.post_text.place(x = 265, y = 50, width = 300, height = 110)

        #Make comment
        self.comment_text = tk.Text(self.post_frame, font = FONT, wrap = "word")
        self.post_comment_btn = tk.Button(self.post_frame, font = FONT, text = "Comment", bg = "lime", fg = "white", command = lambda: self.comment(post))
        self.comment_error = tk.Label(self.post_frame, font = FONT, fg = "red")
        
        self.comment_text.place(x = 580, y = 50, width = 215, height = 70)
        self.post_comment_btn.place(x = 580, y = 135)
        self.comment_error.place(x = 650, y = 135)

        #Refresh
        self.comment_refresh_btn = tk.Button(self.post_frame, font = FONT, text = "Refresh", command = lambda: self.update_comment_list(post))
        self.comment_refresh_btn.place(x = 15, y = 135)

        self.comment_frame.pack_propagate(0)  #Prevent automatic resizing

        #Tree with comments
        self.comment_tree = ttk.Treeview(self.comment_frame)
        self.comment_tree["columns"] = ("Comment", "User", "Date")

        self.comment_tree.column("#0", width=0, stretch=tk.NO)  #Set width to 0 to make it invisible
        self.comment_tree.column("Comment", width=200)
        self.comment_tree.column("User", width=100)
        self.comment_tree.column("Date", width=100)

        self.comment_tree.heading("Comment", text="Comment")
        self.comment_tree.heading("User", text="User")
        self.comment_tree.heading("Date", text="Date")

        self.comment_tree["displaycolumns"] = ("Comment", "User", "Date")

        style = ttk.Style()
        style.configure("Treeview", fieldbackground="white")
        style.configure("Treeview.Heading", font = FONT)
        style.configure("Treeview.Cell", wraplength=200)  #Adjust the wrap length here

        row_height = 75  #Adjust the row height here

        self.comment_tree.configure(style="Custom.Treeview")
        style.configure("Custom.Treeview", rowheight=row_height)

        self.comment_tree.pack(fill="both", expand="yes")

        self.update_post_text(post)
        self.update_comment_list(post)
        

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.connected = True
        
        self.login_gui = StartGui(self, self.socket)
    
    def send_info(self, info):
        self.socket.send(("§".join(info)).encode(FORMAT))
        
    def recv_info(self):
        msg = self.socket.recv(1024).decode(FORMAT)
        return msg
    
def convert_str(recv_str):
    post_list_frame = recv_str.split("§")

    for i, posts in enumerate(post_list_frame):
        post_list_frame[i] = post_list_frame[i].split("¤")
    return post_list_frame

def create_client():
    client = Client()

create_client()