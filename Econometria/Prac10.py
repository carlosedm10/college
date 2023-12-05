"""
1. Identifica dos modelos para la parte tendencia y otros dos para la parte esracional usando modelos ARIMA.
2. Utiliza la funcion BestARIMA para obtener los 5 mejores modelos segun AIC y BIC. ¿Estan los modelos anteriores incluidos?
3. Identifica el mejor modelo de los estimados.
4. Predice la produccion de los 3 primeros meses de 1996, incluyendo los intervalos de confianza. 
"""

import numpy as np
import pandas as pd
import seaborn as sns


from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima import auto_arima
from matplotlib import pyplot as plt
from utilities import (
    check_white_noise,
    check_stationarity,
    format_diagnostics,
    make_series_stationary,
    series_decomposition,
    time_plot,
)


# Significance level
threshold = 0.05

# Load the CSV file
file_path = "Econometria/MST007.csv"
data = pd.read_csv(file_path).dropna()
data["obs"] = pd.to_datetime(data["obs"], format="%YM%m")
print(data)

######################################### VISUAL COMPROVATION #########################################

data = data[data["obs"].dt.year <= 1985]
print(f"df_1985: {data}")
y = data["Vehiculos"]
x = data["obs"]

# Time series plot
time_plot(x, y, variable_name="Vehiculos")

# Chosing the model and showing the Decomposition
series_decomposition(data, variable_name="Vehiculos")

######################################### Correlation and Autocorrelation #########################################
lags = 24

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y, ax=ax1, lags=lags)
plot_pacf(y, ax=ax2, lags=lags)

plt.tight_layout()
plt.show()

stationary_series, num_differences, num_seasonal_diff = make_series_stationary(
    data["Vehiculos"]
)
# ----------------------------- First Difference -----------------------------#
plt.figure(figsize=(10, 6))
plt.plot(
    stationary_series,
    marker="o",
    linestyle="-",
)  # Line plot with points
plt.axhline(y=0, color="r", linestyle="--")
plt.title("Time Series Plot of Vehiculos Data")
plt.xlabel("Date")
plt.ylabel("Vehiculos")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

stationary_series = stationary_series.diff().dropna()
# ----------------------------- Second Difference -----------------------------#
plt.figure(figsize=(10, 6))
plt.plot(
    stationary_series,
    marker="o",
    linestyle="-",
)  # Line plot with points
plt.axhline(y=0, color="r", linestyle="--")
plt.title("Time Series Plot of Vehiculos Data")
plt.xlabel("Date")
plt.ylabel("Vehiculos")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(f" \n Number of differences applied: {num_differences}")
print(f" Number of seasonal differences applied: {num_seasonal_diff} \n")
check = check_stationarity(stationary_series)
print(f"Analysis of stationarity: {check}\n")
# Gráficos ACF y PACF
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(stationary_series, ax=ax1, lags=lags)
plot_pacf(stationary_series, ax=ax2, lags=lags)

plt.tight_layout()
plt.show()


######################################### ARIMA #########################################

print("\n----------------------ARIMA Model ----------------------\n")
best_model = auto_arima(
    y,
    m=12,
    seasonal=False,
    trace=False,
    stepwise=True,
    error_action="ignore",
    suppress_warnings=True,
)
print(
    "Best model suggested is:",
    f"\n ARIMA({best_model.order[0]}, {best_model.order[1]}, {best_model.order[2]})({best_model.seasonal_order[0]}, {best_model.seasonal_order[1]}, {best_model.seasonal_order[2]}, {best_model.seasonal_order[3]})",
    f"\n AIC: {best_model.aic()} -------- BIC: {best_model.bic()}",
)
print(best_model.summary())

######################################### WHITE NOISE #########################################

# Checking if residues are white noise
residuals = best_model.resid()
print("\n----------------------White Noise ----------------------\n")
print("White noise test:")

print(format_diagnostics(check_white_noise(residuals, alpha=0.05)))
