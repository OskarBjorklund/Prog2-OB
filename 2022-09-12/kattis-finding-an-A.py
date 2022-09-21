def afinder(input):
    array = list(input)

    final = []

    for i in range(len(array)):
        if array[i] == "a":
            for j in range(i, len(array)):
                final.append(array[j])
            break
        else:
            continue
    print("".join(final))

afinder(input())