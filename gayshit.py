import re

def convert_multiple_formats(input_str):
    # Split the input string into lines
    lines = input_str.splitlines()
    
    # Process each line
    converted_lines = []
    for line in lines:
        # Replace one or more spaces with a single tab character
        converted_line = re.sub(r'\s+', '\t', line).strip()  # Use strip() to remove any leading/trailing tabs
        converted_lines.append(converted_line)
    
    # Join the converted lines with newline characters
    return '\n'.join(converted_lines)

class Befattning:
    def __init__(self, namn, b, pf, g, lx, lm, mu, fa, syn, fae, ho, tjb):
        self.namn = namn
        self.b = b
        self.pf = pf
        self.g = g
        self.lx = lx
        self.lm = lm
        self.mu = mu
        self.fa = fa
        self.syn = syn
        self.fae = fae
        self.ho = ho
        self.tjb = tjb

    def __repr__(self):
        return (f"Befattning(namn='{self.namn}', b={self.b}, pf={self.pf}, g={self.g}, "
                f"lx={self.lx}, lm={self.lm}, mu={self.mu}, fa={self.fa}, "
                f"syn='{self.syn}', fae={self.fae}, ho='{self.ho}', tjb='{self.tjb}')")

def skapa_befattningar(text):
    befattningar = []
    rader = text.strip().split('\n')
    
    for rad in rader:
        delar = rad.split('\t')
        
        # Debug: Print the parts to check the format
        print(f"Delar: {delar}")
        
        if len(delar) >= 13:
            # Extract parts for `namn` which might span multiple words
            namn = '\t'.join(delar[2:-11]).strip()
            
            # Handle default values for fields
            try:
                b = int(delar[-11]) if delar[-11].isdigit() else 0
            except ValueError:
                b = 0
                
            pf = int(delar[-10]) if delar[-10].isdigit() else 0
            g = int(delar[-9]) if delar[-9].isdigit() else 0
            lx = int(delar[-8]) if delar[-8].isdigit() else 0
            lm = int(delar[-7]) if delar[-7].isdigit() else 0
            mu = int(delar[-6]) if delar[-6].isdigit() else 0
            fa = int(delar[-5]) if delar[-5].isdigit() else 0
            syn = delar[-4]
            fae = int(delar[-3]) if delar[-3].isdigit() else 0
            ho = delar[-2]
            tjb = delar[-1]
                
            befattning = Befattning(namn, b, pf, g, lx, lm, mu, fa, syn, fae, ho, tjb)
            befattningar.append(befattning)

    return befattningar

def filter_befattningar(befattningar):
    filtered = [befattning for befattning in befattningar if befattning.syn == 'C' and befattning.fae == 1]
    return filtered

# Example usage
input_str = """PB	GU	Fallskärmsjägare 	7	7	6	9	2	6	7	A	9	A	A
GB	GU	Fallskärmsjägare 	5	7	5	9	3	7	7	A	9	A	A
GB	GU	Kustjägare (GB)	7	7	6	9	2	6	7	A	9	A	A
GB	GU	Dykare Amfibie	5	7	5	9	3	6	7	A	9	A	A
GB	GU	Jägarsoldat Armen (GB)	7	7	5	9	2	6	7	B	1	A	A
GB	GU	Förstärkningssoldat J-Bat (GB)	5	5	5	9	2	5	6	B	1	A	B
GB	GU	Förstärkningssoldat Jägarförband (GB)	5	5	5	9	2	5	6	B	9	A	B
Menig	GU	Jägarsoldat Armen	5	6	5	9	2	6	7	B	1	A	A
Menig	GU	Förstärkningssoldat J-Bat 	 	5	5	9	2	5	6	B	1	A	B
Menig	GU	Motorcykelordonnans	 	5	4	9	2	3	4	C	1	A	D"""

converted_str = convert_multiple_formats(input_str)
befattningar = skapa_befattningar(converted_str)
filtered_befattningar = filter_befattningar(befattningar)

# Print only the names of the filtered objects
for befattning in befattningar:
    print(befattning)
