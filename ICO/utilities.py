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


def generate_statistics_for_dataset(
    dataset, filename="survey_statistics.xlsx", cross_val_attributes=[]
):
    # Specified attributes for cross-validation

    # Get the "Downloads" directory path
    downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")

    # Create the full path for the Excel file
    full_path = os.path.join(downloads_directory, filename)

    # Initialize the Excel writer and process each column in the dataset
    with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
        for column in dataset.columns:
            # Skip the cross-validation columns themselves
            if column in cross_val_attributes:
                continue

            # Processing the column
            data = dataset[column]

            # Start with general statistics
            if pd.api.types.is_numeric_dtype(data):
                # Numeric data statistics
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
                # Non-numeric data statistics
                value_counts = data.value_counts()
                statistics_data = pd.DataFrame(
                    {"Variable": value_counts.index, "Frecuencia": value_counts.values}
                )

            # Save initial statistics to Excel
            statistics_data.to_excel(
                writer, sheet_name=column[:31], index=False, startrow=0
            )

            # Cross-validation for specified attributes
            start_row = len(statistics_data) + 2
            for attr in cross_val_attributes:
                cross_val_data = (
                    dataset.groupby(attr)[column].value_counts().unstack().fillna(0)
                )
                # Write cross-validation data to Excel
                cross_val_data.to_excel(
                    writer, sheet_name=column[:31], startrow=start_row, index=True
                )
                # Update start_row for the next block of data
                start_row += len(cross_val_data) + 3
    print(
        f"Survey statistics workbook with cross-validation has been saved in '{full_path}'"
    )
