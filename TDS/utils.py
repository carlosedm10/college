from matplotlib import pyplot as plt
from numpy.typing import ArrayLike
from typing import Sequence, Optional
from scipy.signal import get_window
import numpy as np


def continuous_time_plot(
    *args: ArrayLike,
    variable_name: str,
    xlabel="Time (s)",
    ylim=None,
    save_path=None,
    line_style="-",  # Default line style
    linewidth=2,  # Adjust the width of the line
    principal_lines=None,
    secondary_lines=None,
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

    if principal_lines is not None:
        for line in principal_lines:
            plt.axvline(x=line, color="r", linestyle="--")

    if secondary_lines is not None:
        for line in secondary_lines:
            plt.axvline(x=line, color="b", linestyle="--")

    if save_path is None:
        plt.show()
    else:
        plt.savefig(f"{save_path}/{variable_name} time plot.png")


def discrete_time_plot(
    *args: ArrayLike,
    variable_name: str,
    xlabel="Muestras (n)",
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


def split_signal_into_frames(
    signal, sample_rate, window_size, window_overlap, window_type="hann"
):
    """
    Split the signal into frames using a sliding window approach
    Args:
    signal (np.array): The input signal
    sample_rate (int): The sample rate of the signal
    window_size (float): The size of the window in seconds
    window_overlap (float): The overlap between consecutive windows in seconds
    window_type (str): The type of window to use

    Returns:
    np.array: The signal split into frames
    """
    window_length = int(window_size * sample_rate)
    step_size = window_length - int(window_overlap * sample_rate)
    window = get_window(window_type, window_length)
    num_frames = int(np.ceil(float(np.abs(len(signal) - window_length)) / step_size))

    # Zero padding at the end to make sure that all frames have equal number of samples
    # without truncating any part of the signal
    pad_signal_length = num_frames * step_size + window_length
    z = np.zeros((pad_signal_length - len(signal)))
    pad_signal = np.append(signal, z)  # Pad signal

    indices = (
        np.tile(np.arange(0, window_length), (num_frames, 1))
        + np.tile(np.arange(0, num_frames * step_size, step_size), (window_length, 1)).T
    )
    frames = pad_signal[indices.astype(np.int32, copy=False)]

    # Apply the window function to each frame
    windowed_frames = frames * window

    return windowed_frames
