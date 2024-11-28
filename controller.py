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