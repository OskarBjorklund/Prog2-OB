class Student:
    def __init__(self, fornamn, efternamn, personnummer):
        self.fornamn = fornamn
        self.efternamn = efternamn
        self.personnummer = personnummer

    def __str__(self):
        return f"{self.fornamn} {self.efternamn} {self.personnummer}"
