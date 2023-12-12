from typing import Callable

def arithmetic(a1, d, n):
    """
    Returnerar artimetisk summa genom tre argument
    """
    return (n*(a1+(a1+d*(n-1))))/2

def geometric(g1, q, n):
    """
    Returnerar geometrisk summa genom tre argument
    """
    return (g1*((q**n)-1))/(q-1)

def get_number(
        string: str, 
        cast: Callable = float, 
        error_message="Felaktig inmatning, försök igen: "
        ):
    """
    "Oskars" funktion för att säkerhetställa att inmatningingen är nummer.
    """
    number = input(string)
    while True:
        try:
            return cast(number)
        except ValueError:
            number = input(error_message)

def get_sum(order, n):
    while not (choice := input(f"Är den {order} summan [a]rtimetisk eller [g]eometrisk? ")) in ["a", "g"]:
        print("Felaktig inmatning. ")

    if choice == "a":
        # Arimetisk talsumma
        print("Data för den aritmetiska summan:")
        a1 = get_number("Skriv in startvärdet (a1): ")
        d = get_number("Skriv in differensen (d): ")

        return arithmetic(a1, d, n)

    elif choice == "g":
        # Geometrisk talsumma
        print("Data för den geometriska summan:")
        g1 = get_number("Skriv in startvärdet (g1): ")

        while (q := get_number("Skriv in kvoten (q): ")) == 1: 
            print("q får inte anta värdet \"1\", försök igen: ")

        return geometric(g1, q, n)
    
print("Antal termer i summorna:")
n = get_number("Skriv in antal element i följden (n): ", cast=int)

a = get_sum("första")
b = get_sum("andra")

if a == b:
    print(f"Summorna är lika")
elif a > b:
    print("Första summan är störst")
else:
    print("Andra summan är störst")