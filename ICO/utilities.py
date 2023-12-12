# Crear una función para agregar el total en la leyenda
from matplotlib import patches


def add_total_to_legend(ax):
    total_patch = patches.Patch(color="grey", label="Total")
    current_handles, current_labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=[total_patch] + current_handles, labels=["Total"] + current_labels
    )
