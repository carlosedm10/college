import pandas as pd

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

############################################# DEFINITIONS #############################################

# Significance level
threshold = 0.05

# Load the CSV file
file_path = "Econometria/MST007.csv"

data = pd.read_csv(file_path).dropna()
data["obs"] = pd.to_datetime(data["obs"], format="%YM%m")
print(data.head())

data = data[data["obs"].dt.year <= 1985]
print(f"df_1985: {data}")
y = data["Vehiculos"]
x = data["obs"]

######################################### VISUAL COMPROVATION #########################################


# Time series plot
time_plot(x, y, variable_name="Vehiculos")

# Chosing the model and showing the Decomposition
series_decomposition(data, variable_name="Vehiculos")

lags = 24

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y, ax=ax1, lags=lags)
plot_pacf(y, ax=ax2, lags=lags)

plt.tight_layout()
plt.show()
