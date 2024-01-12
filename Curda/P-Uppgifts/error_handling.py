import os
from tkinter import messagebox

def check_file_existance(file_path, file_name):
    if os.path.exists(file_path) == True:
        return file_path
    else:
        messagebox.showerror("Error", f"Filen '{file_name}' kan inte hittas.")