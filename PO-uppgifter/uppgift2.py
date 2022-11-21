with open("uppgift2.txt", "r") as f:
    a = f.read().split()
temp = list(a[0])
cipher = [int(x) for x in temp]

def check(input):
    validnumbers = []
    for i in range(len(input)-1):
        listnumbers = []
        if input[i] != 0:
            listnumbers.append(input[i])
            if input[i]*10+input[i+1] <= 29:
                listnumbers.append(input[i]*10+input[i+1])
            for i in range(len(listnumbers)):
                if listnumbers[i] == 10 or listnumbers[i] == 20:
                    listnumbers.pop(0)
            validnumbers.append(listnumbers)
    if input[-1] != 0:
        listnumbers.append(input[-1])
        validnumbers.append(listnumbers)
    return validnumbers

combinations = check(cipher)

print(combinations)