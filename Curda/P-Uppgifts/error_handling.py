import os, re
from tkinter import messagebox

def check_file_existance(file_path, file_name):
    if os.path.exists(file_path) == True:
        return file_path
    else:
        messagebox.showerror("Error", f"Filen '{file_name}' kan inte hittas.")

def is_valid_email(email, line_num=None):
    """Check if the email has the correct format and show an error message if not."""
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    if not (re.match(email_pattern, email) or email == "N/A"):
        error_message = "Felaktigt e-postformat"
        if line_num is not None:
            error_message += f" på rad {line_num}"
        messagebox.showerror("Error", error_message)
        return False
    return True

def is_valid_phone(phone, line_num=None):
    """Check if the phone number has the correct format and show an error message if not."""
    phone_pattern = r"07[0-9]-[0-9]{7}$"
    if not (re.match(phone_pattern, phone) or phone == "N/A"):
        error_message = "Felaktigt telefonformat"
        if line_num is not None:
            error_message += f" på rad {line_num}"
        messagebox.showerror("Error", error_message)
        return False
    return True

def is_valid_input_lenght(entry):
    if len(entry) > 0 and len(entry) < 25:
        return True
    else:
        return False


def correct_registry_format(file_path):
    """Check if the file has the correct format."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            parts = line.strip().split(';')
            if len(parts) != 5:
                messagebox.showerror("Error", f"Felaktigt format på rad '{line_num}': förväntar 5 personuppgifter, fick {len(parts)}")
                return False

            if not is_valid_phone(parts[2], line_num):
                return False

            if not is_valid_email(parts[3], line_num):
                return False

        return True