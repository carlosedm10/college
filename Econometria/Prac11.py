import pandas as pd

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot as plt
from utilities import (
    check_white_noise,
    format_diagnostics,
    make_series_stationary,
    series_decomposition,
    time_plot,
)

############################################# DEFINITIONS #############################################

# Significance level
threshold = 0.05

# Load the CSV file
file_path = "Econometria/MST007.csv"

data = pd.read_csv(file_path).dropna()  # Drop all NaN values from table
data["obs"] = pd.to_datetime(data["obs"], format="%YM%m")
print(data.head())

variable_name = "Vehiculos"  # Defining the variable name

data = data[data["obs"].dt.year <= 1985]  # Selecting the data until 1985
print(f"df_1985: {data}")
y = data["Vehiculos"]
x = data["obs"]

######################################### VISUAL COMPROVATION #########################################

# Time series plot
time_plot(x, y, variable_name=variable_name, ylim=y.min())

# Chosing the model and showing the Decomposition
# series_decomposition(data, variable_name=variable_name) # Optional

######################################### Correlation and Autocorrelation #########################################

lags = 24

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y, ax=ax1, lags=lags)
plot_pacf(y, ax=ax2, lags=lags)

plt.tight_layout()
plt.show()

stop_differencing = 0
d = 0
# ----------------------------- Diferencing -----------------------------#

# NOTE: make this as many times as necessary

dy = data[variable_name].diff().dropna()

time_plot(dy, variable_name=variable_name)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(dy, ax=ax1, lags=lags)
plot_pacf(dy, ax=ax2, lags=lags)

plt.tight_layout()
plt.show()

######################################### ARIMA MODEL #########################################
print("Write the ARIMA parameters: ")
p = int(input("p: "))
d = int(input("d: "))
q = int(input("q: "))
P = int(input("P: "))
D = int(input("D: "))
Q = int(input("Q: "))
S = int(input("S: "))
model = SARIMAX(y, order=(p, d, q), seasonal_order=(P, D, Q, S))
results = model.fit()
print(results.summary())
