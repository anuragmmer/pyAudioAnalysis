# Audio BPM and Key Detection Script

This Python script allows you to analyze an audio file (`.mp3`, `.wav`, `.aac`) and determine the **BPM (Beats Per Minute)** and **Key** of the track. It also provides the option to display a graph showing the average BPM every 10 seconds. (Written with the help of AI)

## Features

- Supports `.mp3`, `.wav`, `.aac` audio formats.
- Detects the **musical key** of the audio track.
- Calculates the **average BPM** (main BPM) of the audio track.
- Optionally plots a graph showing the BPM trend across the track.
  
---

## How the Script Works

### BPM Calculation:

To determine the **BPM**, the script uses the following steps:
1. **Filtering Audio**: A **bandpass filter** is applied to isolate the frequency range where beats typically occur (0.5 Hz to 5 Hz).
2. **Autocorrelation**: The filtered audio is divided into 5-second windows. For each window, an **autocorrelation** function is computed to find periodic patterns in the signal.
3. **Peak Detection**: Peaks in the autocorrelation represent beats. By measuring the time intervals between peaks, we can calculate the BPM for each window.
4. **Main BPM**: The script calculates the **mode** (most frequent value) of the BPM across all windows to determine the **main BPM** of the audio track.

### Key Detection:

For detecting the **musical key**, the following steps are used:
1. **Fourier Transform**: The script computes the **Fourier Transform** of the audio data to extract the dominant frequencies in the track.
2. **Peak Frequency Detection**: The script identifies the 10 most prominent frequency peaks.
3. **Mapping to Musical Keys**: The script maps the dominant frequencies to the nearest musical keys using the **equal temperament** scale and assigns a musical note to the strongest peak.

#### Key Formula:
- Musical keys are based on the relation:  
  \[
  \text{Half steps from A4} = 12 \times \log_2\left(\frac{f_{\text{dominant}}}{f_{\text{A4}}}\right)
  \]
  Where \( f_{\text{A4}} \) is 440 Hz and \( f_{\text{dominant}} \) is the dominant frequency.

---

## Libraries Used

### Python Libraries

- `numpy`: Used for numerical computations like the **Fourier Transform** and autocorrelation.
- `scipy`: Provides functions for **signal processing** (e.g., filtering, peak detection, and autocorrelation).
- `pydub`: Converts different audio formats (e.g., `.mp3`, `.aac`) to `.wav` for easy manipulation.
- `matplotlib`: Used to plot the graph of the **BPM** over time.
- `tqdm`: A progress bar library used to show progress during BPM calculation.

---

## Installation

### Prerequisites

- **Python 3.7+**
- **pip** (Python's package manager)

### Installing Dependencies

To install the required libraries, use the following command:

```bash
pip install numpy scipy pydub matplotlib tqdm
```

For **Windows** users, you may also need to install **ffmpeg** to work with `.mp3` and `.aac` files:

- Download **ffmpeg** from: https://ffmpeg.org/download.html
- Add **ffmpeg** to your system's environment **PATH**.

---

## Usage

1. Clone this repository or download the script.
   
2. Open a terminal or command prompt and navigate to the folder containing the script.

3. Run the script using Python:

```bash
python bpm_key.py
```

4. A dialog will appear to let you select an audio file.

5. After selecting the file, the script will:
   - Convert the file to WAV format (if needed).
   - Estimate the **Key** of the audio track.
   - Calculate the **BPM** and show the most frequent BPM (Main BPM).
   - Optionally, it will plot a graph of BPM over time if you choose to view it.

---

## Limitations

1. **BPM Accuracy**: 
   - The **BPM detection** process may struggle with complex or highly syncopated rhythms. The result may be inaccurate for tracks with many variable tempos or unusual time signatures.

2. **Key Detection**:
   - The **key detection** uses a basic mapping of dominant frequencies to musical notes. Tracks with **modulations** (changes in key) or very **complex harmonic structures** may result in incorrect key estimations. Additionally, detecting **minor** keys (versus major) is done by approximation.

3. **Audio Format Conversion**:
   - The script uses `pydub` to convert `.mp3` and `.aac` files to `.wav` for analysis. The quality of conversion may impact results, and this adds overhead to the process.

4. **Processing Time**:
   - For long tracks, the analysis process can take time, expect slower performance on **large files**.

---

## Conclusion

This script provides a simple and effective way to analyze **BPM** and **Key** of audio files, but it does come with some limitations due to the complexity of musical compositions. It is best suited for straightforward tracks with consistent tempo and key. Feel free to explore and improve the algorithm to suit your use cases better!

---

Enjoy using the script and feel free to contribute or report issues! 😊

