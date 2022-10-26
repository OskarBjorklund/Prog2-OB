allowed = ["a", "e", "i", "o", "u", "y", " ", "."]

def omvandare(mening):
    lista = list(mening)
    omvand = []
    for i in range(len(lista)-2):
        if lista[i] in allowed:
                if lista[i+1] and lista[i+2] not in allowed:
                    lista.pop(i)
    
    for i in range(len(lista)):
        omvand.append(lista[-1])
        lista.pop(-1)
    print("".join(omvand))
        
antalord = int(input("Antal ord ? "))
omvandare(input("Mening ? "))