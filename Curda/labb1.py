choice = 0

def aritmetisk(n, a1, d):
    """
    Returnerar artimetisk summa genom tre argument
    """
    return (n*(a1+(a1+d*(n-1))))/2

def geometrisk(g1, q, n):
    """
    Returnerar geometrisk summa genom tre argument
    """
    return (g1*((q**n)-1))/(q-1)

while choice != 3: #Stänger av programmet vid input 3
    
    choice = int(input(""" 
                   1. Artimetisk summa
                   2. Geometrisk summa
                   3. Avsluta
                   """)) #Sitt val
    
    if choice == 1: #Val 1
        n = float(input("Välj längden på talföljden: "))
        a1 = float(input("Välj starttalet: "))
        d = float(input("Välj differansen: "))

        print(f"Den artimetiska summan är: {aritmetisk(n, a1, d)}") #Skriver ut artimetisk summa genom anropning av funktionen artimetisk()

    elif choice == 2: #Val 2
        g1 = float(input("Välj starttalet: "))
        q = float(input("Bestäm kvoten: "))
        n = float(input("Välj längden på talföljden: "))

        print(f"Den geometriska summan är: {geometrisk(g1, q, n)}") #Skriver ut geometrisk summa genom anropning av funktionen geometrisk()