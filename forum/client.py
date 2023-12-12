# Imports
import socket as sock
import tkinter as tk
import pickle
from tkinter import messagebox, ttk

# Constants
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

        # Startar login_gui
        self.login_gui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def login_gui(self):
        """
        Login GUI that places everything in self.log_frame within a grid
        """

        # Login
        self.log_frame = tk.Frame(self.root)

        # Labels
        self.username_label = tk.Label(self.log_frame, text = "Username:", font = FONT)
        self.password_label = tk.Label(self.log_frame, text = "Password:", font = FONT)
        self.no_account_label = tk.Label(self.log_frame, text = "Don't have an account?", font = FONT)
        self.error_message_label = tk.Label(self.log_frame, font = FONT)

        # Label grid placement
        self.username_label.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.password_label.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.no_account_label.grid(row = 4, column = 0, sticky = "W", pady = 2)
        self.error_message_label.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2)

        # Entries
        self.pass_str = tk.StringVar()

        self.username_entry = tk.Entry(self.log_frame, font = FONT)
        self.password_entry = tk.Entry(self.log_frame, font = FONT, show = "*", textvariable = self.pass_str)

        # Entry grid placement
        self.username_entry.grid(row = 0, column = 1, pady = 2, sticky = "W")
        self.password_entry.grid(row = 1, column = 1, pady = 2, sticky = "W")

        # Buttons
        self.login_btn = tk.Button(self.log_frame, text = "Login", font = FONT, command = self.login)
        self.register_btn = tk.Button(self.log_frame, text = "Register", font = FONT, command = lambda: self.switch_interface(True))

        # Button grid placement
        self.login_btn.grid(row = 2, column = 0, pady = 2, columnspan = 2)
        self.register_btn.grid(row = 4, column = 1, pady = 2)

        # Checkboxes
        self.pass_int = tk.IntVar(value=0)
        self.show_login_password = tk.Checkbutton(self.log_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(True))
        self.show_login_password.grid(row = 1, column = 2, sticky = "W") 

        # Packing the login frame
        self.log_frame.pack()

    def register_gui(self):
        """
        Registration gui that places everything in self.reg_frame within a grid.
        """
        # Register
        self.reg_frame = tk.Frame(self.root)

        # Labels
        self.username_label = tk.Label(self.reg_frame, text = "Username:", font = FONT)
        self.password_label = tk.Label(self.reg_frame, text = "Password:", font = FONT)
        self.no_account_label = tk.Label(self.reg_frame, text = "Confirm Password:", font = FONT)
        self.error_message_label = tk.Label(self.reg_frame, font = FONT)
        self.account_exists = tk.Label(self.reg_frame, text = "Already have an account?", font = FONT)
        
        # Label grid placement
        self.username_label.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.password_label.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.no_account_label.grid(row = 2, column = 0, sticky = "W", pady = 2)
        self.error_message_label.grid(row = 3, column = 0, sticky = "W", pady = 2, columnspan = 2)
        self.account_exists.grid(row = 5, column = 0, sticky = "W", pady = 2)

        # Entries
        self.pass_str = tk.StringVar()
        self.con_pass_str = tk.StringVar()
        
        self.username_entry = tk.Entry(self.reg_frame, font = FONT)
        self.password_entry = tk.Entry(self.reg_frame, font = FONT, show = "*", textvariable = self.pass_str)
        self.confirm_password_entry = tk.Entry(self.reg_frame, font = FONT, show = "*", textvariable = self.con_pass_str)

        # Entry grid placement
        self.username_entry.grid(row = 0, column = 1, pady = 2, sticky = "W",)
        self.password_entry.grid(row = 1, column = 1, pady = 2, sticky = "W",)
        self.confirm_password_entry.grid(row = 2, column = 1, pady = 2, sticky = "W",)

        # Buttons
        self.login_btn = tk.Button(self.reg_frame, text = "Register", font = FONT, command = self.register)
        self.register_btn = tk.Button(self.reg_frame, text = "Login", font = FONT, command = lambda: self.switch_interface(False))

        # Button grid placement
        self.login_btn.grid(row = 4, column = 0, pady = 2, columnspan = 2)
        self.register_btn.grid(row = 5, column = 1, pady = 2)

        # Checkboxes
        self.pass_int = tk.IntVar(value=0)

        self.show_login_password = tk.Checkbutton(self.reg_frame, onvalue = 1, offvalue = 0, variable = self.pass_int, command = lambda: self.pass_show(False))
        self.show_login_password.grid(row = 1, column = 2, sticky = "W") 

        # Packing the registration frame
        self.reg_frame.pack()

    def login(self):
        """
        The method that takes care of logins. The login information will
        be sent to the server for the server to validate. If the input is correct
        the server will allow you to login to that account.
        """
        # Sends the login information to the server with argument "1" meaning user is trying to log in
        self.client.send_info(["1", self.username_entry.get(), self.password_entry.get()]) # 1 = True, new user

        # Client waits for the server to accept or decline the login information
        login_info = self.client.recv_info().split("§")

        # If the server accepts your login information, the client will recieve a "1"
        if login_info[0] == "1":
            # Root is destroyed and a forum object is created with login_gui's attributes as arguments
            # + login_info[1] which is the username
            self.root.destroy()
            self.forum = ForumGui(self.client, login_info[1], self.socket)
        else:
            # If client recieves "0", invalid login
            self.error_message_label.configure(text = "Invalid login. Check you password.", fg = "red")
    
    def register(self):
        """
        The method that takes care of the registration process. All information
        from the register GUI is sent to the server for confirmation. If the registration
        is successfull the server will tell the client everything went through and
        then the client can login.
        """
        # Check if password and confirm password is equal or not
        if self.password_entry.get() != self.confirm_password_entry.get():
            self.error_message_label.configure(text = "Passwords don't match.", fg = "red")
        else:
            # Sends the login information to the server with argument "0" meaning user is trying to register
            self.client.send_info(["0", self.username_entry.get(), self.password_entry.get()])
            
            if self.client.recv_info() == "1": # 1 = True, something wrong happend with the registration
                if len(self.username_entry.get()) < 1: # Username too short.
                    self.error_message_label.configure(text = "Username must atleast be 1 character.", fg = "red")
                elif len(self.password_entry.get()) < 1: # Password too short.
                    self.error_message_label.configure(text = "Password must atleast be 1 character.", fg = "red")
                else: # Username already in use.
                    self.error_message_label.configure(text = "Username already in use.", fg = "red")
            else:
                # Nothing went wrong, account created
                self.error_message_label.configure(text = "Account created.", fg = "green")
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
                self.confirm_password_entry.delete(0, "end")

    def pass_show(self, state):
        """
        Depending on which argument (state) the method is called with, 
        the method hides or shows the password. The state parameter is
        specified from a checkbutton.
        """
        if state == True:
            self.password_entry.config(show="*"*(not self.pass_int.get()))
        else:
            self.password_entry.config(show="*"*(not self.pass_int.get()))
            self.confirm_password_entry.config(show="*"*(not self.pass_int.get()))

    def switch_interface(self, state):
        """
        method that forgets the packed frames and calls the other method.
        This is depending on which interface is currently in use.
        """
        if state == True:
            self.log_frame.pack_forget()
            self.register_gui()
        else:
            self.reg_frame.pack_forget()
            self.login_gui()

    def on_closing(self):
        """
        When the exit button is pressed a window message will pop up
        asking the user to confirm their action.
        """
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
        """
        This method tells the server that it wants to receive
        the most recent list of posts from the database.
        A message is received from the server and it could either be
        a "0" (no posts exists), or a long string containing the information
        of the posts. If the recieved information contains the string of posts,
        the treeview tree will first be cleared and then created again with the
        new string of posts. The string of posts must be converted from a string
        to a nested list which is done with convert_str.
        """
        self.current_user.send_info(["4"]) # "4" = Client wants to recieve a list of posts
        posts = self.current_user.recv_info()
        if posts != "0":
            self.clear_tree(self.post_tree)
            self.insert_tree(self.post_tree, convert_str(posts), True)
        else:
            self.clear_tree(self.post_tree)

    def update_comment_list(self, post):
        """
        This method tells the server that it wants to receive
        the most recent list of comments to a specefic post from the database.
        A message is received from the server and it could either be
        a "0" (no comments exists), or a long string containing the information
        of the comments. If the recieved information contains the string of comments
        the treeview tree will first be cleared and then created again with the
        new string of comments. The string of comments must be converted from a string
        to a nested list which is done with convert_str.
        """
        self.current_user.send_info(["6", post]) # which post comments are connected to
        comments = self.current_user.recv_info()
        if comments != "0":
            self.clear_tree(self.comment_tree)
            self.insert_tree(self.comment_tree, convert_str(comments), False)
        else:
            self.clear_tree(self.comment_tree)

    def insert_tree(self, tree, children, accessible):
        """
        This method inserts children into specified tree, either post_tree och comment_tree.
        If accesible is True, the double_click method is binded to each children.
        """
        # Inserts comments or posts into selected tree. Accessible grants double_click ability.
        for i in children[::-1]:
            tree.insert("", "end", values = i)
            if accessible == True:
                tree.bind("<Double-1>", self.double_click)
    
    def clear_tree(self, tree):
        """
        Removes all children of specific tree
        """
        for item in tree.get_children():
            tree.delete(item)

    def double_click(self, event):
        """
        Calls switch_interface if selected post is pressed again
        """
        item = self.post_tree.selection()
        for i in item:
            self.switch_interface(True, self.post_tree.item(i, "values")[0])
            
    def logout(self):   
        """
        Destroys root and creates new client object
        """
        self.root.destroy()
        create_client()

    def post(self):
        """
        This method handles new post requests. Firstly, it checks if the input is valid.
        If everything goes right the client will send their entry inputs and their name to the server.
        If the title is not already occupied, the post will successfully be published.
        """
        if len(self.title_entry.get()) > 0 and len(self.title_entry.get()) < 30 and len(self.post_text.get("1.0", "end")) > 1:
            self.current_user.send_info(["2", self.display_name, self.title_entry.get(), self.post_text.get("1.0", "end")])

            if self.current_user.recv_info() == "1": # True, post already exists
                self.post_error.configure(text = "Title already exists")
            else:
                self.post_error.configure(text = "") # Clears error message

        else:
            self.post_error.configure(text = "Title or text too long or short")

        self.title_entry.delete(0, "end")
        self.post_text.delete("1.0", "end")
        self.update_post_list_frame()

    def comment(self, post):
        """
        This method functions similarly as the post method. First it validates the user input, 
        then it sends the input, username and post to the server for it to be uploaded to the 
        database.
        """
        if len(self.comment_text.get("1.0", "end")) > 1 and len(self.comment_text.get("1.0", "end")) < 125:
            self.current_user.send_info(["5", self.display_name, self.comment_text.get("1.0", "end"), post])
            self.comment_error.configure(text = "")
        else:
            self.comment_error.configure(text = "Text too short or long")

        self.comment_text.delete("1.0", "end")
        self.update_comment_list(post)
    
    def update_post_text(self, post):
        """
        This method gathers the correct text for corresponding post from the server 
        and inserts it into an immutable text widget.
        """
        self.post_text.configure(state="normal") # Enables post_text to be changed

        self.current_user.send_info(["3", post])
        text = convert_str(self.current_user.recv_info())

        self.post_text.insert(tk.END, text[1][0])
        self.post_text.configure(state="disabled") # Makes post_text immutable

    def switch_interface(self, state, post):
        """
        Works exactly like switch_interface in the login class but has two LabelFrames
        that needs to be forgotten.
        """
        if state == True: # True = In startscreen
            self.wrapper.forget()
            self.post_list_frame.forget()
            self.post_screen(post)
        else: # False, in postscreen
            self.post_frame.forget()
            self.comment_frame.forget()
            self.start_screen()

    def on_closing(self):
        """
        A windows message pops up if the client wants to close the gui, asking them if they are
        sure to quit. If they quit, the socket will close and root be destroyed.
        """
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.socket.shutdown(sock.SHUT_RDWR)
            self.socket.close()
            self.root.destroy()

    def start_screen(self):
        """
        method that takes care of the graphical part of the forum GUI. Everything is
        placed in the top part, the wrapper, and the post list is placed in the
        post_list_frame.
        """
        # Frames
        self.wrapper = tk.LabelFrame(self.root)
        self.post_list_frame = tk.LabelFrame(self.root)

        # Packing frames
        self.wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
        self.post_list_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        # User preview
        self.username_display = tk.Label(self.wrapper, text = f"Logged in as {self.display_name}", font = FONT)
        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.logout_btn = tk.Button(self.wrapper, text = "Logout",font = FONT, command = self.logout)
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)

        # New post
        self.title_label = tk.Label(self.wrapper, text = "Title:", font = FONT)
        self.text_label = tk.Label(self.wrapper, text = "Message:", font = FONT)
        self.title_entry = tk.Entry(self.wrapper, font = FONT)
        self.post_text = tk.Text(self.wrapper, font = FONT, wrap = "word")
        self.post_error = tk.Label(self.wrapper, font = FONT, fg = "red")
        self.post_btn = tk.Button(self.wrapper, font = FONT, text = "Make new post", bg = "lime", fg = "white", command = self.post)

        # Packing new post
        self.title_label.place(x = 485, y = 5)
        self.text_label.place(x = 650, y = 5)
        self.title_entry.place(x = 435, y = 35, width = 150)
        self.post_text.place(x = 595, y = 35, width = 200, height = 100)
        self.post_error.place(x = 425, y = 65)
        self.post_btn.place(x = 435, y = 95)

        # Refresh
        self.post_refresh_btn = tk.Button(self.wrapper, font = FONT, text = "Refresh", command = self.update_post_list_frame)
        self.post_refresh_btn.place(x = 15, y = 200)

        # Prevent automatic resizing
        self.post_list_frame.pack_propagate(0) 

        # Treeview with headings, title, date, author and answers
        self.post_tree = ttk.Treeview(self.post_list_frame)
        self.post_tree["columns"] = ("Title", "Date", "Author", "Answers")

        self.post_tree.column("# 0", width=0, stretch=tk.NO)  # Set width to 0 to make it invisible
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
        style.configure("Treeview.Cell", wraplength=100)  # Wrap lenght, same width as title

        row_height = 75

        self.post_tree.configure(style = "Custom.Treeview")
        style.configure("Custom.Treeview", rowheight = row_height)

        self.post_tree.pack(fill = "both", expand = "yes")

        # Updates post list as soon as startscreen is called
        self.update_post_list_frame()

    def post_screen(self, post):
        """
        Graphical part of the forum GUI that displays selected posts. Just as
        the start_screen, post_screen is also built by two LabelFrame widgets,
        post_frame and comment_frame. The post_frame displays the post title and text, 
        it also has a section where the client can make a comment. The comment_frame
        has a treeview widget that lists the comments on the connected post.
        """
        # Frames
        self.post_frame = tk.LabelFrame(self.root)
        self.comment_frame = tk.LabelFrame(self.root)

        # Packing the frames
        self.post_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)
        self.comment_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)

        # User preview
        self.username_display = tk.Label(self.post_frame, text = f"Logged in as {self.display_name}", font = FONT)
        self.logout_btn = tk.Button(self.post_frame, text = "Logout", font = FONT, command = self.logout)
        self.back_btn = tk.Button(self.post_frame, text = "Back", font = FONT, command = lambda: self.switch_interface(False, None))

        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.back_btn.grid(row = 0, column = 2, padx = 5, pady = 5)

        # Post Preview
        self.post_title = tk.Label(self.post_frame, text = post, font = ("arial", 15))
        self.post_text = tk.Text(self.post_frame, font = FONT, state = "disabled", wrap = "word")
        
        self.post_title.place(x = 415-(len(post)*5), y = 20) # Centers the label
        self.post_text.place(x = 265, y = 50, width = 300, height = 175)

        # Make comment
        self.comment_text = tk.Text(self.post_frame, font = FONT, wrap = "word")
        self.post_comment_btn = tk.Button(self.post_frame, font = FONT, text = "Comment", bg = "lime", fg = "white", command = lambda: self.comment(post))
        self.comment_error = tk.Label(self.post_frame, font = FONT, fg = "red")
        
        self.comment_text.place(x = 580, y = 50, width = 215, height = 135)
        self.post_comment_btn.place(x = 580, y = 200)
        self.comment_error.place(x = 650, y = 200)

        # Refresh
        self.comment_refresh_btn = tk.Button(self.post_frame, font = FONT, text = "Refresh", command = lambda: self.update_comment_list(post))
        self.comment_refresh_btn.place(x = 15, y = 200)

        self.comment_frame.pack_propagate(0)  # Prevent automatic resizing

        # Tree with comments, user and date as headings
        self.comment_tree = ttk.Treeview(self.comment_frame)
        self.comment_tree["columns"] = ("Comment", "User", "Date")

        self.comment_tree.column("# 0", width=0, stretch=tk.NO)  # Set width to 0 to make it invisible
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
        style.configure("Treeview.Cell", wraplength=200)  # Wraplenght same width as comment

        row_height = 75

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
        
        self.login_gui = StartGui(self, self.socket)
    
    def send_info(self, info):
        """
        method takes a list as argument joins it using the "§" symbol.
        This is then sent to the server using the format utf-8
        """
        self.socket.send(("§".join(info)).encode(FORMAT))
        
    def recv_info(self):
        """
        method returns a recieved string from the server
        """
        return self.socket.recv(1024).decode(FORMAT)
        
    
def convert_str(recv_str):
    """
    When post_list or comment_list is recieved from the server, it is
    recieved as a string that needs to be converted to its original
    format (nested list). The "§" seperates the outer lists, such as post 1, post 2...
    The "¤" seperates the inner lists, such as title, date, user, answer_count...
    After the string is converted to its original format it is returned.
    """
    recv_list = recv_str.split("§")

    for i, posts in enumerate(recv_list):
        recv_list[i] = recv_list[i].split("¤")
    return recv_list

def create_client():
    client = Client()

create_client()