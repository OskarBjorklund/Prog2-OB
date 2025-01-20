import numpy as np
from scipy.stats import norm

# Ladda data
birth = np.loadtxt(r'C:\Users\oskar\Documents\GitHub\Prog2-OB\birth.dat')

# Definiera filter beroende på rökvanor
non_smokers = (birth[:, 19] < 3)  # Kolumn 20: icke-rökare
smokers = (birth[:, 19] == 3)  # Kolumn 20: rökare

# Extrahera födelsevikt (kolumn 3)
x = birth[non_smokers, 2]  # Icke-rökares barn
y = birth[smokers, 2]  # Rökares barn

# Filtrera bort NaN-värden om det finns några
x = x[~np.isnan(x)]
y = y[~np.isnan(y)]

# Beräkna medelvärden
mean_x = np.mean(x)
mean_y = np.mean(y)

# Beräkna skillnaden i medelvärden
mean_diff = mean_x - mean_y

# Stickprovsstorlekar
n_x = len(x)
n_y = len(y)

# Varians och standardfel
var_x = np.var(x, ddof=1)  # ddof=1 för stickprovsvarians
var_y = np.var(y, ddof=1)
SE = np.sqrt(var_x / n_x + var_y / n_y)

# Konfidensnivå (95%)
alpha = 0.05
z_alpha_2 = norm.ppf(1 - alpha / 2)

# Beräkna konfidensintervall
margin_of_error = z_alpha_2 * SE
lower_bound = mean_diff - margin_of_error
upper_bound = mean_diff + margin_of_error

# Resultat
print(f"Medelvikt för barn till icke-rökare: {mean_x:.2f} gram")
print(f"Medelvikt för barn till rökare: {mean_y:.2f} gram")
print(f"Skillnad i medelvikt: {mean_diff:.2f} gram")
print(f"Konfidensintervall för skillnaden: [{lower_bound:.2f}, {upper_bound:.2f}]")