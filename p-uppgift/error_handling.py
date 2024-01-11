# error_handling.py

def read_words_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

def read_leaderboard(file_path):
    try:
        with open(file_path, 'r') as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Warning: The file {file_path} was not found. Creating a new leaderboard.")
        return []

def write_leaderboard(file_path, leaderboard):
    try:
        with open(file_path, 'w') as file:
            for score in leaderboard:
                file.write(f"{score}\n")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
