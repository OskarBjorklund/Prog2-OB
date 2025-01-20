import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rayleigh, norm

# Ladda signaldata
y = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\wave_data.dat')

# Plotta en del av signalen och dess histogram
plt.figure(figsize=(8, 4))

# Signalens första 100 punkter
plt.subplot(1, 2, 1)
plt.plot(y[:100])
plt.title("Del av signalen")
plt.xlabel("Tid")
plt.ylabel("Amplitude")

# ML-skattning av b
n = len(y)
est_ml = np.sqrt(np.sum(y**2) / (2 * n))
print(f"ML-skattning av b: {est_ml:.2f}")

# Signifikansnivå
alpha = 0.05
z_alpha_2 = norm.ppf(1 - alpha / 2)

# Varians och konfidensintervall
var_est_ml = est_ml**2 / n
margin_of_error = z_alpha_2 * np.sqrt(var_est_ml)
lower_bound = est_ml - margin_of_error
upper_bound = est_ml + margin_of_error

print(f"Konfidensintervall för b: [{lower_bound:.2f}, {upper_bound:.2f}]")

# Histogram över signalen
plt.subplot(1, 2, 2)
plt.hist(y, bins=40, density=True, alpha=0.6, color='gray', label="Histogram")

# Lägg till täthetsfunktionen (Rayleigh PDF)
x_grid = np.linspace(np.min(y), np.max(y), 100)
pdf = rayleigh.pdf(x_grid, scale=est_ml)
plt.plot(x_grid, pdf, 'r', label=f"Täthetsfunktion (b: {est_ml:.2f})")

plt.title("Histogram och täthetsfunktion")
plt.xlabel("Värde")
plt.ylabel("Täthet")
plt.legend()
plt.tight_layout()
plt.show()
