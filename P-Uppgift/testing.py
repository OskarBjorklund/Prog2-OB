import tkinter as tk

def on_enter_pressed(event):
    text = entry.get()
    print("Enter pressed! Entry text:", text)

root = tk.Tk()
root.title("Call Function on Enter Pressed")

# Create an Entry widget
entry = tk.Entry(root)
entry.pack()

# Bind the <Return> event to the Entry widget
entry.bind('<Return>', on_enter_pressed)

root.mainloop()
