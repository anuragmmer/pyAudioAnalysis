import os
import numpy as np
import librosa
from pydub import AudioSegment
from tkinter import Tk, filedialog
from tqdm import tqdm

def select_audio_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[
        ("Audio files", "*.wav *.mp3 *.aac *.m4a"),
        ("WAV files", "*.wav"),
        ("MP3 files", "*.mp3"),
        ("AAC files", "*.aac"),
        ("M4A files", "*.m4a")
    ])
    return file_path

def get_user_preference():
    while True:
        response = input("Would you like to see detailed BPM analysis (segment-by-segment and sorted list)? (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' for yes or 'n' for no.")

def convert_to_wav(file_path):
    print("Converting audio to WAV format...")
    try:
        audio = AudioSegment.from_file(file_path)
        wav_path = os.path.splitext(file_path)[0] + "_converted.wav"
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting file to WAV: {e}")
        return None

def beat_detection_and_tempo(audio_path):
    print("Performing beat detection and tempo estimation...")
    try:
        y, sr = librosa.load(audio_path)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        return float(tempo.item() if hasattr(tempo, 'item') else tempo), y, sr
    except Exception as e:
        print(f"Error in beat detection and tempo estimation: {e}")
        return None, None, None

def calculate_segment_bpm(segment, sr):
    try:
        onset_env = librosa.onset.onset_strength(y=segment, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        return float(tempo.item() if hasattr(tempo, 'item') else tempo)
    except Exception as e:
        print(f"Error calculating segment BPM: {e}")
        return 0.0

def process_audio(file_path, print_details=False):
    if not file_path.lower().endswith('.wav'):
        file_path = convert_to_wav(file_path)
        if file_path is None:
            return None, None
    
    overall_tempo, y, sr = beat_detection_and_tempo(file_path)
    if overall_tempo is None:
        return None, None
    
    print(f"Estimated overall tempo: {overall_tempo:.2f} BPM")
    print("Analyzing BPM for each segment...")
    
    segment_duration = 5  # seconds
    hop_length = int(segment_duration * sr)
    
    bpms = []
    total_segments = 0
    for i in tqdm(range(0, len(y), hop_length)):
        segment = y[i:i+hop_length]
        if len(segment) < sr:  # Skip segments shorter than 1 second
            continue
        
        bpm = calculate_segment_bpm(segment, sr)
        total_segments += 1
        if 40 <= bpm <= 250:  # Only add realistic BPM values
            bpms.append(bpm)
        
        if print_details:
            print(f"Segment {total_segments}: Length = {len(segment)} samples, BPM = {bpm:.2f}")
    
    print(f"\nTotal segments analyzed: {total_segments}")
    print(f"Valid BPM values detected: {len(bpms)}")
    
    return bpms, overall_tempo

def main():
    file_path = select_audio_file()
    if not file_path:
        print("No file selected. Exiting.")
        return
    
    print(f"Selected file: {file_path}")
    
    print_details = get_user_preference()
    
    result = process_audio(file_path, print_details)
    if result is None:
        print("Error processing audio. Exiting.")
        return
    
    bpms, overall_tempo = result
    
    if len(bpms) == 0:
        print("No valid BPM values detected in segments.")
        print(f"Overall estimated tempo: {overall_tempo:.2f} BPM")
        return
    
    mean_bpm = np.mean(bpms)
    median_bpm = np.median(bpms)
    std_bpm = np.std(bpms)
    min_bpm = min(bpms)
    max_bpm = max(bpms)
    
    print(f"\nBPM Analysis Summary:")
    print(f"Overall estimated tempo: {overall_tempo:.2f} BPM")
    print(f"Mean segment BPM: {mean_bpm:.2f}")
    print(f"Median segment BPM: {median_bpm:.2f}")
    print(f"Standard deviation: {std_bpm:.2f}")
    print(f"Range: {min_bpm:.2f} - {max_bpm:.2f} BPM")
    rounded_bpm = round(overall_tempo)
    print(f"Rounded BPM: {rounded_bpm}")
    
    if print_details:
        print("\nBPMs in ascending order:")
        sorted_bpms = sorted(bpms)
        for bpm in sorted_bpms:
            print(f"{bpm:.2f}")
    
    if len(bpms) > 1:
        max_diff = max(np.diff(sorted(bpms)))
        if max_diff > 20:
            print("\nALERT: BPM difference between segments exceeds 20!")
            print(f"Maximum BPM difference: {max_diff:.2f}")


if __name__ == "__main__":
    main()