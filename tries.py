import math

# Datos proporcionados
sigma_0 = 42.47 * 10**-12  # en segundos
D = 17 * 10**-6  # s/nm/km convertido a s/m
lambda_m = 1.55 * 10**-6  # micrómetros a metros
c = 3 * 10**8  # velocidad de la luz en m/s
L_60km = 60 * 10**3  # en metros
L_85km = 85 * 10**3  # en metros
C = 3
# Cálculo de Beta_2
beta_2 = -D * lambda_m**2 / (2 * math.pi * c)

# Calcular el factor para 60 km
factor_60km = beta_2 * L_60km / (2 * sigma_0**2)
sigma_60km = sigma_0 * math.sqrt(
    (1 - C * beta_2 * L_60km / (2 * sigma_0**2)) ** 2 + factor_60km**2
)

# Calcular el factor para 85 km
factor_85km = beta_2 * L_85km / (2 * sigma_0**2)
sigma_85km = sigma_0 * math.sqrt(
    (1 - C * beta_2 * L_85km / (2 * sigma_0**2)) ** 2 + factor_85km**2
)

# Calcular la tasa de transmisión máxima B a partir de las sigmas calculadas
B_60km = 1 / (4 * sigma_60km)
B_85km = 1 / (4 * sigma_85km)

# Imprimir los resultados
print("Cálculo de Beta_2:")
print(f"Beta_2: {beta_2:.2e} s^2/m\n")

print("Cálculo de sigma para 60 km:")
print(f"Factor para 60 km: {factor_60km:.2e}")
print(f"Sigma para 60 km: {sigma_60km:.2e} s")
print(f"Tasa de transmisión máxima para 60 km: {B_60km / 10**9:.2f} Gb/s\n")

print("Cálculo de sigma para 85 km:")
print(f"Factor para 85 km: {factor_85km:.2e}")
print(f"Sigma para 85 km: {sigma_85km:.2e} s")
print(f"Tasa de transmisión máxima para 85 km: {B_85km / 10**9:.2f} Gb/s\n")
