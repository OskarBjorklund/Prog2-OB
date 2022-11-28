import tkinter as tk

root = tk.Tk()
root.geometry("500x500")
root.title("My first project")

label = tk.Label(root, text="Hello, world!", font=('Times new roman', 18))
label.pack(padx=20, pady=40)

textbox = tk.Text(root, height=3, font=("Arial", 16))
textbox.pack()

btnframe = tk.Frame(root)
btnframe.columnconfigure(0, weight=1)
btnframe.columnconfigure(1, weight=1)
btnframe.columnconfigure(2, weight=1)

btn1 = tk.Button(btnframe, text="1", font=("Arial", 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(btnframe, text="2", font=("Arial", 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(btnframe, text="3", font=("Arial", 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(btnframe, text="4", font=("Arial", 18))
btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

btn5 = tk.Button(btnframe, text="5", font=("Arial", 18))
btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

btn6 = tk.Button(btnframe, text="6", font=("Arial", 18))
btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

btnframe.pack(fill='x')

root.mainloop()