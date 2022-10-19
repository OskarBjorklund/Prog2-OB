def liarcheck(guesses):

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(0, len(guesses), 2):
        if guesses[i+1] == "too high":
            for j in range(int(guesses[i])-1, len(numbers)-1):
                numbers[j] = 0
            numbers[int(guesses[i])-1:] 
        elif guesses[i+1] == "too low":
            for j in range(int(guesses[i])):
                numbers[j] = 0
        elif guesses[i+1] == "right on":
            if int(guesses[i]) in numbers:
                print("Stan may be honest")
            else:
                print("Stan is dishonest")
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

inputs = []
while True:
    adder = input()
    if adder == "0":
        break
    else:
        inputs.append(adder)
        
liarcheck(inputs)