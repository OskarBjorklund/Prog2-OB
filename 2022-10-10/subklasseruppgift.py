class Djur:
    def __init__(self, namn):
        self.namn = namn
class Fagel(Djur):
    def __init__(self, namn, vingspann):
        super().__init__(namn)
        self.vingspann = vingspann
class Fisk(Djur):
    def __init__(self, namn, maxdjup):
        super().__init__(namn)
        self.maxdjup = maxdjup
    def fånga(haj, torsk):
        if torsk.hastighet < 30 and haj.maxdjup >= torsk.maxdjup:
            return True
        else:
            return False
class Torsk(Fisk):
    def __init__(self, namn, maxdjup, hastighet):
        super().__init__(namn, maxdjup)
        self.hastighet = hastighet
class Haj(Fisk):
    def __init__(self, namn, maxdjup, antalTänder):
        super().__init__(namn, maxdjup)
        self.antalTänder = antalTänder

torsk1 = Torsk("per", 45, 20)

haj1 = Haj("Pelle", 100, 100)

print(Fisk.fånga(haj1, torsk1))