with open("uppgift1.txt", "r") as f:
    a = f.read().split()
tor = int(a[0])
mor = int(a[1])

torantal = 0
morantal = 0

antal = 40

time = 0

while antal > 0:
    if time % tor == 0:
        antal -= 1
        torantal += 1
    if time % mor == 0:
        antal -= 1
        morantal += 1
    time += 1

time -= 1

if time % tor == 0 and time % mor == 0:
    torantal -= 1
    morantal -= 1

print(f"Tors tid ? {tor}")
print(f"Mors tid ? {mor}")
print(f"Svar: Tor {torantal}, Mor {morantal}")