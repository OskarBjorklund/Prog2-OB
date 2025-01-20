import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Ladda data
birth = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\birth.dat')
# Definiera filter beroende på om modern röker (kolonn 20
# är 3) eller inte (kolonn 20 är 1 eller 2). Notera att
# eftersom indexering i Python börjar med noll så betecknas
# kolonn 20 med indexet 19.
non_smokers = (birth[:, 19] < 3)
smokers = (birth[:, 19] == 3)
# Extrahera födelsevikten (kolonn 3) för de två kategorierna.
x = birth[non_smokers, 2]
y = birth[smokers, 2]

x = x[~np.isnan(x)]
y = y[~np.isnan(y)]


# Skapa en stor figur.
plt.figure(figsize=(8, 8))
# Plotta ett låddiagram över x.
plt.subplot(2, 2, 1)
plt.boxplot(x)
plt.axis([0, 2, 500, 5000])

# Plotta ett låddiagram över y.
plt.subplot(2, 2, 2)
plt.boxplot(y)
plt.axis([0, 2, 500, 5000])
# Beräkna kärnestimator för x och y. Funktionen
# gaussian_kde returnerar ett funktionsobjekt som sedan
# kan evalueras i godtyckliga punkter.
kde_x = stats.gaussian_kde(x)
kde_y = stats.gaussian_kde(y)
# Skapa ett rutnät för vikterna som vi kan använda för att
# beräkna kärnestimatorernas värden.
min_val = np.min(birth[:, 2])
max_val = np.max(birth[:, 2])
grid = np.linspace(min_val, max_val, 60)
# Plotta kärnestimatorerna.
plt.subplot(2, 2, (3, 4))
plt.plot(grid, kde_x(grid), 'b')
plt.plot(grid, kde_y(grid), 'r')
plt.show()