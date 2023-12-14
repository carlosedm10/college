import numpy as np
import os
from openpyxl import Workbook

from matplotlib import patches
import pandas as pd
from scipy.stats import skew, kurtosis


def add_total_to_legend(ax):
    total_patch = patches.Patch(color="grey", label="Total")
    current_handles, current_labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=[total_patch] + current_handles, labels=["Total"] + current_labels
    )


def generate_statistics_for_survey_dataset(dataset, filename="survey_statistics.xlsx"):
    # Get the "Downloads" directory path
    downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")

    # Create the full path for the Excel file
    full_path = os.path.join(downloads_directory, filename)

    # Initialize the Excel writer and process each column in the dataset
    with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
        for column in dataset.columns:
            data = dataset[column]

            # Check if the data in the column is numeric
            if pd.api.types.is_numeric_dtype(data):
                # Calculate numeric statistics
                statistics_data = pd.DataFrame(
                    {
                        "Variable": [
                            "Recuento",
                            "Promedio",
                            "Desviación Estándar",
                            "Coeficiente de Variación",
                            "Mínimo",
                            "Máximo",
                            "Rango",
                            "Sesgo Estandarizado",
                            "Curtosis",
                        ],
                        "Valor": [
                            data.count(),
                            data.mean(),
                            data.std(),
                            data.std() / data.mean() * 100
                            if data.mean() != 0
                            else np.nan,
                            data.min(),
                            data.max(),
                            data.max() - data.min(),
                            skew(data, nan_policy="omit"),
                            kurtosis(data, nan_policy="omit"),
                        ],
                    }
                )
            else:
                # Calculate frequency for non-numeric data
                value_counts = data.value_counts()
                statistics_data = pd.DataFrame(
                    {"Variable": value_counts.index, "Frecuencia": value_counts.values}
                )

            # Write to a new sheet in the Excel file
            statistics_data.to_excel(
                writer, sheet_name=column[:31], index=False
            )  # Sheet names are limited to 31 characters

    print(f"Survey statistics workbook has been saved in '{full_path}'")
