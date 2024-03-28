import numpy as np
import matplotlib.pyplot as plt

# Constants
lambda_ = 1  # Wavelength (lambda), you can set this to the actual wavelength you're working with
L = 3.5 * lambda_  # Length of the antenna in terms of wavelength
k0 = 2 * np.pi / lambda_  # wavenumber


def F(u):
    # Define the F(u) function using the sinc function
    return L * np.sinc(u)


def u(theta):
    # Calculate u based on the angle theta
    return (k0 * L) / (2 * np.pi) * (np.cos(theta) - 1)


# Find the maximum value of F(u) for normalization
theta_range = np.linspace(0, np.pi, 1000)
F_max = np.max(F(u(theta_range)))


# dN function for normalized radiation pattern
def dN(theta):
    return np.abs(F(u(theta))) / F_max * np.abs(np.sin(theta))


# Generate a range of theta values for plotting
theta_values = np.linspace(0, 2 * np.pi, 1000)
dN_values = dN(theta_values)

# Plot the radiation pattern on a polar plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(theta_values, dN_values)
ax.set_title(f"Radiation Pattern for L = {L}λ")
plt.show()
