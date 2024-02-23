import sys
import sounddevice as sd
import numpy as np

sys.path.append("/Users/carlosedm10/projects/college/TDS")

from utils import continuous_time_plot, discrete_time_plot
from scipy.io import wavfile


# Path to the .wav files
audio_A1 = "/Users/carlosedm10/projects/college/TDS/P1/Practicas_Practica1_sound1.wav"
audio_SH = "/Users/carlosedm10/projects/college/TDS/P1/Practicas_Practica1_sound2.wav"
audio_MM = "/Users/carlosedm10/projects/college/TDS/P1/Practicas_Practica1_sound3.wav"
audio_A2 = "/Users/carlosedm10/projects/college/TDS/P1/Practicas_Practica1_sound4.wav"
audio_TAP = "/Users/carlosedm10/projects/college/TDS/P1/Practicas_Practica1_sound5.wav"

audios = [audio_A1, audio_SH, audio_MM, audio_A2, audio_TAP]

# Exercise 1.2
freq1, y1 = wavfile.read(audios[0])
freq2, y2 = wavfile.read(audios[1])
freq3, y3 = wavfile.read(audios[2])

# Time vector of 100ms
time_scale = freq1 * 0.1
audio_100ms = y1[:1600]
print(len(audio_100ms))

continuous_time_plot(audio_100ms, variable_name="Audio 100ms", xlabel="Time (ms)")
