def liercheck(guesses):
    truth = True
    if guesses[1] == "too high":
        top = guesses[0]
    elif guesses[1] == "too low":
        bottom = guesses[0]

    print(bottom)

inputs = []
while True:
    adder = input()
    if adder == "0":
        break
    else:
        inputs.append(adder)

liercheck(inputs)