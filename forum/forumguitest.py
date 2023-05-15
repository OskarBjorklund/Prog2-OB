import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

FONT = ("Arial", 15)	
IP = "localhost"
PORT = 8822
FORMAT = "utf-8"

class ForumGui:

    def __init__(self, current_user):
        self.root = tk.Tk()
        self.root.geometry("830x500")
        self.root.resizable(False, False)
        self.root.title("Forum")
        self.current_user = current_user

        self.mydb = mysql.connector.connect(host=IP, user="root", password="", database="forum")
        self.mycursor = self.mydb.cursor()

        self.start_screen()
        self.root.mainloop()

    def update(self, rows):
        for i in rows:
            self.post_tree.insert("", "end", values = i)
        self.post_tree.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        item = self.post_tree.selection()
        for i in item:
            print("You clicked on", self.post_tree.item(i, "values")[0])   

    def post(self):
        pass

    def start_screen(self):
        self.wrapper = tk.LabelFrame(self.root)
        self.post_list = tk.LabelFrame(self.root)

        self.wrapper.pack(fill = "both", expand = "yes", padx = 10, pady = 10)
        self.post_list.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

        self.username_display = tk.Label(self.wrapper, text = f"Logged in as {self.current_user}", font = FONT)
        self.username_display.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.title_label = tk.Label(self.wrapper, text = "Title:", font = FONT)
        self.text_label = tk.Label(self.wrapper, text = "Message:", font = FONT)
        self.title_entry = tk.Entry(self.wrapper)
        self.text_entry = tk.Entry(self.wrapper)

        self.title_label.place(x = 485, y = 5)
        self.text_label.place(x = 650, y = 5)
        self.title_entry.place(x = 435, y = 35, width = 150)
        self.text_entry.place(x = 595, y = 35, width = 200, height = 100)

        self.post_btn = tk.Button(self.wrapper, font = FONT, text = "Make new post", bg = "lime", fg = "white")
        self.post_btn.place(x = 435, y = 95)

        self.logout_btn = tk.Button(self.wrapper, text = "Logout")
        self.logout_btn.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.post_tree = ttk.Treeview(self.post_list, columns = (1, 2, 3 ,4), show = "headings", height = "6")
        self.post_tree.pack()

        self.post_tree.heading(1, text = "Title")
        self.post_tree.heading(2, text = "Date")
        self.post_tree.heading(3, text = "Author")
        self.post_tree.heading(4, text = "Answers")

        self.query = "SELECT title, date_published, author_name, answer_count from post"
        self.mycursor.execute(self.query)
        self.rows = self.mycursor.fetchall()

        print(self.rows)
        post_list = []
        for i, tuples in enumerate(self.rows):
            #Converts tuples to list in order to convert datetime to str
            post_list.append(list(tuples))
            date_convert = post_list[i][1].strftime('%m/%d/%Y')
            post_list[i][1] = date_convert
            post_list[i][3] = str(post_list[i][3])

            post_list[i] = "¤".join(post_list[i])
        
        post_list ="§".join(post_list)

        post_list = post_list.split("§")
        for i, posts in enumerate(post_list):
            post_list[i] = post_list[i].split("¤")

        self.update(post_list)


            


forum = ForumGui("NitroxEnjoyer")