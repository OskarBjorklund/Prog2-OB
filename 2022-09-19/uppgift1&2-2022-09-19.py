def my_function(*args):

    sum = 0

    if len(args) > 0:
        for i in range(len(args)):
            sum += args[i]
        return sum
    else:
        return("Felaktig inmatning")

print(my_function(1, 2, 3))

def food(s, vegan=False):
    if vegan == True:
        print(f"soja{s}")
    else:
        print(s)
        
food("mjölk")
food("mjölk", True)