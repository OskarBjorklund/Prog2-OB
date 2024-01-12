def checker(input):
    
    final = []
    try:
        for i in range(6):

            if i == 0 or i == 1:
                final.append(int(1-input[i]))
            
            if i == 2 or i == 3 or i == 4:
                final.append(int(2-input[i]))

            if i == 5:
                final.append(int(8-input[i]))
        
        string = [str(x) for x in final]

        print(" ".join(string))

    except:
        
        print("Felaktig input")

integers = [int(x) for x in input().split()]

checker(integers)