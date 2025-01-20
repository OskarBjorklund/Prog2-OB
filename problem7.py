import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tools import regress

# Ladda in data
moore_data = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\moore.dat')

# Separera data i x (år) och y (antal transistorer per ytenhet)
x = moore_data[:, 0]
y = moore_data[:, 1]

# Logaritmera y för modellen
w = np.log(y)

# Skapa designmatrisen X
X = np.column_stack((np.ones(len(x)), x))

# Utför regression
beta_hat, beta_conf = regress(X, w)

# Prediktera värden
y_hat = X @ beta_hat

# Plotta originaldata och skattad modell
plt.figure(figsize=(8, 6))
plt.scatter(x, w, label='Data', alpha=0.7)
plt.plot(x, y_hat, color='red', label='Skattad modell')
plt.xlabel('År')
plt.ylabel('Antal transistorer per ytenhet')
plt.title('Moores lag - Linjär regression')
plt.legend()
plt.show()

# Residualer
residuals = w - y_hat

# QQ-plot för residualer
plt.figure(figsize=(8, 6))
plt.subplot(2, 1, 1)
stats.probplot(residuals, plot=plt)
plt.title('QQ-plot för residualer')

# Histogram för residualer
plt.subplot(2, 1, 2)
plt.hist(residuals, bins=20, density=True, alpha=0.7)
plt.title('Histogram för residualer')
plt.tight_layout()
plt.show()

# Prediktera antalet transistorer för 2025
x_pred = 2025
X_pred = np.array([1, x_pred])
w_pred = X_pred @ beta_hat
y_pred = np.exp(w_pred)

print(f'Förutsagt antal transistorer per ytenhet år 2025: {y_pred:.2e}')