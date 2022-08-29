def translator(input):
    array = list(input)

    robber = [] #robber = rövare :)

    for i in range(len(array)):
        if array[i] in ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]:
            robber.append(array[i]+"o"+array[i])
        else:
            robber.append(array[i])

    return "".join(robber)

def backwards(input):
    array = list(input)

    back = []

    for i in range(len(array)):
        back.insert(0, array[i])

    return "".join(back)

print(translator("oskar"))
print(backwards("oskar"))