with open("input.txt", "r") as f:
    kuber = f.read()

kuber = int(kuber)

antal = 0

for i in range(kuber):
    antal += (i+1)**3

print(f"Antal: {antal}")