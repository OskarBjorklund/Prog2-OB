import os

def get_existing_file_name():
    while True:
        file_name = input("Enter the file name: ")
        if os.path.exists(file_name):
            print("File found: " + file_name)
            return file_name
        else:
            print("Filen finns inte. Försök igen.")