import librosa
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

y, sr = librosa.load(file_path)

# Estimate tempo
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

# Adjust n_fft and hop_length based on tempo
if tempo >= 240:
    n_fft = 2048
    hop_length = 512
elif tempo >= 120:
    n_fft = 1024
    hop_length = 256
else:
    n_fft = 512
    hop_length = 128

# Calculate number of segments in the audio file
n_segments = int(np.ceil(len(y) / (sr * 15)))

# Adjust number of segments and time interval if audio is less than 100 seconds
if len(y) < sr * 100:
    n_segments = int(np.ceil(len(y) / (sr * 5)))
    time_interval = 5
else:
    time_interval = 15

# Initialize arrays for storing results
noise_values = np.zeros(n_segments)
tonal_shift_values = np.zeros(n_segments)

# Analyze each segment of the audio file
for i in range(n_segments):
    # Extract segment of audio signal
    y_segment = y[i * sr * time_interval:(i + 1) * sr * time_interval]

    # Calculate spectrogram
    S = np.abs(librosa.stft(y_segment, n_fft=n_fft, hop_length=hop_length))

    # Calculate average energy in each frequency band
    energy = librosa.feature.spectral_bandwidth(S=S, sr=sr)
    energy_mean = np.mean(energy, axis=1)

    # Calculate noise level in dB
    noise = librosa.amplitude_to_db(librosa.feature.rms(y=y_segment))
    noise_mean = np.mean(noise)

    # Calculate tonal shift
    chroma = librosa.feature.chroma_stft(y=y_segment, sr=sr, hop_length=hop_length)
    tonal_shift = np.mean(np.abs(np.diff(chroma)))

    # Store results
    noise_values[i] = noise_mean
    tonal_shift_values[i] = tonal_shift

# Plot results
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 10))

axs[0].plot(np.arange(n_segments) * time_interval, noise_values, 'ro-')
axs[0].set_ylabel('Noise (dB)')

axs[1].plot(np.arange(n_segments) * time_interval, tonal_shift_values, 'go-')
axs[1].set_ylabel('Tonal Shift')

plt.xlabel('Time (seconds)')
plt.show()
