import os, re
from tkinter import messagebox

def check_file_existance(file_path, file_name):
    if os.path.exists(file_path) == True:
        return file_path
    else:
        messagebox.showerror("Error", f"Filen '{file_name}' kan inte hittas.")

def correct_registry_format(file_path):
    """Check if the file has the correct format."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            parts = line.strip().split(';')
            if len(parts) != 5:
                messagebox.showerror("Error", f"Felaktigt format på rad '{line_num}': förväntar 5 personuppgifter, fick {len(parts)}")
                return False

            # Phone number format check (071-1111111)
            phone_pattern = r"07[0-9]-[0-9]{7}"
            if not re.match(phone_pattern, parts[2]) and parts[2] != "N/A":
                messagebox.showerror("Error", f"Felaktigt telefon format på rad {line_num}")
                return False

            # Email format check
            if not re.match(r"[^@]+@[^@]+\.[^@]+", parts[3]) and parts[3] != "N/A":
                messagebox.showerror("Error", f"Felaktigt e-post format på rad {line_num}")
                return False

        return True