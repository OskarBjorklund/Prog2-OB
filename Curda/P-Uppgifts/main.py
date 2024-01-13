import tkinter as tk
from tkinter import messagebox, ttk
import os
from error_handling import check_file_existance, correct_registry_format, is_valid_email, is_valid_phone, is_valid_input_lenght

FONT = ("Arial", 10)

class StartGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Register")
        self.root.resizable(width=False, height=False)
        self.root.geometry("{}x{}".format(500, 220))

        self.main_gui()
        self.root.mainloop()

    def main_gui(self):
        
        self.main_frame = tk.LabelFrame(self.root)

        self.main_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)

        self.main_frame.columnconfigure(0, weight = 1)

        self.new_registry_label = tk.Label(self.main_frame, text = "Skapa nytt register", font = FONT)
        self.new_registry_entry = tk.Entry(self.main_frame, font = FONT)

        self.browse_registry_button = tk.Button(self.main_frame, text = "Bläddra bland register", font = FONT)

        self.manual_search_label = tk.Label(self.main_frame, text = "Manuel sökning", font = FONT)
        self.manual_search_entry = tk.Entry(self.main_frame, font = FONT)

        self.combine_registry_button = tk.Button(self.main_frame, text = "Samkörning av register", font = FONT)

        self.new_registry_label.grid(row = 0, column = 0, pady = 5, sticky = "ew")
        self.new_registry_entry.grid(row = 1, column = 0, pady = 5, sticky = "ew")
        self.browse_registry_button.grid(row = 2, column = 0, pady = 5, sticky = "ew")
        self.manual_search_label.grid(row = 3, column = 0, pady = 5, sticky = "ew")
        self.manual_search_entry.grid(row = 4, column = 0, pady = 5, sticky = "ew")
        self.combine_registry_button.grid(row = 5, column = 0, pady = 5, sticky = "ew")

        self.new_registry_entry.bind("<Return>", self.create_new_registry)
        self.manual_search_entry.bind("<Return>", self.manual_search_registry)
        
        self.main_frame.pack() 

    def create_new_registry(self, event):
        new_registry_name = self.new_registry_entry.get()
        self.root.destroy()
        self.registry = RegistryGui(new_registry_name, [])
        

    def manual_search_registry(self, event):
        text = self.manual_search_entry.get()
        self.search_registry(text)

    def search_registry(self, registry_name):
        # Check if the file exists before destroying the root
        file_path = os.path.join(os.path.dirname(__file__), registry_name)
        if check_file_existance(file_path, registry_name):
            if correct_registry_format(file_path):
                self.root.destroy()
                self.registry = open_file(registry_name)

    def on_closing(self):
        pass

class RegistryGui:
    def __init__(self, register_name, person_list):
        self.register_name = register_name
        self.person_list = person_list

        self.root = tk.Tk()
        self.root.title(self.register_name)
        self.root.resizable(width=False, height=False)
        self.root.geometry("{}x{}".format(800, 600))

        self.register_gui()
        self.root.mainloop()

    def insert_tree(self, children):
        """
        This method inserts children into specified tree
        """
        # Inserts comments or posts into selected tree. 
        for i in children[::-1]:
            self.list_tree.insert("", "end", values = i)
            self.list_tree.bind("<Double-1>", self.double_click)
    
    def clear_tree(self):
        """
        Removes all children from the tree
        """
        for item in self.list_tree.get_children():
            self.list_tree.delete(item)

    def double_click(self, event):
        """
        Calls switch_interface if selected post is pressed again
        """
        item = self.list_tree.selection()
        for i in item:
            print(self.list_tree.item(i, "values")[0])

    def add_person(self):
    # Retrieve the data from entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        # Validate email and phone
        if not is_valid_email(email):
            return  # Stop the function if the email is invalid

        if not is_valid_phone(phone):
            return  # Stop the function if the phone is invalid
        
        if not is_valid_input_lenght(first_name):
            return  # Stop the function if the phone is invalid
        
        if not is_valid_input_lenght(last_name):
            return  # Stop the function if the phone is invalid
        
        if not is_valid_input_lenght(address):
            return  # Stop the function if the phone is invalid

        # Create a new Person object
        new_person = Person(last_name, first_name, phone, email, address)

        # Add the new person to the person list
        self.person_list.append(new_person)

        # Optionally clear the entry fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

        self.clear_tree()
        self.insert_tree(to_nested_list(self.person_list))

    def return_to_start_menu(self):
        self.root.destroy()
        start_program()

    def save_file_button(self):
        save_file(self.register_name, format_person_list_to_file_format(self.person_list))

    def create_person_list(self, line, registry):
        attributes = line.strip().split(";")
        person = Person(*attributes)
        registry.person_list.append(person)
    
    def print_persons(self):
        for person in self.person_list:
            print(person)
    
    def register_gui(self):
        self.wrapper = tk.LabelFrame(self.root)
        self.list_frame = tk.LabelFrame(self.root)

        self.wrapper.pack(fill = "both", expand = "yes", padx = 10, pady = 10)
        self.list_frame.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

        # Create a menubar
        self.menubar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff = 0)
        self.file_menu.add_command(label = "Spara", command = self.save_file_button)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Återgå till huvudmeny", command = self.return_to_start_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff = 0)
        self.help_menu.add_command(label="Instruktioner")

        # Adding the "File" menu to the menubar
        self.menubar.add_cascade(label = "Fil", menu = self.file_menu)
        self.menubar.add_cascade(label = "Hjälp", menu = self.help_menu)

        # Display the menubar
        self.root.config(menu=self.menubar)

        self.search_option = ttk.Combobox(self.wrapper, values=["Telefon", "Namn", "E-Post"])
        self.search_option.set("Telefon")  # Set the default value

        self.first_name_entry = tk.Entry(self.wrapper, font = FONT)
        self.first_name_label = tk.Label(self.wrapper, text = "Förnamn", font = FONT)
        self.last_name_entry = tk.Entry(self.wrapper, font = FONT)
        self.last_name_label = tk.Label(self.wrapper, text = "Efternamn", font = FONT)
        self.phone_entry = tk.Entry(self.wrapper, font = FONT)
        self.phone_label = tk.Label(self.wrapper, text = "Telefonnummer", font = FONT)
        self.email_entry = tk.Entry(self.wrapper, font = FONT)
        self.email_label = tk.Label(self.wrapper, text = "E-post", font = FONT)
        self.address_entry = tk.Entry(self.wrapper, font = FONT)
        self.address_label = tk.Label(self.wrapper, text = "Adress", font = FONT)

        self.add_person_button = tk.Button(self.wrapper, text = "Lägg till person", font = FONT, command = self.add_person)

        self.first_name_entry.grid(row = 1, column = 0, pady = 5, padx = 5)
        self.first_name_label.grid(row = 0, column = 0, pady = 5, padx = 5)
        self.last_name_entry.grid(row = 1, column = 1, pady = 5, padx = 5)
        self.last_name_label.grid(row = 0, column = 1, pady = 5, padx = 5)
        self.phone_entry.grid(row = 1, column = 2, pady = 5, padx = 5)
        self.phone_label.grid(row = 0, column = 2, pady = 5, padx = 5)
        self.email_entry.grid(row = 1, column = 3, pady = 5, padx = 5)
        self.email_label.grid(row = 0, column = 3, pady = 5, padx = 5)
        self.address_entry.grid(row = 1, column = 4, pady = 5, padx = 5)
        self.address_label.grid(row = 0, column = 4, pady = 5, padx = 5)

        self.add_person_button.grid(row = 2, column = 2, pady = 5, padx = 5)
        self.search_option.grid(row = 3, column = 2, pady = 5, padx = 5)

        self.list_frame.pack_propagate(0) 

        self.list_tree = ttk.Treeview(self.list_frame)
        self.list_tree["columns"] = ("last_name", "first_name", "phone", "email", "address")

        self.list_tree.column("# 0", width=0, stretch=tk.NO)  # Set width to 0 to make it invisible
        self.list_tree.column("last_name", width=150)
        self.list_tree.column("first_name", width=150)
        self.list_tree.column("phone", width=150)
        self.list_tree.column("email", width=150)
        self.list_tree.column("address", width=150)

        self.list_tree.heading("last_name", text="Efternamn")
        self.list_tree.heading("first_name", text="Förnamn")
        self.list_tree.heading("phone", text="Telefonnummer")
        self.list_tree.heading("email", text="E-post")
        self.list_tree.heading("address", text="Adress")

        self.list_tree["displaycolumns"] = ("last_name", "first_name", "phone", "email", "address")

        style = ttk.Style()
        style.configure("Treeview", fieldbackground="white")
        style.configure("Treeview.Heading", font = FONT)
        style.configure("Treeview.Cell", wraplength = 125)

        row_height = 75

        self.list_tree.configure(style = "Custom.Treeview")
        style.configure("Custom.Treeview", rowheight = row_height)

        self.list_tree.pack(fill = "both", expand = "yes")

        # Create a vertical scrollbar for the list_tree
        scrollbar = ttk.Scrollbar(self.list_frame, orient = "vertical", command = self.list_tree.yview)
        # Configure the Treeview to update the scrollbar
        self.list_tree.configure(yscrollcommand = scrollbar.set)

        # Pack the scrollbar to the right side of the list_frame
        scrollbar.pack(side="right", fill = "y")
        # Pack the Treeview to fill the rest of the space
        self.list_tree.pack(side = "left", fill = "both", expand = "yes")

        self.insert_tree(to_nested_list(self.person_list))

class Person:
    def __init__(self, first_name, last_name, phone, email, address):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, Phone: {self.phone}, Email: {self.email}, Address: {self.address}"

def create_person_from_line(line):
    attributes = line.strip().split(';')
    return Person(*attributes)

def open_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)

    person_list = []
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        for line in file:
            person = create_person_from_line(line)
            person_list.append(person)
        registry = RegistryGui(filename, person_list)  # Creating RegistryGUI instance with person_list
        return registry
    
def to_nested_list(person_list):
        nested_list = []
        for person in person_list:
            nested_list.append([person.first_name, person.last_name, person.phone, person.email, person.address])
        return nested_list

def format_person_list_to_file_format(person_list):
    formatted_text_list = []

    for person in person_list:
        # Construct the formatted string for each person
        formatted_person = f"{person.last_name};{person.first_name};{person.phone};{person.email};{person.address}"
        formatted_text_list.append(formatted_person)

    # Join the formatted strings with newline characters to create the final text representation
    formatted_text = "\n".join(formatted_text_list)

    return formatted_text

def save_file(filename, list_of_personal_info):
    script_directory = os.path.dirname(__file__)
    file_path = os.path.join(script_directory, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(list_of_personal_info)

def start_program():  
    StartGui()

start_program()