dkuvert = int(input("Kuvert ? "))
daffisch = int(input("Affisch ? "))
dblad = int(input("Blad ? "))
print("svar:", "{0:.4f}".format(2*0.229*0.324*dkuvert + 2*0.297*0.42*daffisch + 0.210*0.297*dblad))