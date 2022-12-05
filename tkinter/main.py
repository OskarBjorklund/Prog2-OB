import tkinter as tk
from tkinter import messagebox

class MyGui:

    def __init__(self):

        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close without question", command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Brösta äcklig mat", command=self.avoid)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="Blir det Donken?", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()
        self.check_state2 = tk.IntVar()
        self.check_state3 = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text="Brösta äcklig mat", font=("Arial", 12), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.check = tk.Checkbutton(self.root, text="Jag heter William Breander", font=("Arial", 12), variable=self.check_state2)
        self.check.pack(padx=10, pady=10)
        
        self.check = tk.Checkbutton(self.root, text="Jag heter Axel Brandel eller Oscar Wernerus", font=("Arial", 12), variable=self.check_state3)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Uträkna", font=("Arial", 16), command=self.avoid)
        self.button.pack(padx=10, pady=10)

        self.clearbtn = tk.Button(self.root, text="Clear", font=("Arial", 16), command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def avoid(self):
        tmp = self.textbox.get('1.0', tk.END)
        if self.check_state2.get() != 0:
            messagebox.showinfo(title="Message", message="Det blir vatten.")
        elif self.check_state.get() != 0:
            messagebox.showinfo(title="Message", message="Det blir skolmat.")
        elif self.check_state3.get() != 0:
            messagebox.showinfo(title="Message", message="Det blir donken oavsett.")
        else:
            if "sej" in tmp:
                messagebox.showinfo(title="Message", message="Det blir donken.")
            else:
                messagebox.showinfo(title="Message", message="Det blir skolmat.")

    def shortcut(self, event):
        if event.keysym == "Return":
            self.avoid()

    def on_closing(self):
        if messagebox.askyesno(title="Windows message", message="Are you sure you want to quit?"):
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)
MyGui()