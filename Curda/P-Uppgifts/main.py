import tkinter as tk
from tkinter import messagebox, ttk
import os, sys

try:
    from error_handling import (check_file_existance, correct_registry_format, 
                                valid_filename, person_exists, 
                                is_valid_id_format, combine_registry_error)
except ImportError:
    messagebox.showerror("Error", "Avslutar programmet på grund av saknad fil 'error_handling.py'.")
    sys.exit()

FONT = ("Arial", 10)
REGISTER_BROWSER_FILE = "register.txt"

class StartGui:
    """
    A GUI class for the starting interface of the registry application.

    This class creates the initial graphical user interface that users interact with upon starting
    the application. It provides options for creating new registries, browsing existing ones,
    and other functionalities related to registry management.
    """

    def __init__(self):
        """
        Initializes the StartGui instance, setting up the main window and interface elements.

        The constructor initializes the root window, sets its title, size, and other properties,
        and then calls the `main_gui` method to set up the interface components.
        """
        self.root = tk.Tk()  # Create the main application window
        self.root.title("Register")  # Set the title of the window
        self.root.resizable(width=False, height=False)  # Fix the size of the window
        self.root.geometry("500x250")  # Set the initial size of the window

        self.main_gui()  # Set up the main GUI components
        self.root.mainloop()  # Start the Tkinter event loop

    def create_new_registry(self, event):
        """
        Creates a new registry with the specified name entered by the user.

        This method validates the entered registry name to ensure it follows the correct format and is unique.
        If validation passes, it proceeds to create a new registry and opens its GUI.

        Args:
            event: The event that triggered this method (not used in the method body).
        """
        # Retrieve the new registry name from the entry field
        new_registry_name = self.new_registry_entry.get()
        
        # Validate the filename and check if it's unique
        validated_filename = valid_filename(new_registry_name, include_register_browser_in_blacklist(REGISTER_BROWSER_FILE))
        
        if validated_filename:
            # If validation is successful, create the registry and open its GUI
            self.root.destroy()
            self.registry = RegistryGui(validated_filename, [])

        
    def manual_search_registry(self, event):
        """
        Initiates a manual search for a specific registry based on user input.

        This method is triggered by an event (such as pressing the Enter key) and retrieves the
        registry name from an entry field to perform the search.

        Args:
            event: The event that triggered this method (not used in the method body).
        """
        # Retrieve the search text from the entry field
        text = self.manual_search_entry.get()

        # Perform the search for the specified registry
        self.search_registry(text)


    def search_registry(self, registry_name):
        """
        Searches for a registry with the given name and opens it if it exists and is correctly formatted.

        This method checks if the specified registry file exists and conforms to the correct format.
        If these conditions are met, it opens the registry in a new GUI.

        Args:
            registry_name (str): The name of the registry to search for.
        """
        # Check if the specified registry file exists and has the correct format
        if check_file_existance(registry_name) and correct_registry_format(registry_name):
            # Destroy the current root window and open the found registry
            self.root.destroy()
            self.registry = open_registry_files(registry_name)


    def registry_browser_gui(self, use_combine_mode):
        """
        Sets up the registry browsing interface.

        This method configures the GUI for browsing through registries. It includes a treeview for displaying registry names
        and, if in combine mode, additional functionalities for combining registries and viewing combined results.

        Args:
            use_combine_mode (bool): Determines whether to set up the interface in combine mode, which includes 
                                     additional options for combining registries.
        """
        clear_widgets(self.main_frame)

        self.menubar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff = 0)
        self.file_menu.add_command(label = "Återgå till huvudmeny", command = lambda: return_to_start_menu(self.root))

        self.help_menu = tk.Menu(self.menubar, tearoff = 0)
        self.help_menu.add_command(label="Instruktioner", command = get_instruction)

        # Adding the "Fil" menu to the menubar
        self.menubar.add_cascade(label = "Fil", menu = self.file_menu)
        self.menubar.add_cascade(label = "Hjälp", menu = self.help_menu)

        # Display the menubar
        self.root.config(menu=self.menubar)

        self.browse_tree = ttk.Treeview(self.list_frame, columns=("name"), show="headings")
        self.browse_tree.heading("name", text="Filnamn")
        self.browse_tree.pack(fill="both", expand="yes")

        if use_combine_mode:
            self.root.geometry("{}x{}".format(800, 500))
            insert_tree(self.browse_tree, open_registry_browser_files(), self, False)   

            # Creating a treeview for combined people list
            self.combined_list_tree = ttk.Treeview(self.combined_registry_frame)
            self.combined_list_tree["columns"] = ("last_name", "first_name", "phone", "email", "address")

            self.combined_list_tree.column("# 0", width=0, stretch=tk.NO)
            self.combined_list_tree.column("last_name", width=150)
            self.combined_list_tree.column("first_name", width=150)
            self.combined_list_tree.column("phone", width=150)
            self.combined_list_tree.column("email", width=150)
            self.combined_list_tree.column("address", width=150)

            self.combined_list_tree.heading("last_name", text="Efternamn")
            self.combined_list_tree.heading("first_name", text="Förnamn")
            self.combined_list_tree.heading("phone", text="Telefonnummer")
            self.combined_list_tree.heading("email", text="E-post")
            self.combined_list_tree.heading("address", text="Adress")

            self.combined_list_tree.pack(fill="both", expand="yes")

            self.both_button = tk.Button(self.main_frame, text = "Lista på alla som finns i båda (de valda) registren", font = FONT, command = self.combine_buttons_pressed)
            self.union_button = tk.Button(self.main_frame, text = "Unionen på alla som finns i något av (de valda) registren", font = FONT, command = lambda: self.combine_buttons_pressed(True))

            self.both_button.pack(fill = "x", padx = 5, pady = 5)
            self.union_button.pack(fill = "x", padx = 5, pady = 5)

        else:
            insert_tree(self.browse_tree, open_registry_browser_files(), self, True)  

    def combine_buttons_pressed(self, union=False):
        """
        Handles the action triggered by pressing the combine buttons in the GUI.

        This method combines the person lists from two selected registries. It can perform either
        a union operation (merging and removing duplicates) or find common entries (intersection) 
        between the two registries.

        Args:
            union (bool): If True, performs a union of the two lists. Otherwise, finds duplicates.
        """
        # Check if the correct number of registries is selected and if they exist
        if combine_registry_error(get_selected_items(self.browse_tree)):
            first_file = get_selected_items(self.browse_tree)[0][0]
            second_file = get_selected_items(self.browse_tree)[1][0]

            if check_file_existance(first_file) and check_file_existance(second_file):
                # Convert the person lists from both files into nested lists
                first_person_list = to_nested_list(open_registry_files(first_file, True))
                second_person_list = to_nested_list(open_registry_files(second_file, True))

                # Perform the specified combine operation and refresh the tree view
                if union:
                    combined_list = combine_and_remove_duplicates(first_person_list, second_person_list)
                    refresh_tree(self.combined_list_tree, combined_list, self, True)
                else:
                    duplicates_list = find_duplicates(first_person_list, second_person_list)
                    refresh_tree(self.combined_list_tree, duplicates_list, self, True)


    def main_gui(self):
        """
        Sets up the main graphical user interface of the application.

        This method creates and arranges the primary widgets for the registry application, including
        areas for creating a new registry, browsing existing registries, conducting manual searches,
        and combining registries. It organizes these widgets in a grid layout and sets up event bindings
        for user interactions.

        The method also configures the main frame layout and ensures that the interface components
        are properly displayed and interactable.
        """
        self.list_frame = tk.LabelFrame(self.root)
        self.main_frame = tk.LabelFrame(self.root)
        self.combined_registry_frame = tk.LabelFrame(self.root)

        self.list_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)
        self.main_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)
        self.combined_registry_frame.pack(fill="both", expand = "yes", padx = 10, pady = 10)

        self.main_frame.columnconfigure(0, weight = 1)

        # New registry widgets
        self.new_registry_label = tk.Label(self.main_frame, text = "Skapa nytt register", font = FONT)
        self.new_registry_entry = tk.Entry(self.main_frame, font = FONT)

        # Browse registry widgets
        self.browse_registry_button = tk.Button(self.main_frame, text = "Bläddra bland register", font = FONT, command = lambda: self.registry_browser_gui(False))

        # Manual registry search widgets
        self.manual_search_label = tk.Label(self.main_frame, text = "Manuel sökning", font = FONT)
        self.manual_search_entry = tk.Entry(self.main_frame, font = FONT)

        # Combined registry widgets
        self.combine_registry_button = tk.Button(self.main_frame, text = "Samkörning av register", font = FONT, command = lambda: self.registry_browser_gui(True))

        # New registry widgets grid placement
        self.new_registry_label.grid(row = 0, column = 0, pady = 5, sticky = "ew")
        self.new_registry_entry.grid(row = 1, column = 0, pady = 5, sticky = "ew")

        # Browse registry widgets grid placement
        self.browse_registry_button.grid(row = 2, column = 0, pady = 5, sticky = "ew")

        # Manual registry search widgets grid placement
        self.manual_search_label.grid(row = 3, column = 0, pady = 5, sticky = "ew")
        self.manual_search_entry.grid(row = 4, column = 0, pady = 5, sticky = "ew")

        # Combined registry widgets grid placement
        self.combine_registry_button.grid(row = 5, column = 0, pady = 5, sticky = "ew")

        # Bind "Enter" press
        self.new_registry_entry.bind("<Return>", self.create_new_registry)
        self.manual_search_entry.bind("<Return>", self.manual_search_registry)
        
        # Pack
        self.main_frame.pack() 

class RegistryGui:
    """
    A GUI class for managing a registry of persons.

    This class creates a graphical user interface for displaying, adding, modifying,
    and deleting person records. It includes various functionalities such as searching,
    sorting, and updating person details.

    Attributes:
        register_name (str): The name of the registry.
        person_list (list): A list of Person objects representing individuals in the registry.
    """

    def __init__(self, register_name, person_list):
        """
        Initializes the RegistryGui instance with a registry name and a list of persons.

        Args:
            register_name (str): The name of the registry.
            person_list (list of Person): The initial list of persons in the registry.
        """
        self.register_name = register_name  # Name of the registry
        self.person_list = person_list      # List of persons in the registry

        # Set up the main window
        self.root = tk.Tk()
        self.root.title(self.register_name)    # Window title set to the registry name
        self.root.resizable(width=False, height=False)  # Fixed window size
        self.root.geometry("850x800")          # Set the geometry of the window

        self.register_gui()  # Call to set up the GUI components
        self.root.mainloop() # Start the main event loop
        
    def add_person(self):
        """
        Adds a new person to the person list based on the data entered in the entry widgets.

        This method retrieves the data from the entry fields, validates each field, creates
        a new Person object, and appends it to the person list. It then refreshes the Treeview
        to display the updated list.
        """
        # Retrieve the data from entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        # Validate the data
        if not is_valid_id_format(first_name, "name"):
            return  # Stop the function if the first name is invalid
        if not is_valid_id_format(last_name, "name"):
            return  # Stop the function if the last name is invalid
        if not is_valid_id_format(phone, "phone"):
            return  # Stop the function if the phone number is invalid
        if not is_valid_id_format(email, "email"):
            return  # Stop the function if the email is invalid
        if not is_valid_id_format(address, "adress"):
            return  # Stop the function if the address is invalid

        # Create a new Person object
        new_person = Person(last_name, first_name, phone, email, address)

        # Add the new person to the person list
        self.person_list.append(new_person)

        # Clear the entry fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

        # Refresh the Treeview with the updated person list
        refresh_tree(self.list_tree, self.person_list, self)


    def save_file_button(self):
        """
        Handles the action to save the current person list to a file.

        This method triggers when the 'save' button is clicked. It saves the current list
        of persons to a file with the name stored in `self.register_name`. Additionally,
        it updates the registry list file to include this new register.
        """
        # Save the current person list to a file
        save_file(self.register_name, format_person_list_to_file_format(self.person_list))

        # Update the registry list file with the new register name
        update_registry_list_file(self.register_name)

    def create_person_list(self, line, registry):
        """
        Creates a person from a line of text and adds it to the person list of a registry.

        This method is used to parse a line of text containing person attributes, create a
        Person object from it, and then append this object to the registry's person list.

        Args:
            line (str): A line of text representing a person's information.
            registry: The registry object to which the person will be added.
        """
        # Split the line into attributes and create a Person object
        attributes = line.strip().split(";")
        person = Person(*attributes)

        # Append the created Person object to the registry's person list
        registry.person_list.append(person)


    def search_button_press(self):
        """
        Initiates a search for persons based on the selected criteria and query.

        This method is triggered when the 'search' button is pressed. It retrieves the
        selected search criteria and the query from the entry fields, and then calls
        the `search_person` method to perform the search.
        """
        # Retrieve the selected search criteria and query
        search_criteria = self.search_option.get()
        query = self.search_entry.get()

        # Perform the search if criteria and query are provided
        if search_criteria and query:
            self.search_person(search_criteria, query)

    
    def search_person(self, search_criteria, query):
        """
        Searches for persons in the list based on specified criteria and query.

        The method validates the query format based on the search criteria (email, phone, name)
        and then searches the person list for matching entries. The results are displayed in a messagebox.

        Args:
            search_criteria (str): The criterion to search by ('email', 'phone', 'name').
            query (str): The query string used for searching.
        """
        # Validate the query based on the selected search criteria
        if search_criteria == "Sök efter E-Post" and not is_valid_id_format(query, "email"):
            return  # Stop the search if the email is invalid
        elif search_criteria == "Sök efter telefon" and not is_valid_id_format(query, "phone"):
            return  # Stop the search if the phone is invalid
        elif search_criteria == "Sök efter förnamn" and not is_valid_id_format(query, "name"):
            return  # Stop the search if the phone is invalid
        elif search_criteria == "Sök efter efternamn" and not is_valid_id_format(query, "name"):
            return # Stop the search if the phone is invalid

        # Perform the search based on the selected criteria
        matching_persons = []
        if search_criteria == "Sök efter telefon" and person_exists(self.person_list, query, "phone"):
            matching_persons = [person for person in self.person_list if person.phone == query]
        elif search_criteria == "Sök efter E-Post" and person_exists(self.person_list, query, "email"):
            matching_persons = [person for person in self.person_list if person.email == query]
        elif search_criteria == "Sök efter hela namnet":
            query = query.lower()  # Convert query to lowercase for case-insensitive search
            if person_exists(self.person_list, query, "full_name"):
                matching_persons = [person for person in self.person_list if f"{person.first_name} {person.last_name}".lower() == query]
        elif search_criteria == "Sök efter förnamn":
            query = query.lower()  # Convert query to lowercase for case-insensitive search
            if person_exists(self.person_list, query, "first_name"):
                matching_persons = [person for person in self.person_list if person.first_name.lower() == query]
        elif search_criteria == "Sök efter efternamn":
            query = query.lower()  # Convert query to lowercase for case-insensitive search
            if person_exists(self.person_list, query, "last_name"):
                matching_persons = [person for person in self.person_list if person.last_name.lower() == query]

        # Display the search results
        if matching_persons:
            result_message = "Match hittad:\n\n" + "\n\n".join(str(person) for person in matching_persons)
            messagebox.showinfo("Sökresultat", result_message)


    def sort_persons(self, sort_by):
        """
        Sorts the person list based on the specified attribute.

        The list can be sorted by either first name or last name in descending order.

        Args:
            sort_by (str): The attribute to sort by ('first_name', 'last_name').
        """
        if sort_by == "first_name":
            # Sort the person list by first name in descending order
            self.person_list.sort(key=lambda person: person.first_name.lower(), reverse=True)
        elif sort_by == "last_name":
            # Sort the person list by last name in descending order
            self.person_list.sort(key=lambda person: person.last_name.lower(), reverse=True)

        # Refresh the TreeView to display the sorted list
        refresh_tree(self.list_tree, self.person_list, self)


    def change_person_info(self):
        """
        Changes the information of a specified person in the person list.

        This method allows updating the phone number, email, or address of a person whose name 
        is specified. The updated information is validated before being applied.
        """
        # Extract the target name and desired changes from the entry fields
        target_name = self.target_name_entry.get().lower()
        change_option = self.info_change_option.get()
        new_change = self.new_change_entry.get()

        # Check if the person exists and update the specified attribute
        if person_exists(self.person_list, target_name, "full_name"):
            for person in self.person_list:
                if f"{person.first_name} {person.last_name}".lower() == target_name:
                    if change_option == "Ändra telefon" and is_valid_id_format(new_change, "phone"):
                        person.phone = new_change
                    elif change_option == "Ändra E-Post" and is_valid_id_format(new_change, "email"):
                        person.email = new_change
                    elif change_option == "Ändra address" and is_valid_id_format(new_change, "adress"):
                        person.address = new_change

            # Clear the entry fields after updating
            self.target_name_entry.delete(0, tk.END)
            self.new_change_entry.delete(0, tk.END)

            # Refresh the TreeView to show updated information
            refresh_tree(self.list_tree, self.person_list, self)


    def delete_person(self):
        """
        Deletes a specified person from the person list.

        The method identifies a person by name entered in the deletion field and removes them 
        from the person list, updating the TreeView accordingly.
        """
        # Retrieve the target name from the entry field
        target_name = self.delete_target_entry.get().lower()

        # Check if the person exists in the list and delete if found
        if person_exists(self.person_list, target_name, "full_name"):
            for i, person in enumerate(self.person_list):
                if f"{person.first_name} {person.last_name}".lower() == target_name:
                    del self.person_list[i]  # Delete the person
                    break

            # Clear the deletion field
            self.delete_target_entry.delete(0, tk.END)

            # Refresh the TreeView to reflect the deletion
            refresh_tree(self.list_tree, self.person_list, self)

            # Display a success message
            messagebox.showinfo("Borttagen", f"{target_name} har tagits bort.")


    def register_gui(self):
        """
        Sets up the GUI components for the registry interface.

        This method is responsible for initializing and arranging various widgets in the GUI.
        It includes setup for menu bars, entry fields for person information, search functionality,
        sorting options, information modification, and deletion options. It also configures the
        Treeview widget for displaying person information and integrates a scrollbar for it.

        The method organizes the layout using Tkinter's grid system and also configures the styles
        and properties of widgets, ensuring a structured and user-friendly interface.
        """
        
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
        self.file_menu.add_command(label = "Återgå till huvudmeny", command = lambda: return_to_start_menu(self.root))

        self.help_menu = tk.Menu(self.menubar, tearoff = 0)
        self.help_menu.add_command(label="Instruktioner", command = get_instruction)

        # Adding the "File" menu to the menubar
        self.menubar.add_cascade(label = "Fil", menu = self.file_menu)
        self.menubar.add_cascade(label = "Hjälp", menu = self.help_menu)

        # Display the menubar
        self.root.config(menu=self.menubar)

        # Adding a person widgets
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

        # Searching for a person widgets
        self.search_option = ttk.Combobox(self.wrapper, values=["Sök efter förnamn", "Sök efter efternamn", "Sök efter hela namnet", "Sök efter telefon", "Sök efter E-Post"])
        self.search_option.set("Sök efter förnamn")  # Set the default value
        self.search_entry = tk.Entry(self.wrapper, font = FONT)
        self.search_button = tk.Button(self.wrapper, text = "Sök", font = FONT, command = self.search_button_press)

        # Sort personlist widgets
        self.sort_first_name_button = tk.Button(self.wrapper, text = "Sortera efter förnamn", font = FONT, command = lambda: self.sort_persons("first_name"))
        self.sort_last_name_button = tk.Button(self.wrapper, text = "Sortera efter efternamn", font = FONT, command = lambda: self.sort_persons("last_name"))

        # Change info widgets
        self.target_name_label = tk.Label(self.wrapper, text = "Namn (Förnamn + Efternamn)", font = FONT)
        self.target_name_entry = tk.Entry(self.wrapper, font = FONT)
        self.info_change_option = ttk.Combobox(self.wrapper, values=["Ändra telefon", "Ändra E-Post", "Ändra address"])
        self.info_change_option.set("Ändra telefon")  # Set the default value
        self.new_change_label = tk.Label(self.wrapper, text = "Ändring", font = FONT)
        self.new_change_entry = tk.Entry(self.wrapper, font = FONT)
        self.execute_change_button = tk.Button(self.wrapper, text = "Utför ändring", font = FONT, command = self.change_person_info)

        # Delete person widgets
        self.delete_target_label = tk.Label(self.wrapper, text = "Namn (Förnamn + Efternamn)", font = FONT)
        self.delete_target_entry = tk.Entry(self.wrapper, font = FONT)
        self.delete_target_button = tk.Button(self.wrapper, text = "Radera", font = FONT, command = self.delete_person)

        # Add person widgets grid placement
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

        # Search for person widgets grid placement
        self.search_option.grid(row = 3, column = 2, pady = 5, padx = 5)
        self.search_entry.grid(row = 3, column = 3, pady = 5, padx = 5)
        self.search_button.grid(row = 3, column = 4, pady = 5, padx = 5)

        # Sort people widgets grid placement
        self.sort_first_name_button.grid(row = 3, column = 0, pady = 5, padx = 5)
        self.sort_last_name_button.grid(row = 3, column = 1, pady = 5, padx = 5)

        # Change person info widgets grid placement
        self.target_name_label.grid(row = 4, column = 0, pady = 5, padx = 5)
        self.target_name_entry.grid(row = 5, column = 0, pady = 5, padx = 5)
        self.info_change_option.grid(row = 5, column = 1, pady = 5, padx = 5)
        self.new_change_label.grid(row = 4, column = 2, pady = 5, padx = 5)
        self.new_change_entry.grid(row = 5, column = 2, pady = 5, padx = 5)
        self.execute_change_button.grid(row = 5, column = 3, pady = 5, padx = 5)

        # Delete person widgets grid placement
        self.delete_target_label.grid(row = 6, column = 0, pady = 5, padx = 5)
        self.delete_target_entry.grid(row = 7, column = 0, pady = 5, padx = 5)
        self.delete_target_button.grid(row = 7, column = 1, pady = 5, padx = 5)


        self.list_frame.pack_propagate(0) # Forbid resizing

        # Treeview widget
        self.list_tree = ttk.Treeview(self.list_frame)
        self.list_tree["columns"] = ("last_name", "first_name", "phone", "email", "address")

        width = 150
        wraplength = 125
        row_height = 75

        self.list_tree.column("# 0", width=0, stretch=tk.NO)
        self.list_tree.column("last_name", width = width)
        self.list_tree.column("first_name", width = width)
        self.list_tree.column("phone", width = width)
        self.list_tree.column("email", width = width)
        self.list_tree.column("address", width = width)

        self.list_tree.heading("last_name", text = "Efternamn")
        self.list_tree.heading("first_name", text = "Förnamn")
        self.list_tree.heading("phone", text = "Telefonnummer")
        self.list_tree.heading("email", text = "E-post")
        self.list_tree.heading("address", text = "Adress")

        self.list_tree["displaycolumns"] = ("last_name", "first_name", "phone", "email", "address")

        style = ttk.Style()
        style.configure("Treeview", fieldbackground="white")
        style.configure("Treeview.Heading", font = FONT)
        style.configure("Treeview.Cell", wraplength = wraplength) # Wraplenght

        self.list_tree.configure(style = "Custom.Treeview")
        style.configure("Custom.Treeview", rowheight = row_height)

        # Create a vertical scrollbar for the list_tree
        scrollbar = ttk.Scrollbar(self.list_frame, orient = "vertical", command = self.list_tree.yview)
        # Configure the Treeview to update the scrollbar
        self.list_tree.configure(yscrollcommand = scrollbar.set)

        # Pack the scrollbar to the right side of the list_frame
        scrollbar.pack(side="right", fill = "y")
        # Pack the Treeview to fill the rest of the space
        self.list_tree.pack(side = "left", fill = "both", expand = "yes")

        # Insert people in tree
        insert_tree(self.list_tree, to_nested_list(self.person_list), self, False)

class Person:
    """
    Represents a person with basic contact details.

    This class encapsulates the details of a person, including their last name,
    first name, phone number, email address, and physical address.

    Attributes:
        last_name (str): The last name of the person.
        first_name (str): The first name of the person.
        phone (str): The phone number of the person.
        email (str): The email address of the person.
        address (str): The physical address of the person.
    """

    def __init__(self, last_name, first_name, phone, email, address):
        """
        Initializes a new instance of the Person class.
        """
        self.last_name = last_name  # Store the last name
        self.first_name = first_name  # Store the first name
        self.phone = phone  # Store the phone number
        self.email = email  # Store the email address
        self.address = address  # Store the physical address

    def __str__(self):
        """
        Returns a string representation of the person.

        This method formats the person's details into a readable string.

        Returns:
            str: A formatted string containing the person's details.
        """
        # Format and return the person's details as a string
        return f"{self.first_name} {self.last_name}, Telefon: {self.phone}, E-Post: {self.email}, Address: {self.address}"

    
def clear_widgets(target):
    """
    Removes all child widgets from a given parent widget.

    This function iterates over all children of the target widget and destroys them, effectively clearing the widget.

    Args:
        target (tk.Widget): The parent widget from which all child widgets will be removed.
    """
    for widget in target.winfo_children():
        widget.destroy()  # Destroy each child widget

    
def insert_tree(tree, children, instance, use_bind):
    """
    Populates a Treeview with items and optionally binds a double-click event.

    This function inserts a list of items ('children') into the specified Treeview widget ('tree'). 
    It also provides an option to bind a double-click event to these items.

    Args:
        tree (ttk.Treeview): The Treeview widget to populate.
        children (list): A list of items to insert into the Treeview.
        instance: The instance of the class where this function is called.
        use_bind (bool): If True, binds a double-click event to the items in the Treeview.
    """
    for item in children[::-1]:
        tree.insert("", "end", values=item)  # Insert each item into the Treeview

    if use_bind:
        # Bind double-click event to the tree items
        tree.bind("<Double-1>", lambda event: double_click(event, tree, instance))


def clear_tree(tree):
    """
    Removes all items from a Treeview widget.

    This function clears all the entries in the specified Treeview widget, making it empty.

    Args:
        tree (ttk.Treeview): The Treeview widget to clear.
    """
    for item in tree.get_children():
        tree.delete(item)  # Remove each item from the Treeview


def refresh_tree(tree, list, instance, is_nested=False):
    """
    Refreshes the content of a Treeview widget with new data.

    Args:
        tree (ttk.Treeview): The Treeview widget to be refreshed.
        list (list): A list of data to be inserted into the Treeview.
        instance: The instance of the class where this function is called.
        is_nested (bool, optional): A flag indicating if the list is already in a nested format suitable for Treeview. Defaults to False.
    """
    clear_tree(tree)  # Clear the existing content of the Treeview
    if is_nested:
        # If the list is already nested, insert it directly
        insert_tree(tree, list, instance, False)
    else:
        # Convert the list to a nested format and then insert
        insert_tree(tree, to_nested_list(list), instance, False)


def double_click(event, tree, instance):
    """
    Handles the double-click event on a Treeview item.

    Args:
        event: The event object (not used in this function).
        tree (ttk.Treeview): The Treeview widget where the event occurred.
        instance: The instance of the class where this function is called.
    """
    item = tree.selection()  # Get the selected item
    for i in item:
        filename = tree.item(i, "values")[0]
        instance.search_registry(filename)  # Call the search_registry method with the filename


def get_selected_items(tree):
    """
    Retrieves the values of all selected items in a Treeview.

    Args:
        tree (ttk.Treeview): The Treeview widget to get selected items from.

    Returns:
        list: A list of values of the selected items.
    """
    selected_items = tree.selection()  # Get all selected items
    values = []
    for item in selected_items:
        item_values = tree.item(item, "values")  # Get values for each item
        values.append(item_values)
    return values

    
def create_person_from_line(line):
    """
    Creates a Person object from a line of text.

    Args:
        line (str): A line of text representing a person's details.

    Returns:
        Person: A Person object created from the provided line.
    """
    attributes = line.strip().split(';')  # Split the line into attributes
    return Person(*attributes)  # Create a Person object with the attributes


def open_registry_files(filename, combine_registry=False):
    """
    Opens a registry file and reads its content into a list of Person objects.

    Args:
        filename (str): The name of the file to open.
        combine_registry (bool, optional): A flag to indicate if the function is used for combining registries. Defaults to False.

    Returns:
        If combine_registry is True, returns a list of Person objects. 
        Otherwise, initializes and returns a RegistryGui instance with the list of Person objects.
    """
    file_path = os.path.join(os.path.dirname(__file__), filename)
    person_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            person = create_person_from_line(line)
            person_list.append(person)
        if combine_registry:
            return person_list
        else:
            registry = RegistryGui(filename, person_list)
            return registry

    
def open_registry_browser_files():
    """
    Opens and reads the registry browser file, returning a list of registry names.

    Returns:
        list: A list of registry names read from the file.
    """
    file_path = check_file_existance(REGISTER_BROWSER_FILE)

    if file_path:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            values = file_contents.strip().split(';')
            result_list = [value.strip() for value in values]
            return result_list
    return []


def include_register_browser_in_blacklist(blacklist_word):
    """
    Includes an additional word into the blacklist extracted from the registry browser file.

    Args:
        blacklist_word (str): The words to be added to the blacklist
    
    Returns:
    list: The updated blacklist with the new word included.
    """

    list_of_blacklist_words = open_registry_browser_files()
    if list_of_blacklist_words is None:
        list_of_blacklist_words = []

    list_of_blacklist_words.append(blacklist_word)
    return list_of_blacklist_words

def to_nested_list(person_list):
    """
    Converts a list of Person objects into a nested list of their attributes.

    Each Person object is transformed into a list of its attributes (last name, first name, phone, email, address), 
    and these lists are then compiled into a larger list.

    Args:
        person_list (list): A list of Person objects.

    Returns:
        list: A nested list where each inner list contains the attributes of a Person object.
    """
    nested_list = []
    for person in person_list:
        # Append a list of attributes for each person to the nested list
        nested_list.append([person.last_name, person.first_name, person.phone, person.email, person.address])
    return nested_list

def get_instruction():
    info_text = (
    "Register:\n"
    "Namn: [A-Ö] - Ex Linda\n"
    "Telefonnummer: 07[0-9] + \"-\" + 7*[0-9] - Ex 071-1234567\n"
    "E-Post: [A-Ö] + \"@\" + [A-Ö] + \".\" + [A-Ö] - Ex kth@kth.se\n"
    "Address: Gata address + \", \" + Stad - Ex Kthvägen 10, Stockholm\n\n"
    "\"N/A\" Används vid okänd info.\n\n"
    "Glöm inte att spara filen!\n\n"
    "Bläddra:\n"
    "Dubbelklicka på en fil.\n\n"
    "Samköra:\n"
    "Markera två filer."
    )
    messagebox.showinfo("Instruktioner", info_text)

def find_duplicates(list1, list2):
    """
    Finds duplicate items that are present in both list1 and list2.

    This function identifies items that are common to both lists and compiles them into a new list, ensuring each item is unique.

    Args:
        list1 (list): The first list to compare for duplicates.
        list2 (list): The second list to compare for duplicates.

    Returns:
        list: A list of items that are duplicates in both list1 and list2.
    """
    duplicates = []
    for item in list1:
        # Check if an item is in both lists and not already in duplicates
        if item in list2 and item not in duplicates:
            duplicates.append(item)  # Append duplicate item to the list
    return duplicates

def combine_and_remove_duplicates(list1, list2):
    """
    Combines two lists into one and removes any duplicate entries.

    This function creates a new list that includes all unique items from both list1 and list2.

    Args:
        list1 (list): The first list to be combined.
        list2 (list): The second list to be combined.

    Returns:
        list: A combined list of unique items from both list1 and list2.
    """
    combined_list = list1.copy()  # Start with a copy of list1
    for item in list2:
        # Append items from list2 if they are not already in the combined list
        if item not in combined_list:
            combined_list.append(item)
    return combined_list

def format_person_list_to_file_format(person_list):
    """
    Formats a list of Person objects into a string suitable for file storage.

    Each Person object's attributes are concatenated into a semicolon-separated string.
    All such strings from the list are then joined with newline characters.

    Args:
        person_list (list): A list of Person objects.

    Returns:
        str: A string representation of the person list, formatted for file storage.
    """
    formatted_text_list = []

    for person in person_list:
        # Construct the formatted string for each person in the correct order
        formatted_person = f"{person.last_name};{person.first_name};{person.phone};{person.email};{person.address}"
        formatted_text_list.append(formatted_person)

    # Join the formatted strings with newline characters to create the final text representation
    formatted_text = "\n".join(formatted_text_list)

    return formatted_text


def save_file(filename, list_of_personal_info):
    """
    Saves a string of personal information to a specified file.

    The file is created or overwritten in the script's directory.

    Args:
        filename (str): The name of the file to save the data to.
        list_of_personal_info (str): The string containing the personal information.
    """
    script_directory = os.path.dirname(__file__)
    file_path = os.path.join(script_directory, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write the personal information string to the file
        file.write(list_of_personal_info)


def update_registry_list_file(new_registry_name, registry_list_file=REGISTER_BROWSER_FILE):
    """
    Updates the registry list file with a new registry name.

    The new name is appended to the file, which contains a list of registry names.

    Args:
        new_registry_name (str): The new registry name to append.
        registry_list_file (str, optional): The file name where registry names are stored. Defaults to "register.txt".
    """
    script_directory = os.path.dirname(__file__)
    file_path = os.path.join(script_directory, registry_list_file)

    if new_registry_name not in open_registry_browser_files():
        with open(file_path, 'a', encoding='utf-8') as file:  # 'a' mode for appending
            file.write(new_registry_name + ";")  # Append the new registry name

def return_to_start_menu(target_root):
    """
    Closes the current Tkinter window and returns to the start menu.

    Args:
        target_root (Tk): The root Tkinter window to be destroyed.
    """
    target_root.destroy()  # Close the current Tkinter window
    start_program()       # Start the initial program menu

def start_program():
    """
    Initializes and starts the main GUI application.
    """
    StartGui()  # Initialize and start the main GUI

start_program()