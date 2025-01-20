import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import probplot, jarque_bera

# Ladda data från fil
birth = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\birth.dat')

# Variabler att analysera
baby_weight = birth[:, 2]
mother_age = birth[:, 3]
mother_weight = birth[:, 14]
mother_height = birth[:, 15]

# Funktion för att skapa Q-Q-plot
def create_qq_plot(data, title):
    plt.figure(figsize=(6, 6))
    _ = probplot(data[~np.isnan(data)], plot=plt)  # Filtrera NaN
    plt.title(title)
    plt.xlabel("Teoretiska kvantiler")
    plt.ylabel("Empiriska kvantiler")
    plt.show()

# Funktion för att utföra Jarque-Bera-test
def jarque_bera_omit(data):
    jb_stat, p_value = jarque_bera(data[~np.isnan(data)])
    return jb_stat, p_value

# Q-Q-plot och Jarque-Bera-test för varje variabel
for var, title in zip(
    [baby_weight, mother_age, mother_weight, mother_height],
    ["Baby weight", "Mother age", "Mother weight", "Mother height"],
):
    create_qq_plot(var, f"Q-Q plot for {title}")
    jb_stat, p_value = jarque_bera_omit(var)
    print(f"{title}:")
    print(f"Jarque-Bera Statistic: {jb_stat:.2f}, P-value: {p_value:.4f}")
    if p_value < 0.05:
        print(f"{title} avviker från normalfördelning (p < 0.05).\n")
    else:
        print(f"{title} kan antas vara normalfördelad (p >= 0.05).\n")
