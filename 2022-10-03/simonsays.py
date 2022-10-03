def simoncheck(word):
    check = [str(x) for x in word.split()]

    if check[0] == "simon" and check[1] == "says":
        for i in range(0, 2):
            check.pop(0)
        print(" ".join(check))
    else:
        print("")

inputs = int(input())


for i in range(inputs):
    simoncheck(input())