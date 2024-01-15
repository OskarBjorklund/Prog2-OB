import os, re
from tkinter import messagebox

def check_file_existance(file_name):
    """
    Checks if a file exists in the same directory as the script.

    Args:
        file_name (str): The name of the file to check.

    Returns:
        str: The path to the file if it exists, otherwise displays an error message and returns None.
    """

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(file_path) == True:
        return file_path # Returns a correct existing path to a file
    else:
        messagebox.showerror("Error", f"Filen '{file_name}' kan inte hittas.")

def is_valid_id_format(input_value, validation_type, line_num=None):
    """
    Validates if the input value matches the specified format type.

    This function checks the input value against different regular expression patterns based on the validation type specified (email, phone, name, or address). It accepts 'N/A' for any type.

    Args:
        input_value (str): The value to be validated.
        validation_type (str): The type of validation to perform. Options include 'email', 'phone', 'name', and 'address'.
        line_num (int, optional): The line number in the file where the input value is found. Used for error reporting.

    Returns:
        bool: True if the input value matches the specified format, False otherwise. If the format type is not recognized, it returns True by default.
    """
    if validation_type == "email":
        pattern = r"[^@]+@[^@]+\.[^@]+" # Format anything@anything.anything
        error_message = "Felaktigt e-postformat"
    elif validation_type == "phone":
        pattern = r"07[0-9]-[0-9]{7}$" # Format 07(0-9)-(0-9)*7
        error_message = "Felaktigt telefonformat"
    elif validation_type == "name":
        pattern = r"^[A-Za-z]+$" # Only letters
        error_message = "Felaktigt namnformat"
    elif validation_type == "address":
        pattern = r"^[A-Za-z]+.*" # Letters and symbols
        error_message = "Felaktigt adressformat"
    else:
        return True  # Return True if correct format

    if not (re.match(pattern, input_value) or input_value == "N/A"): # Accepts N/A
        if line_num is not None:
            error_message += f" på rad {line_num}" # Displays what row an error has occured
        messagebox.showerror("Error", error_message)
        return False

    return True

def correct_registry_format(file_name):
    """
    Validates the format of a registry file. Each line in the file should contain 5 pieces of information.

    Args:
        file_name (str): The name of the file to be checked.

    Returns:
        bool: True if the file format is correct, False otherwise.
    """

    # Construct the full path of the file
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        # Enumerate through each line in the file
        for line_num, line in enumerate(file, 1):
            # Split the line into parts based on the ';' delimiter
            parts = line.strip().split(';')

            # Check if the number of parts is not equal to 5 (expected format)
            if len(parts) != 5:
                # Show an error message and return False for incorrect format
                messagebox.showerror("Error", f"Felaktigt format på rad '{line_num}': förväntar 5 personuppgifter, fick {len(parts)}")
                return False

            # Validate the phone number format
            if not is_valid_id_format(parts[2], "phone", line_num):
                # If phone number format is incorrect, the function returns False
                return False

            # Validate the email format
            if not is_valid_id_format(parts[3], "email", line_num):
                # If email format is incorrect, the function returns False
                return False

        # If all lines are correctly formatted, return True
        return True

    
def valid_filename(filename, blacklist):
    """
    Validates a filename to ensure it only contains letters and numbers and is not in the blacklist.

    Args:
        filename (str): The name of the file to validate.
        blacklist (list): A list of filenames that are not allowed.

    Returns:
        str: The validated filename with '.txt' appended, or None if validation fails.
    """
    # Converts å, ä and ö to a and o
    filename = filename.replace("ö", "o").replace("å", "a").replace("ä", "a")

    # Check if the filename only contains letters and numbers
    if not filename.isalnum():
        messagebox.showerror("Error", "Otilåtna bokstäver")
        return None

    filename += ".txt"


    # Check if the filename is in the blacklist
    if blacklist and filename in blacklist:
        messagebox.showerror("Error", f"Filen {filename} finns redan.")
        return None

    return filename

def person_exists(person_list, query, search_by):
    """
    Checks if a person exists in the given list based on the provided query and search criteria.

    Args:
        person_list (list): The list of Person objects to search through.
        query (str): The search query (name, phone number, or email).
        search_by (str): The criteria for searching ('name', 'phone', or 'email').

    Returns:
        bool: True if a person matching the query exists, False otherwise.
    """
    # Convert the query to lowercase for case-insensitive search
    query = query.lower()

    if query == "":
        messagebox.showerror("Error", f"Textrutan är tom, du måste ange något.")
        return False
    
    if search_by == "name":
        # Check if a person with the given full name exists in the list
        for person in person_list:
            person_full_name = f"{person.first_name} {person.last_name}".lower()
            if person_full_name == query:
                return True
    elif search_by == "phone":
        # Check if a person with the given phone number exists in the list
        for person in person_list:
            if person.phone == query:
                return True
    elif search_by == "email":
        # Check if a person with the given email exists in the list
        for person in person_list:
            if person.email == query:
                return True
    
    messagebox.showerror("Error", f"Informationen {query} kan inte hittas.")
    return False

def combine_registry_error(selections):
    """
    Validates whether exactly two items are selected.

    Args:
        selections (list): The list of selected items.

    Returns:
        bool: True if exactly two items are selected, False otherwise, with an error message displayed.
    """

    if len(selections) == 2: # Two selected registries
        return True
    else:
        messagebox.showerror("Error", f"Markera två stycken register, du markerade {len(selections)} stycken.")
        return False