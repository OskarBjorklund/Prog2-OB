def inputmodule(value_type, message):

    continue_running = True

    if value_type == int:
        while continue_running:
            try:
                input_value = int(input(message))
                continue_running = False
            except ValueError:
                print("Inmatningen måste vara ett heltal")

    elif value_type == float:
        while continue_running:
            try:
                input_value = float(input(message))
                continue_running = False
            except ValueError:
                print("Inmatningen måste vara ett flyttal")

    return input_value