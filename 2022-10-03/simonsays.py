def simoncheck(word):
    check = [str(x) for x in word.split()]

    if check[0] == "Simon" and check[1] == "says":
        for i in range(0, 2):
            check.pop(0)
        return(" ".join(check))

inputs = int(input())
printlist = []

for i in range(inputs):
    printlist.append(simoncheck(input()))

for i in range(len(printlist)):
    if printlist[i] == None:
        continue
    else: 
        print(printlist[i])