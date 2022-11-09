allowed1 = ["a", "e", "i", "o", "u", "y"]
allowed2 = ["a", "e", "i", "o", "u", "y", " ", "."]

def omvandare(mening):
    lista = list(mening)
    omvand = []
    antal_pops = 0
    for i in range(len(lista)-2):
        if lista[i] in allowed1:
                if lista[i+1] not in allowed2 and lista[i+2] not in allowed2:
                    antal_pops += 1
    for i in range(len(lista)-2-antal_pops):
        if lista[i] in allowed1:
                if lista[i+1] not in allowed2 and lista[i+2] not in allowed2:
                    lista.pop(i)
    
    for i in range(len(lista)):
        omvand.append(lista[-1])
        lista.pop(-1)
    print("".join(omvand))
        
antalord = int(input("Antal ord ? "))
omvandare(input("Mening ? "))