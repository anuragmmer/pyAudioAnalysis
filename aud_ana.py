import numpy as np
import librosa
import tkinter as tk
from tkinter import filedialog
import plotly.graph_objects as go

# Prompt user to select audio file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Load audio file
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

# Compute onset strength envelope
onset_env = librosa.onset.onset_strength(y=y, sr=sr)

import matplotlib.pyplot as plt

# Plot onset strength envelope
plt.figure(figsize=(14, 5))
plt.plot(librosa.times_like(onset_env), onset_env, label='Onset Strength')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Onset Strength Envelope')
plt.legend()

# Detect onset times
onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)

# Compute inter-onset intervals (IOIs)
iois = np.diff(onset_times)

# Compute mean and standard deviation of IOIs
ioi_mean = np.mean(iois)
ioi_std = np.std(iois)

# Define threshold for rhythmic change
threshold = ioi_std * 2

# Detect rhythmic changes
changes = []
for i, ioi in enumerate(iois):
    if ioi > threshold:
        start_time = onset_times[i]
        end_time = onset_times[i+1]
        changes.append((start_time, end_time, ioi))

from sklearn.preprocessing import MinMaxScaler

# Normalize noise and tonal shift values
scaler = MinMaxScaler(feature_range=(1, 10))
normalized_noise = scaler.fit_transform(noise_values.reshape(-1, 1)).flatten()
normalized_tonal_shift = scaler.fit_transform(tonal_shift_values.reshape(-1, 1)).flatten()

# Calculate the average of normalized values
average_values = (normalized_noise + normalized_tonal_shift) / 2.0

# Create an interactive scatter plot with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=np.arange(n_segments) * time_interval, y=average_values, mode='lines+markers', name='Average Value'))
fig.update_layout(
    title='Interactive Plot of Average Values',
    xaxis=dict(title='Time (seconds)'),
    yaxis=dict(title='Average Value (Scaled)'),
)
fig.show()

# Plot results
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 10))

axs[0].plot(np.arange(n_segments) * time_interval, noise_values, 'ro-')
axs[0].set_ylabel('Noise (dB)')

axs[1].plot(np.arange(n_segments) * time_interval, tonal_shift_values, 'go-')
axs[1].set_ylabel('Tonal Shift')

plt.xlabel('Time (seconds)')
plt.show()
