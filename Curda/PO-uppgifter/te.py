def highestbag(info):
    indicates = [index for index, item in enumerate(info) if item == max(info)]
    return indicates

teabags = int(input("Antal påsar ? "))
participants = int(input("Antal personer ? "))
teabaginfo = []
cans = 0

for i in range(teabags):
    teabaginfo.append(int(input(f"Påse {i+1} räcker till ? ")))

while participants > 0:
    if teabaginfo[highestbag(teabaginfo)[0]] < 10:
        participants -= teabaginfo[highestbag(teabaginfo)[0]]
        teabaginfo[highestbag(teabaginfo)[0]] = 0
        cans += 1
    else:
        participants -= 10
        teabaginfo[highestbag(teabaginfo)[0]] = teabaginfo[highestbag(teabaginfo)[0]] - 10
        cans += 1

print(cans)