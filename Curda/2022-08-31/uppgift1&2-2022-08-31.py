x = 0
while x < 1000:
    x += 1
    if x % 7 == 0:
        print(x)

x = str(input())
array = list(x)
count = 0

for i in range(len(array)):
    proceed = True
    while proceed:
        try:
            x = int(array[i])
            proceed = False
        except:
            break
        else:
            count += 1
print(count)