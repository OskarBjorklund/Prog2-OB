# hantera modulen os, som bl.a. kan skapa och radera mappar
import os
import random

try:
    os.mkdir("txt_files")
    print("Skapat undermapp!")
except: # blir fel ifall t.ex. mappen redan finns
    for i in range(1, 101):
        os.remove(f"txt_files/{i}.txt")    # ta bort fil
    os.rmdir("txt_files")

    os.mkdir("txt_files")
    print("Skapat undermapp!")
    
# öppna fil i undermapp
bingo_file = random.randint(1, 101)

for i in range(1, 101):
    with open(f"txt_files/{i}.txt", "a") as f:
        if i == bingo_file:
            f.write("Bingo")
        else:
            f.write("")

for i in range(1, 101):
    with open(f"txt_files/{i}.txt", "r") as f:
        if f.read() == "Bingo":
            print(i)