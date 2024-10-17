# BPM Analyzer

## Overview

This script is designed to analyze the tempo (in beats per minute, BPM) of audio files. It provides an overall tempo estimation and can perform segment-by-segment BPM analysis for detailed insights into the audio file's rhythm.

## Why

Analyzing the BPM of audio files is useful for various purposes, such as:
- Music production and DJing, where you need to match tracks with similar BPMs.
- Not limited to musical files only, the script can handle non-musical files as well for most use cases.
- Audio analysis for research purposes.
- Identifying tempo variations within a track.

This script simplifies the process by converting audio files into WAV format (if necessary) and performing BPM calculations automatically.

## What

- The script accepts multiple audio file types (WAV, MP3, AAC, M4A) and converts them into WAV format for processing.
- It estimates the overall BPM of the audio file and, optionally, performs a detailed analysis of BPMs across smaller segments of the track.
- Outputs a summary of the BPM analysis, including mean, median, and standard deviation of the BPMs detected across segments.
- Detects large tempo variations between segments and alerts if there is a significant difference.

## How

### Requirements

Make sure you have the following installed:
- Python 3.x
- `numpy`
- `librosa`
- `pydub`
- `tqdm`
- `tkinter`

You can install these dependencies using pip:

```bash
pip install numpy librosa pydub tqdm
```

### Usage

1. Run the script:
   ```bash
   python bpm_analyser.py
   ```

2. A file selection window will open. Choose the audio file you want to analyze.

3. The script will ask if you'd like to see detailed segment-by-segment BPM analysis. Enter `y` for yes or `n` for no.

4. The script will process the file, convert it to WAV if necessary, and perform beat detection and tempo estimation.

5. The results will be printed in the console, including the overall BPM and a detailed segment analysis (if requested).

### Example Output

```bash
Estimated overall tempo: 128.00 BPM
Total segments analyzed: 12
Valid BPM values detected: 10
Mean segment BPM: 127.50
Median segment BPM: 127.00
Standard deviation: 1.50
Range: 125.00 - 130.00 BPM
Rounded BPM: 128
```

### Notes

- Only realistic BPM values between 40 and 250 are considered valid.
- The script alerts you if there's a significant BPM difference (greater than 20) between segments.
