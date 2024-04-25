# Noise function
from matplotlib import pyplot as plt
from scipy.fftpack import fft

import numpy as np

time = np.linspace(0, 1, 1000)
noise = 5 * np.random.normal(0, 1, 1000)

signal_1 = 4 * np.cos(2 * np.pi * 5 * time)
signal_2 = 3 * np.cos(2 * np.pi * 10 * time + 0.1)

signal = signal_1 + signal_2 + noise

# Calculate the power of the signal and the noise
signal_power = np.sum(np.abs(fft(signal_1 + signal_2)) ** 2) / len(time)
noise_power = np.sum(np.abs(fft(noise)) ** 2) / len(time)

# Calculate the noise to signal ratio
nsr = noise_power / signal_power

# Plot the signal and the noise
plt.figure(figsize=(10, 6))
plt.plot(time, signal_1 + signal_2 + noise, label="Signal")
plt.title(f"Signal with NSR = {nsr:.2f}")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

# Now analizing the spectrum using fft
spectrum = fft(signal)

length = len(spectrum)
t = np.linspace(0, 1, length)
plt.figure(figsize=(10, 6))
plt.plot(t, np.abs(spectrum), label="Spectrum")
plt.title(f"Spectrum with NSR = {nsr:.2f}")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.legend()
plt.show()
