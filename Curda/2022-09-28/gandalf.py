code = list(input())
sentence = [str(x) for x in input().split()]
check = True


if len(sentence) == len(code):
    for i in range(len(code)):
        for j in range(len(code)):
            if code[i] == code[j]:
                if i == j:
                    continue
                elif sentence[i] != sentence[j]:
                    check = False

    for i in range(len(sentence)):
        for j in range(len(sentence)):
            if sentence[i] == sentence[j]:
                if i == j:
                    continue
                elif code[i] != code[j]:
                    check = False
else:
    check = False

print(check)