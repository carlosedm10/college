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
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima import auto_arima


from matplotlib import pyplot as plt

from utilities import (
    check_white_noise,
    check_stationarity,
    format_diagnostics,
    plot_diagnostics,
    suggest_arima_parameters,
    make_series_stationary,
)


# Significance level
threshold = 0.05

# Load the CSV file
file_path = "Econometria/MST007.csv"
data = pd.read_csv(file_path).dropna()
data["obs"] = pd.to_datetime(data["obs"], format="%YM%m")
print(data)

######################################### GRAPHS #########################################
print(
    "",
    "\n------------------------------Graph Representation------------------------------",
    "\n",
)
data = data[data["obs"].dt.year <= 1985]
print(f"df_1985: {data}")
y = data["Vehiculos"]
x = data["obs"]

# ----------------------------- Time Series Plot -----------------------------#
plt.figure(figsize=(10, 6))
plt.plot(
    data["obs"],
    y,
    marker="o",
    linestyle="-",
)  # Line plot with points
plt.axhline(y=0, color="r", linestyle="--")
plt.title("Time Series Plot of Vehiculos Data")
plt.xlabel("Date")
plt.ylabel("Vehiculos")
plt.grid(True)
plt.ylim(bottom=y.min())
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------- Mean range graph -----------------------------#
# Grouping the data by year
data["Year"] = data["obs"].dt.year
grouped_data = data.groupby("Year").agg(["mean", "max", "min"])


# Calculating the range for each year
grouped_data["Range"] = (
    grouped_data["Vehiculos"]["max"] - grouped_data["Vehiculos"]["min"]
)

# Preparing data for plotting
mean_values = grouped_data["Vehiculos"]["mean"]
range_values = grouped_data["Range"]
# Calculate the slope and intercept of the line
slope, intercept = np.polyfit(mean_values, range_values, 1)

# Plotting the range mean graph
plt.figure(figsize=(10, 6))
plt.scatter(mean_values, range_values)
plt.plot(
    mean_values, slope * mean_values + intercept, color="red"
)  # Add the linear equation to the plot

plt.title("Range Mean Graph by Year")
plt.xlabel("Mean of Vehiculos")
plt.ylabel("Range of Vehiculos")
plt.grid(True)
plt.show()


######################################### ANALYSIS OF THE SEASONAL COMPONENT #########################################
# Extracting month and year from the date
data["Month"] = data["obs"].dt.month

# Creating a pivot table for the annual subseries plot
pivot_data = data.pivot_table(
    values="Vehiculos", index="Month", columns="Year", aggfunc="mean"
)

# Plotting the annual subseries
plt.figure(figsize=(12, 8))
sns.lineplot(data=pivot_data, dashes=False)
plt.title("Annual Subseries Plot of Vehiculos Data")
plt.xlabel("Month")
plt.ylabel("Vehiculos")
plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# We are using an multiplicatibe model because the seasonal variation is constant over time.
decomposition = seasonal_decompose(data["Vehiculos"], model="multiplicatibe", period=12)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plotting the components
plt.figure(figsize=(14, 8))

# Plot for the trend component
plt.subplot(411)
plt.plot(data["obs"], data["Vehiculos"], label="Original")
plt.legend(loc="best")
plt.title("Original Time Series")
plt.grid(True)
plt.xlim(data["obs"][0])
plt.xticks(rotation=45)
plt.tight_layout()

# Plot for the trend component
plt.subplot(412)
plt.plot(data["obs"], trend, label="Trend")
plt.legend(loc="best")
plt.grid(True)
plt.xlim(data["obs"][0])

plt.xticks(rotation=45)
plt.tight_layout()

# Plot for the seasonal component
plt.subplot(413)
plt.plot(data["obs"], seasonal, label="Seasonality")
plt.legend(loc="best")
plt.grid(True)
plt.xlim(data["obs"][0])

plt.xticks(rotation=45)
plt.tight_layout()

# Plot for the residual component
plt.subplot(414)
plt.plot(data["obs"], residual, label="Residuals")
plt.legend(loc="best")
plt.grid(True)
plt.xlim(data["obs"][0])

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

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

# Obtén los valores de ACF y PACF
acf_vals = acf(stationary_series, nlags=lags)
pacf_vals = pacf(stationary_series, nlags=lags)

# Suponiendo un intervalo de confianza del 95%
confidence_level = 1.96

# Sugerir valores de p y q
p, q = suggest_arima_parameters(acf_vals, pacf_vals, confidence_level)


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
plot_diagnostics(residuals)
