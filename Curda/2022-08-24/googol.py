def googolTime(h, min):

    minutes = (10**100+min)

    hours = minutes // 60

    hours = hours + h

    return (hours % 24, minutes % 60)

print(googolTime(14, 2))