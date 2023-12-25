import numpy as np
import librosa
import tkinter as tk
from tkinter import filedialog
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm

def adjust_parameters(y, sr, n_fft, hop_length, convergence_threshold=5, max_iterations=10):
    print("Initializing parameters...")
    for iteration in range(max_iterations):
        print(f"\nIteration {iteration + 1}:")

        tempo_stability = []
        for _ in range(5):  
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
            tempo_stability.append(tempo)

        if np.std(tempo_stability) < convergence_threshold:
            print("Parameters are stable. Exiting parameter adjustment loop.")
            break  
        else:
            n_fft = max(512, n_fft // 2)
            hop_length = max(128, hop_length // 2)
            print(f"Adjusting parameters - n_fft: {n_fft}, hop_length: {hop_length}")

    return n_fft, hop_length

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

print(f"Selected audio file: {file_path}")

y, sr = librosa.load(file_path)

tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
n_fft = 2048
hop_length = 512
n_fft, hop_length = adjust_parameters(y, sr, n_fft, hop_length)
print(f"\nOptimal Parameters - n_fft: {n_fft}, hop_length: {hop_length}")
total_duration = len(y) / sr
time_interval = 1
n_segments = int(np.ceil(total_duration / time_interval))
noise_values = np.zeros(n_segments)
tonal_shift_values = np.zeros(n_segments)
tempo_values = np.zeros(n_segments)
progress_bar = tqdm(total=n_segments, desc="Analyzing Segments", unit="segment")
for i in range(n_segments):
    progress_bar.update(1)
    start_time = i * time_interval
    end_time = (i + 1) * time_interval
    if end_time > total_duration:
        end_time = total_duration
    y_segment = y[int(start_time * sr):int(end_time * sr)]
    S = np.abs(librosa.stft(y_segment, n_fft=n_fft, hop_length=hop_length))
    energy = librosa.feature.spectral_bandwidth(S=S, sr=sr)
    energy_mean = np.mean(energy, axis=1)
    noise = librosa.amplitude_to_db(librosa.feature.rms(y=y_segment))
    noise_mean = np.mean(noise)
    chroma = librosa.feature.chroma_stft(y=y_segment, sr=sr, hop_length=hop_length)
    tonal_shift = np.mean(np.abs(np.diff(chroma)))
    noise_values[i] = noise_mean
    tonal_shift_values[i] = tonal_shift
    tempo_values[i], _ = librosa.beat.beat_track(y=y_segment, sr=sr)
progress_bar.close()
window_size = 5 
smoothed_tempo_values = moving_average(tempo_values, window_size)
fig_subplots = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=['Tempo', 'Noise (dB)', 'Tonal Shift'])
fig_subplots.add_trace(go.Scatter(x=np.arange(n_segments) * time_interval, y=tempo_values, mode='lines+markers', name='Tempo'), row=1, col=1)
fig_subplots.add_trace(go.Scatter(x=np.arange(n_segments - window_size + 1) * time_interval, y=smoothed_tempo_values, mode='lines', name='Smoothed Tempo'), row=1, col=1)
fig_subplots.add_trace(go.Scatter(x=np.arange(n_segments) * time_interval, y=noise_values, mode='lines+markers', name='Noise (dB)'), row=2, col=1)
fig_subplots.add_trace(go.Scatter(x=np.arange(n_segments) * time_interval, y=tonal_shift_values, mode='lines+markers', name='Tonal Shift'), row=3, col=1)
fig_subplots.update_layout(
    height=800,
    width=1200,
    title='Tempo, Noise, and Tonal Shift Over Time',
    xaxis=dict(title='Time (seconds)'),
    yaxis=dict(title='Tempo'),
    yaxis2=dict(title='Noise (dB)'),
    yaxis3=dict(title='Tonal Shift'),
)
fig_subplots.show()
