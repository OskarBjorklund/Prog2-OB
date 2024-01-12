deltagare = int(input("Antal deltagare ? "))

n1, n2 = 0, 1

count = 1

deltagare -= 1

while deltagare > 0:
       nth = n1 + n2
       deltagare -= nth
       # update values
       n1 = n2
       n2 = nth
       count += 1

print(count)