with open("input.txt", "r") as f:
    a = f.read().split()
height = int(a[0])
width = int(a[1])
cipher = a[2]

gridline = []
for i in range(width):
    gridline.append("_")
grid = []
for i in range(height):
    grid.append(list(gridline))

final = []

x = 0
reversex = False
y = 0
reversey = False

i = 0
while i < len(cipher):

    if grid[y][x] == "_":
        grid[y][x] = cipher[i]
    else:
        i -= 1

    #Reverse X
    if x == width-1:
        reversex = True
    if x == 0:
        reversex = False
    
    if reversex == True:
        x -= 1
    else:
        x += 1

    #Reverse Y
    if y == height-1:
        reversey = True
    if y == 0:
        reversey = False
    
    if reversey == True:
        y -= 1
    else:
        y += 1

    i += 1

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] != "_":
            final.append(grid[i][j])

print("".join(final))