import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Parametrar
n = 25  # Antal observationer per simulering
mu = 2  # Sanna värdet på väntevärdet
sigma = 1  # Standardavvikelse
alpha = 0.05  # Ett minus konfidensgraden
m = 100  # Antal simuleringar

# Simulera data och beräkna intervall
x = stats.norm.rvs(loc=mu, scale=sigma, size=(m, n))
xbar = np.mean(x, axis=-1)
lambda_alpha_2 = stats.norm.ppf(1 - alpha / 2)
D = sigma / np.sqrt(n)
undre = xbar - lambda_alpha_2 * D
övre = xbar + lambda_alpha_2 * D

# Plotta konfidensintervallen
plt.figure(figsize=(4, 8))
for k in range(m):
    if övre[k] < mu or undre[k] > mu:
        color = 'r'  # Intervall som inte innehåller mu
    else:
        color = 'b'  # Intervall som innehåller mu
    plt.plot([undre[k], övre[k]], [k, k], color)

# Lägg till det sanna värdet på mu
plt.plot([mu, mu], [-1, m], 'g')
plt.title("Simulerade konfidensintervall")
plt.xlabel("Värden")
plt.ylabel("Simuleringar")
plt.show()

# Räkna hur många intervall som innehåller mu
antal_innehåller_mu = np.sum((undre <= mu) & (övre >= mu))
print(f"Antal intervall som innehåller det sanna värdet på μ: {antal_innehåller_mu} / {m}")
