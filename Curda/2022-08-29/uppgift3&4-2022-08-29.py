dic = {"Sverige": "Stockholm", "Norge": "Olso", "Finland": "Helsingborg"}

dic.update({"Danmark": "Köpenhamn"})

dic.pop("Finland")

set1 = set()

set1.add("Banan")
set1.add("Päron")
set1.add("Äpple")

set2 = set()

set2.add("Kiwi")
set2.add("Ananas")
set2.add("Päron")

final = set1.union(set2)

print(final)