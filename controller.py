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
        self.view.cycle_button.config(command=self.cycle_frequency_plot)
        self.view.combine_button.config(command=self.combine_plots)
        self.view.display_waveform_button.config(command=self.display_waveform_in_new_window)
        self.view.display_bar_graph_button.config(command=self.display_bar_graph)
        self.current_freq_range = 'low'  # Initialize with 'low' frequency range
        self.bar_graph_created = False  # Flag to check if the bar graph has been created

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
                # Display the waveplot of the low, mid, and high frequency components
                self.display_low_mid_high_waveplot()
                # Compute and display the highest resonance frequency
                peak_frequency = self.model.compute_highest_resonance()
                self.view.update_frequency(peak_frequency)
            else:
                self.view.update_status("Failed to load or process audio file.")

    def cycle_frequency_plot(self):
        """Cycle through the low, mid, and high frequency plots"""
        if self.current_freq_range == 'low':
            self.current_freq_range = 'mid'
        elif self.current_freq_range == 'mid':
            self.current_freq_range = 'high'
        else:
            self.current_freq_range = 'low'

        self.display_low_mid_high_waveplot()

    def display_waveform(self):
        """Display the waveform of the cleaned audio data"""
        # Get the cleaned audio data from the model
        audio_data = self.model.audio_data
        sample_rate = self.model.sample_rate

        # Plot the waveform using Matplotlib
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(np.linspace(0, len(audio_data) / sample_rate, len(audio_data)), audio_data)
        ax.set_title("Waveform of the Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=self.view.plot_frame)  # Plot inside plot_frame
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_low_mid_high_waveplot(self):
        # Clear the previous plot
        for widget in self.view.plot_frame.winfo_children():
            widget.destroy()

        # Display the waveplot of the low, mid, and high frequency components
        low_freq_power, mid_freq_power, high_freq_power = self.model.compute_low_mid_high_freq()

        # Apply FFT to convert the time-domain signal into the frequency domain
        fft_result = np.fft.fft(self.model.audio_data)
        fft_magnitude = np.abs(fft_result)
        frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / self.model.sample_rate)

        # Define frequency ranges
        low_freq_range = (0, 1000)
        mid_freq_range = (1000, 4000)
        high_freq_range = (4000, 20000)

        # Find the indices of the frequencies within the ranges
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        mid_freq_indices = np.where((frequencies >= mid_freq_range[0]) & (frequencies < mid_freq_range[1]))[0]
        high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        # Plot the waveforms for the current frequency range
        fig, ax = plt.subplots(figsize=(8, 3))
        if self.current_freq_range == 'low':
            ax.plot(frequencies[low_freq_indices], fft_magnitude[low_freq_indices])
            ax.set_title("Low Frequency Component")
        elif self.current_freq_range == 'mid':
            ax.plot(frequencies[mid_freq_indices], fft_magnitude[mid_freq_indices])
            ax.set_title("Mid Frequency Component")
        else:
            ax.plot(frequencies[high_freq_indices], fft_magnitude[high_freq_indices])
            ax.set_title("High Frequency Component")

        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=self.view.plot_frame)  # Plot inside plot_frame
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_bar_graph(self, low_freq_power, mid_freq_power, high_freq_power):
        """Create a bar graph of the low, mid, and high frequency power in a separate window"""
        # Create a new Toplevel window
        bar_graph_window = tk.Toplevel(self.view.root)
        bar_graph_window.title("Frequency Power Distribution")

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(['Low Frequency', 'Mid Frequency', 'High Frequency'], [low_freq_power, mid_freq_power, high_freq_power])
        ax.set_xlabel('Frequency Range')
        ax.set_ylabel('Power')
        ax.set_title('Frequency Power Distribution')
        ax.grid(True)

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=bar_graph_window)  # Plot inside the new window
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def combine_plots(self):
        """Combine the waveform and frequency plots"""
        # Clear the previous plot
        for widget in self.view.plot_frame.winfo_children():
            widget.destroy()

        # Get the cleaned audio data from the model
        audio_data = self.model.audio_data
        sample_rate = self.model.sample_rate

        # Apply FFT to convert the time-domain signal into the frequency domain
        fft_result = np.fft.fft(audio_data)
        fft_magnitude = np.abs(fft_result)
        frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / sample_rate)

        # Define frequency ranges
        low_freq_range = (0, 1000)
        mid_freq_range = (1000, 4000)
        high_freq_range = (4000, 20000)

        # Find the indices of the frequencies within the ranges
        low_freq_indices = np.where((frequencies >= low_freq_range[0]) & (frequencies < low_freq_range[1]))[0]
        mid_freq_indices = np.where((frequencies >= mid_freq_range[0]) & (frequencies < mid_freq_range[1]))[0]
        high_freq_indices = np.where((frequencies >= high_freq_range[0]) & (frequencies < high_freq_range[1]))[0]

        # Plot the combined frequency components
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot the low, mid, and high frequency components together
        ax.plot(frequencies[low_freq_indices], fft_magnitude[low_freq_indices], label="Low Frequency Component")
        ax.plot(frequencies[mid_freq_indices], fft_magnitude[mid_freq_indices], label="Mid Frequency Component")
        ax.plot(frequencies[high_freq_indices], fft_magnitude[high_freq_indices], label="High Frequency Component")
        ax.set_title("Combined Frequency Components")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.legend()

        fig.tight_layout(pad=3.0)

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=self.view.plot_frame)  # Plot inside plot_frame
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_waveform_in_new_window(self):
        """Display the waveform of the cleaned audio data in a new window"""
        # Get the cleaned audio data from the model
        audio_data = self.model.audio_data
        sample_rate = self.model.sample_rate

        # Create a new Toplevel window
        waveform_window = tk.Toplevel(self.view.root)
        waveform_window.title("Waveform")

        # Plot the waveform using Matplotlib
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(np.linspace(0, len(audio_data) / sample_rate, len(audio_data)), audio_data)
        ax.set_title("Waveform of the Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=waveform_window)  # Plot inside the new window
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_bar_graph(self):
        """Display the bar graph of the low, mid, and high frequency power in a separate window"""
        # Compute the low, mid, and high frequency power
        low_freq_power, mid_freq_power, high_freq_power = self.model.compute_low_mid_high_freq()

        # Create a new Toplevel window
        bar_graph_window = tk.Toplevel(self.view.root)
        bar_graph_window.title("Frequency Power Distribution")

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(['Low Frequency', 'Mid Frequency', 'High Frequency'], [low_freq_power, mid_freq_power, high_freq_power])
        ax.set_xlabel('Frequency Range')
        ax.set_ylabel('Power')
        ax.set_title('Frequency Power Distribution')
        ax.grid(True)

        # Convert the Matplotlib plot to a Tkinter widget
        canvas = FigureCanvasTkAgg(fig, master=bar_graph_window)  # Plot inside the new window
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)