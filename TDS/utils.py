from matplotlib import pyplot as plt
from numpy.typing import ArrayLike


def continuous_time_plot(
    *args: ArrayLike,
    variable_name: str,
    xlabel="Date",
    ylim=None,
    save_path=None,
    line_style="-",  # Default line style
    linewidth=2,  # Adjust the width of the line
):
    """
    This function plots a time series plot with the following characteristics:
    - Line plot with points
    - Horizontal line at y=0
    - Title with the name of the variable
    - X and Y axis labels
    - Grid
    - Y axis starts at 0
    - X axis labels rotated 45 degrees

    Args:
    x (pd.Series): X axis values.
    y (pd.Series): Y axis values.
    variable_name (str, optional): Name of the variable to be displayed in the title. Defaults to str.

    xlabel (str, optional): X axis label. Defaults to "Date".
    """
    plt.figure(figsize=(10, 6))
    plt.plot(
        *args,
        linestyle=line_style,  # Specify the line style
        linewidth=linewidth,  # Specify the width of the line
    )
    plt.axhline(
        y=0, color="r", linestyle="-", linewidth=0.5
    )  # Adjusted for consistency
    plt.title(f"Continuous plot of {variable_name}")
    plt.xlabel(xlabel)
    plt.ylabel(variable_name)
    plt.grid(True)
    plt.ylim(bottom=ylim)
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(f"{save_path}/{variable_name} time plot.png")


def discrete_time_plot(
    *args: ArrayLike,
    variable_name: str,
    xlabel="Time (s)",
    ylim=None,
    save_path=None,
    markerfmt="o",  # Default marker format
    linefmt="-",  # Default line format
    markersize=1,  # Adjust the size of the point
    linewidth=0.5,  # Adjust the width of the line
):
    """
    This function plots a time series plot with the following characteristics:
    - Line plot with points
    - Horizontal line at y=0
    - Title with the name of the variable
    - X and Y axis labels
    - Grid
    - Y axis starts at 0
    - X axis labels rotated 45 degrees

    Args:
    x (pd.Series): X axis values.
    y (pd.Series): Y axis values.
    variable_name (str, optional): Name of the variable to be displayed in the title. Defaults to str.

    xlabel (str, optional): X axis label. Defaults to "Date".
    """
    plt.figure(figsize=(10, 6))
    plt.stem(
        *args,
        markerfmt=markerfmt,  # Marker format
        linefmt=linefmt,  # Line format
    )
    plt.setp(plt.gca().lines, markersize=markersize)  # Set marker size
    plt.setp(plt.gca().lines, linewidth=linewidth)  # Set line width

    # plt.axhline(
    #     y=0, color="r", linestyle="--", linewidth=linewidth
    # )  # Adjusted the baseline width for visibility
    plt.title(f"Discrete Plot of {variable_name}")
    plt.xlabel(xlabel)
    plt.ylabel(variable_name)
    plt.grid(True)
    plt.ylim(bottom=ylim)
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(f"{save_path}/{variable_name} time plot.png")
