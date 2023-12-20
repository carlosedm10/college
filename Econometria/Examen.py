import os
import pandas as pd

from utilities import autocorrelation_plots

############################# SET UP #############################
save_path = os.path.join(os.path.expanduser("~"), "Downloads")

# Load the CSV file
file_path = "Econometria/MRD003.csv"

data = pd.read_csv(file_path).dropna()  # Drop all NaN values from table
print(data.head(10))

variable_name = "RENTA"  # Defining the variable name

autocorrelation_plots(
    series=data[variable_name],
    lags=6,
    variable_name=variable_name,
    save_path=save_path,
)
