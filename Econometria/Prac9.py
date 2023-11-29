"""
1. Represent the time series and find the classical components(tendency, stationality and seasonality)
2. Determine the extraseasonal component, the seasonal component and the irregular component.
3. Obtain the Autocorrelation Function and the Partial Autocorrelation Function.
4. Diferentiatie in the adequate order.
"""

import pandas as pd
import seaborn as sns


from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


from matplotlib import pyplot as plt

from utilities import (
    check_stationarity,
    format_models,
    generate_all_arima_params,
    best_arima_models,
    suggest_arima_parameters,
    make_series_stationary,
    suggest_sarima_parameters,
)


# Significance level
threshold = 0.05

# Load the CSV file
file_path = "Econometria/MST015.csv"
data = pd.read_csv(file_path)
print(data.head())

######################################### GRAPHS #########################################
print(
    "",
    "\n------------------------------Graph Representation------------------------------",
    "\n",
)
y = data["PASAJEROS"]
data["obs"] = pd.to_datetime(data["obs"], format="%YM%m")


plt.figure(figsize=(10, 6))
plt.plot(
    data["obs"],
    y,
    marker="o",
    linestyle="-",
)  # Line plot with points
plt.axhline(y=0, color="r", linestyle="--")
plt.title("Time Series Plot of PASAJEROS Data")
plt.xlabel("Date")
plt.ylabel("PASAJEROS")
plt.grid(True)
plt.ylim(bottom=y.min())
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()


# Grouping the data by year
data["Year"] = data["obs"].dt.year
grouped_data = data.groupby("Year").agg(["mean", "max", "min"])

print(grouped_data)

# Calculating the range for each year
grouped_data["Range"] = (
    grouped_data["PASAJEROS"]["max"] - grouped_data["PASAJEROS"]["min"]
)

# Preparing data for plotting
mean_values = grouped_data["PASAJEROS"]["mean"]
range_values = grouped_data["Range"]

# Plotting the range mean graph
plt.figure(figsize=(10, 6))
plt.scatter(mean_values, range_values)
plt.title("Range Mean Graph by Year")
plt.xlabel("Mean of PASAJEROS")
plt.ylabel("Range of PASAJEROS")
plt.grid(True)

# Show the plot
# plt.show()

# ----------------------------- ANALYSIS OF THE SEASONAL COMPONENT -----------------------------#
# Extracting month and year from the date
data["Month"] = data["obs"].dt.month

# Creating a pivot table for the annual subseries plot
pivot_data = data.pivot_table(
    values="PASAJEROS", index="Month", columns="Year", aggfunc="mean"
)

# Plotting the annual subseries
plt.figure(figsize=(12, 8))
sns.lineplot(data=pivot_data, dashes=False)
plt.title("Annual Subseries Plot of PASAJEROS Data")
plt.xlabel("Month")
plt.ylabel("PASAJEROS")
plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()

# Show the plot
# plt.show()

# We are using an multiplicatibe model because the seasonal variation is constant over time.
decomposition = seasonal_decompose(data["PASAJEROS"], model="multiplicatibe", period=12)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plotting the components
plt.figure(figsize=(14, 8))

# Plot for the trend component
plt.subplot(411)
plt.plot(data["obs"], data["PASAJEROS"], label="Original")
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

# plt.show()

######################################### Correlation and Autocorrelation #########################################

stationary_series, num_differences = make_series_stationary(data["PASAJEROS"])
print(f" \n Number of differences applied: {num_differences} \n")
check = check_stationarity(stationary_series)


print(f"Analysis of stationarity: {check}\n")
# Gráficos ACF y PACF
print(f"length: {len(stationary_series)}")
lags = 12

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(stationary_series, ax=ax1, lags=lags)
plot_pacf(stationary_series, ax=ax2, lags=lags)

plt.tight_layout()
# plt.show()

params = generate_all_arima_params(3, 1, 1, 12)
print(f"Total number of models: {len(params)}")
print(f"Models: {params}")

best_aic, best_bic = best_arima_models(stationary_series, params)

# Formatting the models for printing
formatted_aic_models = format_models(best_aic)
formatted_bic_models = format_models(best_bic)

# Printing the formatted models
print(f"Best models by AIC:\n{chr(10).join(formatted_aic_models)}")
print(f"---- Best models by BIC:\n{chr(10).join(formatted_bic_models)}")
