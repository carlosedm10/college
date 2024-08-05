"""
Author: Carlos E. Dominguez Martinez

Description:
This script generates phase and polar plots of the array factor for a linear antenna array.
It uses the parameters defined at the beginning of the script to calculate the array factor 
and visualize it in two different ways.

How to Use:
1. Adjust the parameters N, K, D, and ALPHA to match the specifications of your antenna array.
2. Run the script to generate the plots.
3. The phase plot will show the array factor as a function of the phase (ψ).
4. The polar plot will show the array factor in polar coordinates.
"""

import matplotlib.pyplot as plt
import numpy as np

# Parameters
N = 2  # Number of dipoles in the array
K = 2 * np.pi  # Wavenumber (lambda = 1)
D = 3 / 4  # Distance in terms of lambda
ALPHA = 90  # Phase shift in degrees

# Convert alpha to radians
alpha = ALPHA * np.pi / 180

# Psi values for phase plot
psi = np.linspace(-4 * np.pi, 4 * np.pi, 1000)

# Array Factor
fa = np.abs(np.sin(N * psi / 2) / np.sin(psi / 2))
# ------------------------- Plotting -------------------------- #
# Create figure and subplots
fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212, polar=True)

# Phase plot
ax1.plot(psi, fa)
ax1.axvline(x=-K * D + alpha, color="r", linestyle="--")
ax1.axvline(x=K * D + alpha, color="r", linestyle="--")

# Setting x-axis in multiples of pi
ticks = np.arange(-4 * np.pi, 4 * np.pi, np.pi)
ax1.set_xticks(ticks)
ax1.set_xticklabels([f"{int(tick/np.pi)}π" if tick != 0 else "0" for tick in ticks])

# Title and labels for the phase plot
ax1.set_title("Phase Plot of the Array Factor")
ax1.set_xlabel("Phase (ψ)")
ax1.set_ylabel("Array Factor (|F|)")

# Polar plot
theta = np.linspace(0, 2 * np.pi, 500)  # Full polar plot from 0 to 2*pi
psi_polar = K * D * np.cos(theta) + alpha  # Psi values for polar plot

# Adjust the psi_polar with alpha for correct transformation
fa_polar = np.abs(np.sin(N * (psi_polar) / 2) / np.sin((psi_polar) / 2))

# Plotting the array factor in polar coordinates
ax2.plot(theta, fa_polar)

# Add a line indicating the angle for alpha
ax2.axvline(x=np.pi / 2 + alpha, color="r", linestyle="--", linewidth=2)

# Title for the polar plot
ax2.set_title("Polar Plot of the Array Factor")


# Swithc the axes to start from the top
# ax2.set_theta_zero_location("N")


# Display the plots
plt.tight_layout()
plt.show()
