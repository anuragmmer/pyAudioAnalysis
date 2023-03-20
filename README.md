Here's a Python script that analyzes an audio file's spectral characteristics to measure its noise level and tonal shift. It uses the "librosa" library to perform various audio processing tasks such as loading audio files, estimating tempo, computing spectrograms, and feature extraction. The results of the analysis are plotted using the "matplotlib" library to visualize the noise level and tonal shift over time for each 15-second segment of the audio file.

The code imports the necessary libraries for audio analysis: librosa, numpy, and matplotlib. It also imports the filedialog and tkinter libraries for opening and selecting an audio file. The code then prompts the user to select an audio file using a GUI dialog box, and reads the file using the librosa.load function. The tempo of the audio file is then estimated using the librosa.beat.beat_track function.

Based on the estimated tempo, the n_fft (number of samples in each Fourier transform) and hop_length (number of samples between successive frames) are adjusted. The code then calculates the number of 15-second segments in the audio file and initializes arrays for storing the results. Each 15-second segment of the audio file is then analyzed. For each segment, the code calculates the spectrogram, the average energy in each frequency band, the noise level in dB, and the tonal shift.

Finally, the code plots the results in two subplots: one for noise and one for tonal shift.

Function:

The noise level is calculated by computing the Root Mean Square (RMS) amplitude of the audio signal and converting it to decibels (dB). The tonal shift is calculated by computing the Chroma feature of the audio signal and then taking the absolute difference between consecutive Chroma feature vectors.

The script also adjusts the parameters of the spectrogram calculation (n_fft and hop_length) based on the estimated tempo of the audio file to improve accuracy.

Steps to run the code:
   1. Install Python: If you don't already have Python installed on your computer, go to the official Python website and download the latest version of Python for your operating system. Follow the installation instructions to install Python on your computer.
   2. Install Required Libraries: The code requires several Python libraries to be installed in order to run. The required libraries are librosa, matplotlib, numpy, and tkinter. Open a command prompt or terminal and type the following commands to install the libraries:
     pip install librosa
     pip install matplotlib
     pip install numpy
   3. Download the Code: Download the code and save it as a Python file with a .py extension.
   4. Open a command prompt or terminal on your computer.
   5. Navigate to the directory where the code file is located using the "cd" command. For example, if the code file is located in the "Downloads" folder, type the following command: cd Downloads
   6. Run the Code: Type the following command to run the code:
     python noise_tonal_analyzer.py
   7. Select Audio File: A file dialog box will appear allowing you to select an audio file for analysis. Navigate to the directory where the audio file is located and select the file.
   8. View the Results: After the code finishes running, the results will be displayed in a graph. You can view the graph in the Python IDE or by opening the generated graph image file.

Limitations and errors that can occur in this code include:

1. If the user selects a file format that is not supported by librosa, the code will raise an error.
2. If the audio file is too short, the code may not be able to extract meaningful information from each 15-second segment.
3. If the audio file is of poor quality or has significant background noise, the results may not be accurate.
4. The values of n_fft and hop_length are based on empirical observations and may not be optimal for all types of audio files.
5. The code does not take into account the possibility of multiple tempos or key changes in the audio file.
