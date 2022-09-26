def checker(input):
    
    final = []

    if input[0] != "1":
        final.append(int(1-input[0]))
    else:
        final.append(0)
    
    
    if input[1] != "1":
        final.append(int(1-input[1]))
    else:
        final.append(0)

    
    if input[2] != "2":
        final.append(int(2-input[2]))
    else:
        final.append(0)

    
    if input[3] != "2":
        final.append(int(2-input[3]))
    else:
        final.append(0)

    
    if input[4] != "2":
        final.append(int(2-input[4]))
    else:
        final.append(0)

    
    if input[5] != "8":
        final.append(int(8-input[5]))
    else:
        final.append(0)
    
    string = [str(x) for x in final]

    print(" ".join(string))

integers = [int(x) for x in input().split()]

checker(integers)