import tkinter as tk
from tkinter import ttk

class ForumGui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.title("Forum")
        self.start_screen()
        self.root.mainloop()

    def start_screen(self):
        self.wrapper1 = tk.LabelFrame(self.root)
        self.wrapper2 = tk.LabelFrame(self.root)

        self.mycanvas = tk.Canvas(self.wrapper2)
        self.mycanvas.pack(side=tk.LEFT, fill = "y")

        self.scrollbar = ttk.Scrollbar(self.wrapper2, orient="vertical", command = self.mycanvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.mycanvas.configure(yscrollcommand = self.scrollbar.set)
            
        self.mycanvas.bind("<Configure>", lambda e: self.mycanvas.configure(scrollregion=self.mycanvas.bbox('all')))

        self.scroll_frame = tk.Frame(self.mycanvas)
        self.scroll_list()
        self.mycanvas.create_window((0,0), window = self.scroll_frame, anchor = "nw")

        self.wrapper1.pack(fill="both", expand="yes", padx=10, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)

    def scroll_list(self):
        for i in range(50):
            tk.Button(self.scroll_frame, text = "thoy - "+str(i)).pack()



forum = ForumGui()