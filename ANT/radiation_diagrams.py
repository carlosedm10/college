import numpy as np
import matplotlib.pyplot as plt

# Constants
lambda_ = 1  # Wavelength (lambda), you can set this to the actual wavelength you're working with
L = 1 / 4 * lambda_  # Length of the antenna in terms of wavelength
k0 = 2 * np.pi / lambda_  # wavenumber


def u(theta):
    # Calculate u based on the angle theta
    return (k0 * L) / (2 * np.pi) * (np.cos(theta) - 1)


def f_uniform(u):
    # Define the F(u) function using the sinc function
    return L * np.sinc(u)


def f_triangular(u):
    # Define the F(u) function using the sinc function
    return L / 2 * (np.sinc(u / 2)) ** 2


def f_cosine(u):
    # Define the F(u) function using the sinc function
    return 2 * L / np.pi * np.cos(u * np.pi) / (1 - 4 * u**2)


# Find the maximum value of each F(u) for normalization
theta_range = np.linspace(0, np.pi, 1000)


# dN function for normalized radiation pattern
def dN(F, theta):
    F_max = np.max(F(u(theta)))
    return np.abs(F(u(theta))) / F_max * np.abs(np.sin(theta))


# Generate a range of theta values for plotting
theta_values = np.linspace(0, 2 * np.pi, 1000)

# Calculate normalized radiation patterns
dN_uniform = dN(f_uniform, theta_values)
dN_triangular = dN(f_triangular, theta_values)
dN_cosine = dN(f_cosine, theta_values)

# Plot the radiation patterns on a polar plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(theta_values, dN_uniform, label="Uniform")
ax.plot(theta_values, dN_triangular, label="Triangular")
ax.plot(theta_values, dN_cosine, label="Cosine")
ax.set_title(f"Radiation Pattern for L = {L}λ")
ax.legend()
plt.show()
