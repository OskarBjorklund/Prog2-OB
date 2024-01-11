class Elev:
    def __init__(self, namn, ålder, godkänd):
        self.namn = namn
        self.ålder = ålder
        self.godkänd = godkänd
    
    def presentera(self):
        if self.godkänd == True:
            return(f"Hej jag heter {self.namn} och är {self.ålder} och just nu är jag glad för jag fick godkänt")
        else:
            return(f"Hej jag heter {self.namn} och är {self.ålder} och just nu är jag ledsen för jag inte fick godkänt")

Axel = Elev("Axel Brandel", "18", True)

print(Elev.presentera(Axel))