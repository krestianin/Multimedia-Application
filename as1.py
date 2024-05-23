import tkinter as tk
from tkinter import filedialog
import wave
import numpy as np
import matplotlib.pyplot as plt

# Function to open file dialog and return the selected file path
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    return file_path

# Function to read the .wav file and return the data and parameters
def read_wave_file(file_path):
    with wave.open(file_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
        
    samples = np.frombuffer(frames, dtype=np.int16)
    samples = np.reshape(samples, (-1, n_channels))
    return samples, framerate

# Function to plot waveforms
def plot_waveform(samples, framerate):
    time = np.arange(samples.shape[0]) / framerate
    plt.figure(figsize=(10, 6))

    # Plot left channel
    plt.subplot(2, 1, 1)
    plt.plot(time, samples[:, 0], color='blue')
    plt.title('Left Channel')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    # Plot right channel
    plt.subplot(2, 1, 2)
    plt.plot(time, samples[:, 1], color='red')
    plt.title('Right Channel')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

# Main function
def main():
    file_path = open_file_dialog()
    if not file_path:
        print("No file selected")
        return

    samples, framerate = read_wave_file(file_path)
    total_samples = samples.shape[0]
    
    print(f"Total number of samples: {total_samples}")
    print(f"Sampling frequency: {framerate} Hz")

    plot_waveform(samples, framerate)

if __name__ == "__main__":
    main()

