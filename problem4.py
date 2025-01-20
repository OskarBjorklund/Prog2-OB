import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Ladda data
birth = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\birth.dat')

# Definiera filter beroende på rökvanor
non_smokers = (birth[:, 19] < 3)  # Kolumn 20: icke-rökare
smokers = (birth[:, 19] == 3)  # Kolumn 20: rökare

# Extrahera födelsevikt (kolumn 3)
x = birth[non_smokers, 2]  # Icke-rökares barn
y = birth[smokers, 2]  # Rökares barn

# Skapa figur för histogram och KDE
plt.figure(figsize=(8, 8))

# Histogram för icke-rökare
plt.subplot(2, 1, 1)
plt.hist(x, bins=40, density=True, alpha=0.6, color='blue', label="Icke-rökare")
plt.title("Födelsevikt: Icke-rökare")
plt.xlabel("Vikt (gram)")
plt.ylabel("Täthet")
plt.legend()

# Histogram för rökare
plt.subplot(2, 1, 2)
plt.hist(y, bins=40, density=True, alpha=0.6, color='red', label="Rökare")
plt.title("Födelsevikt: Rökare")
plt.xlabel("Vikt (gram)")
plt.ylabel("Täthet")
plt.legend()

plt.tight_layout()
plt.show()

# KDE för att jämföra tätheter
plt.figure(figsize=(8, 4))
kde_x = gaussian_kde(x)
kde_y = gaussian_kde(y)
grid = np.linspace(min(birth[:, 2]), max(birth[:, 2]), 100)

plt.plot(grid, kde_x(grid), label="Icke-rökare (KDE)", color='blue')
plt.plot(grid, kde_y(grid), label="Rökare (KDE)", color='red')
plt.title("Kärntäthet för födelsevikt")
plt.xlabel("Vikt (gram)")
plt.ylabel("Täthet")
plt.legend()
plt.show()
