import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patches
from scipy.stats import skew, kurtosis
from tabulate import tabulate


def add_total_to_legend(ax):
    total_patch = patches.Patch(color="grey", label="Total")
    current_handles, current_labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=[total_patch] + current_handles, labels=["Total"] + current_labels
    )


def plot_statistics(data):
    # Calculate the required statistics
    count = len(data)
    mean = np.mean(data)
    std_dev = np.std(data)
    coefficient_of_variation = (std_dev / mean) * 100
    min_value = np.min(data)
    max_value = np.max(data)
    data_range = max_value - min_value
    skewness = skew(data)
    kurt = kurtosis(data)

    # Create a list of tuples for the statistics
    statistics_data = [
        ("Recuento", count),
        ("Promedio", mean),
        ("Desviación Estándar", std_dev),
        ("Coeficiente de Variación", coefficient_of_variation),
        ("Mínimo", min_value),
        ("Máximo", max_value),
        ("Rango", data_range),
        ("Sesgo Estandarizado", skewness),
        ("Curtosis", kurt),
    ]

    # Generate the table
    table = tabulate(statistics_data, headers=["Variable", "Valor"], tablefmt="grid")

    return table
