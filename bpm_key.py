import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
from pydub import AudioSegment
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import collections
from tqdm import tqdm
import time


def select_audio_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.aac")])
    return file_path


def convert_audio_to_wav(file_path):
    print("Converting audio file to WAV format...")
    audio = AudioSegment.from_file(file_path)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    print("Conversion complete!")
    return wav_path


def bandpass_filter(audio_data, sample_rate, lowcut=0.5, highcut=5.0):
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(1, [low, high], btype='band')
    filtered_audio = signal.lfilter(b, a, audio_data)
    return filtered_audio


def calculate_bpm(audio_data, sample_rate, window_size=5):
    window_samples = sample_rate * window_size
    bpm_values = []

    # Bandpass filter to isolate beat frequencies
    filtered_data = bandpass_filter(audio_data, sample_rate)

    print("Analyzing BPM...")
    # Initialize progress bar
    total_windows = len(filtered_data) // window_samples
    with tqdm(total=total_windows, desc="Processing", unit="window") as pbar:
        for i in range(0, len(filtered_data), window_samples):
            window = filtered_data[i:i + window_samples]
            if len(window) < window_samples:
                break

            # Calculate autocorrelation
            corr = signal.correlate(window, window, mode='full')
            corr = corr[len(corr) // 2:]

            # Find peaks in the autocorrelation
            peaks, _ = signal.find_peaks(corr, distance=sample_rate // 2)  # Ensure there's a minimum distance between peaks

            if len(peaks) > 1:
                # Calculate time intervals between peaks
                peak_intervals = np.diff(peaks) / sample_rate  # Time between peaks in seconds
                peak_intervals = peak_intervals[peak_intervals > 0]  # Remove negative or zero intervals

                if len(peak_intervals) > 0:
                    avg_time_per_beat = np.mean(peak_intervals)
                    bpm = 60.0 / avg_time_per_beat
                    if 60 <= bpm <= 180:  # Filter unreasonable BPM values
                        bpm_values.append(bpm)

            pbar.update(1)

    return bpm_values


def estimate_key(audio_data, sample_rate):
    print("Detecting key...")
    # Perform Fourier transform to get frequencies
    fft_result = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)

    # Consider only the positive frequencies
    positive_freqs = frequencies[np.where(frequencies > 0)]
    positive_magnitudes = np.abs(fft_result[np.where(frequencies > 0)])

    # Find the top 10 strongest frequency peaks
    top_indices = np.argsort(positive_magnitudes)[-10:]  # Get indices of the top 10 frequencies
    peak_freqs = positive_freqs[top_indices]

    # Map frequencies to musical keys (approximation)
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    a4_freq = 440.0  # Frequency of A4
    num_keys = len(key_names)

    # Find closest musical key for the dominant frequency
    fundamental_freq = peak_freqs[np.argmax(positive_magnitudes[top_indices])]
    half_steps_from_a4 = int(np.round(12 * np.log2(fundamental_freq / a4_freq)))
    key_index = (half_steps_from_a4 + 9) % num_keys  # Adding 9 to align with C

    return key_names[key_index]


def plot_bpm(bpm_values, window_size=5):
    avg_bpm_per_10s = []
    for i in range(0, len(bpm_values), 2):  # 10s interval (2 windows of 5s)
        avg_bpm = np.mean(bpm_values[i:i+2])  # Average of two 5s windows
        avg_bpm_per_10s.append(avg_bpm)
    
    plt.plot(np.arange(1, len(avg_bpm_per_10s) + 1) * 10, avg_bpm_per_10s, marker='o')
    plt.title("Average BPM Every 10 Seconds")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("BPM")
    plt.show()


def main():
    print("Initializing...")
    file_path = select_audio_file()

    if not file_path:
        print("No file selected")
        return
    
    # Confirm the file name
    confirm = input(f"You selected '{file_path}'. Proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("File selection canceled.")
        return

    print("Loading and converting audio...")
    wav_path = convert_audio_to_wav(file_path)

    # Load WAV file
    print("Processing audio...")
    sample_rate, audio_data = wavfile.read(wav_path)

    # If audio has two channels, take the mean
    if len(audio_data.shape) == 2:
        audio_data = np.mean(audio_data, axis=1)

    # Estimate the key of the audio
    estimated_key = estimate_key(audio_data, sample_rate)
    print(f"Estimated Key: {estimated_key}")

    # Calculate BPM
    bpm_values = calculate_bpm(audio_data, sample_rate)

    # Calculate the mode BPM (main BPM)
    bpm_mode = collections.Counter(np.round(bpm_values)).most_common(1)[0][0]  # Get the most common (mode) BPM
    print(f"Main BPM: {bpm_mode}")

    # Ask the user if they want to plot the graph (y/n)
    show_graph = input("Do you want to see the BPM graph? (y/n): ").strip().lower()

    if show_graph == 'y':
        print("Plotting BPM graph...")
        # Plot BPM values every 10 seconds
        plot_bpm(bpm_values)

    # Clean up temporary WAV file
    print("Cleaning up...")
    os.remove(wav_path)
    

    print("\nProcess complete!")
    print(f"Final Results:\n- Estimated Key: {estimated_key}\n- Main BPM: {bpm_mode}")

if __name__ == "__main__":
    main()
