def replace_swedish_characters(text):
    """
    This function takes a string as input, replaces all occurrences of Swedish characters
    'ö' with 'o', 'å' with 'a', and 'ä' with 'a', and then returns the modified string.
    """
    # Replace Swedish characters with their corresponding English characters
    text = text.replace("ö", "o").replace("å", "a").replace("ä", "a")
    return text

# Request input from the user
user_input = input("Please enter a text: ")

# Call the function and display the result
modified_text = replace_swedish_characters(user_input)
print("Modified Text:", modified_text)