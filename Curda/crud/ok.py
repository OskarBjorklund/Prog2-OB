def main():
    file_path = r'C:\Users\oskar\OneDrive\Dokument\GitHub\Prog2-OB\crud\students.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize empty lists to store information
    social_security = []
    last_names = []
    first_names = []

    # Process the data and populate the lists
    for i in range(0, len(lines), 3):
        social_security.append(lines[i].strip())
        last_names.append(lines[i + 1].strip())
        first_names.append(lines[i + 2].strip())

    # Example: Printing the first few entries
    for i in range(0, len(lines) // 3):  # Change the range to print more entries
        print(f"Namn: {first_names[i]} {last_names[i]} Personnr: {social_security[i]}")

main()