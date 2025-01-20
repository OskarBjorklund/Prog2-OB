import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rayleigh

# Generera exempeldata (ersätt med din faktiska data)
M = 10000  # Antal observationer
true_b = 4  # Sant värde för Rayleighfördelning
x = rayleigh.rvs(scale=true_b, size=M)

# Beräkna ML- och MK-skattning
est_ml = np.sqrt(np.sum(x**2) / (2 * M))  # ML-skattning
est_mk = np.mean(x) * np.sqrt(2 / np.pi)  # MK-skattning

# Skattningsvärden och etiketter
estimations = [est_ml, est_mk]
labels = ["ML-skattning", "MK-skattning"]

# Iterera över värden och etiketter
for i, label in zip(estimations, labels):
    # Skapa figur
    plt.figure()

    # Visa histogrammet
    plt.hist(x, bins=40, density=True, alpha=0.6, color='gray', label="Histogram")

    # Beräkna och plotta täthetsfunktionen
    x_grid = np.linspace(np.min(x), np.max(x), 100)
    pdf = rayleigh.pdf(x_grid, scale=i)
    plt.plot(x_grid, pdf, 'r', label=f"Täthetsfunktion ({label}: {i:.2f})")

    # Formatera grafen
    plt.title(f"Histogram och täthetsfunktion ({label})")
    plt.xlabel("Värde")
    plt.ylabel("Täthet")
    plt.legend()
    plt.show()