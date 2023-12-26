# Analyse Tempo, Noise, and Tonal Shift of Audio Files

This Python script utilizes the `librosa`, `numpy`, `tkinter`, and `plotly` libraries to perform a detailed analysis of an audio file. The analysis includes estimating tempo, measuring noise levels, and calculating tonal shifts over time. The results are presented in a visual representation using interactive line plots. To understand the graph being plotted and the meaning behind the numbers check: [GUIDE.md](https://github.com/anuragmmer/pyAudioAnalysis/blob/main/GUIDE.md).

## Prerequisites

Before running the script, make sure you have the required libraries installed. You can install them using the following commands:

```bash
pip install numpy librosa tkinter plotly tqdm
```

## Usage

1. Run the script in a Python environment.

2. A file dialog will prompt you to select an audio file for analysis.

3. The script will display the selected audio file path and proceed to load the audio.

4. It estimates the initial tempo with default parameters and then dynamically adjusts parameters for more accurate tempo estimation.

5. The optimal parameters for analysis are printed.

6. The audio file is divided into segments, and the script analyzes each segment, calculating tempo, noise (in dB), and tonal shift over time.

7. A progress bar provides feedback on the analysis progress.

8. The script generates a set of interactive line plots using Plotly, showcasing the temporal evolution of tempo, noise, and tonal shift.

## Additional Information

- The `adjust_parameters` function optimizes the parameters (`n_fft` and `hop_length`) for tempo estimation based on the stability of tempo values over multiple iterations.

- The `moving_average` function applies a moving average to smooth the tempo curve, providing a clearer representation of the overall trend.

- The interactive line plots visualize the changes in tempo, noise levels, and tonal shifts over time, offering insights into the audio's characteristics.

## Dependencies

- [NumPy](https://numpy.org/): For numerical operations.
- [Librosa](https://librosa.org/doc/main/index.html): For audio analysis and processing.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): For creating the file dialog to select an audio file.
- [Plotly](https://plotly.com/python/): For creating interactive plots.
- [tqdm](https://github.com/tqdm/tqdm): For displaying progress bars in the console.

## Notes

- Adjust the parameters as needed for your specific analysis requirements.
- Feel free to customize the script or integrate it into your projects.

## Limitations

- The script assumes that the selected audio file is in a format compatible with the `librosa` library (.mp3/.wav). Ensure that your audio file is supported by `librosa` to avoid potential issues.

- The accuracy of the tempo estimation and parameter adjustment is subject to the characteristics of the input audio file. Noisy or complex audio may affect the reliability of the analysis.

- The script does not handle errors that may arise during the file selection or audio loading process.

- The moving average applied to the tempo curve introduces a trade-off between smoothness and responsiveness to rapid changes. Adjust the `window_size` parameter accordingly based on the desired level of smoothing.
