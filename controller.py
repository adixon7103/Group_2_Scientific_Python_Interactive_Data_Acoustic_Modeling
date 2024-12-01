import numpy as np
from model import SoundData
from view import View
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Controller:
    def __init__(self, root):
        self.model = SoundData()
        self.view = View(root)
        self.view.load_button.config(command=self.load_audio)

    def load_audio(self):
        """Handle the audio loading process"""
        file_path = self.view.load_audio()
        if file_path:
            success = self.model.load_audio(file_path)
            if success:
                self.view.update_status(f"Successfully loaded {file_path}")
                info = self.model.get_audio_info()
                self.view.update_info(info)
                # Now display the waveform
                self.display_waveform()
                # Compute and display the highest resonance frequency
                peak_frequency = self.model.compute_highest_resonance()
                self.view.update_frequency(peak_frequency)
                # Display the waveplot of the low, mid, and high frequency components
                self.display_low_mid_high_waveplot()

            else:
                self.view.update_status("Failed to load or process audio file.")

    def display_waveform(self):
        """Display the waveform of the cleaned audio data"""
        # Get the cleaned audio data from the model
        audio_data = self.model.audio_data
        sample_rate = self.model.sample_rate

        # Plot the waveform using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(np.linspace(0, len(audio_data) / sample_rate, len(audio_data)), audio_data)
        ax.set_title("Waveform of the Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=self.view.waveform_frame)  # Plot inside waveform_frame
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_low_mid_high_waveplot(self):
        # Display the waveplot of the low, mid, and high frequency components
        low_freq_power, mid_freq_power, high_freq_power = self.model.compute_low_mid_high_freq()

        # Apply FFT to convert the time-domain signal into the frequency domain
        fft_result = np.fft.fft(self.audio_data)
        fft_magnitude = np.abs(fft_result)
        frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / self.sample_rate)

        # Define frequency ranges
        low_freq_range = (0, 1000)
        mid_freq_range = (1000, 4000)
        high_freq_range = (4000, 20000)

        # Find the indices of the frequencies within the ranges
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        mid_freq_indices = np.where((frequencies >= mid_freq_range[0]) & (frequencies < mid_freq_range[1]))[0]
        high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        # Plot the waveforms for the low, mid, and high frequency ranges
        plt.figure(figsize=(12, 6))
        plt.bar(['Low Frequency', 'Mid Frequency', 'High Frequency'], [low_freq_power, mid_freq_power, high_freq_power])
        plt.xlabel('Frequency Range')
        plt.ylabel('Power')
        plt.title('Low, Mid, and High Frequency Components')
        plt.grid(True)
        plt.show()

    