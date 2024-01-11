from Input_module import inputmodule

def calculate_arithmetic_sum(starting_element, difference, number_of_elements):

    arithmetic_sum = (starting_element+starting_element+difference*(number_of_elements-1))*number_of_elements/2 
    return arithmetic_sum

def calculate_geometric_sum(starting_element, quotient, number_of_elements):

    geometric_sum = starting_element*(quotient**number_of_elements-1)/(quotient-1) 
    return geometric_sum

def collect_arithmetic_attributes():
    starting_element = inputmodule(float, "Mata in första elementet i den aritmetiska summan: ")
    difference = inputmodule(float, "Mata in differensen i den aritmetiska summan: ")
    return starting_element, difference

def collect_geometric_attributes():
    starting_element = inputmodule(float, "Mata in första elementet i den geometriska summan: ")

    quotient = inputmodule(float, "Mata in kvoten mellan elementen i den geometriska summan: ")
    while quotient == 1:
        print("Kvoten får inte vara ett, detta orsakar division med noll. Försök igen.")
        quotient = inputmodule(float, "Mata in kvoten mellan elementen i den geometriska summan: ")
    return starting_element, quotient

def collect_number_of_elements():
    number_of_elements = inputmodule(int, "Mata in antalet element i summorna: ")
    while number_of_elements<1:
        print("Antalet element måste vara större än noll. Försök igen.")
        number_of_elements = inputmodule(int, "Mata in antalet element i summorna: ")
    return number_of_elements

def choose_type_of_sum(message):
    choice_of_sum = input(message)
    while choice_of_sum.upper() != "A" and choice_of_sum.upper() != "G":
        print("Inmatningen måste vara [a] eller [g]. Försök igen.")
        choice_of_sum = input(message)
    return choice_of_sum


def main():

    first_sum_variant = choose_type_of_sum("Är den första summan aritmetisk [a] eller geometrisk [g]: ")
    if first_sum_variant.upper() == "A":
        first_sum_attributes = collect_arithmetic_attributes()
    elif first_sum_variant.upper() == "G":
        first_sum_attributes = collect_geometric_attributes()
    
    second_sum_variant = choose_type_of_sum("Är den andra summan aritmetisk [a] eller geometrisk [g]: ")
    if second_sum_variant.upper() == "A":
        second_sum_attributes = collect_arithmetic_attributes()
    elif second_sum_variant.upper() == "G":
        second_sum_attributes = collect_geometric_attributes()

    number_of_elements = collect_number_of_elements()

    if first_sum_variant.upper() == "A":
        first_sum_value = calculate_arithmetic_sum(first_sum_attributes[0], first_sum_attributes[1], number_of_elements)
    elif first_sum_variant.upper() == "G":
        first_sum_value = calculate_geometric_sum(first_sum_attributes[0], first_sum_attributes[1], number_of_elements)

    if second_sum_variant.upper() == "A":
        second_sum_value = calculate_arithmetic_sum(second_sum_attributes[0], second_sum_attributes[1], number_of_elements)
    elif second_sum_variant.upper() == "G":
        second_sum_value = calculate_geometric_sum(second_sum_attributes[0], second_sum_attributes[1], number_of_elements)

    if first_sum_value>second_sum_value:
        print("Första summan är störst.")
    elif first_sum_value<second_sum_value:
        print("Andra summan är störst.")
    else:
        print("Wow! Summorna är exakt lika stora.")

######################## Main Program ########################
main()