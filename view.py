import tkinter as tk
from tkinter import filedialog

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("RT60 Tracker")

        self.status_label = tk.Label(root, text="Select an audio file to load.")
        self.status_label.pack(pady=20)

        self.load_button = tk.Button(root, text="Load Audio", command=self.load_audio)
        self.load_button.pack(pady=10)

        self.info_label = tk.Label(root, text="")
        self.info_label.pack(pady=20)

        # Create a frame to hold the waveform plot
        self.waveform_frame = tk.Frame(root)
        self.waveform_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Add a label for the highest resonance frequency
        self.frequency_label = tk.Label(root, text="Peak Frequency (Hz): Not computed yet")
        self.frequency_label.pack(pady=20)

        # Add a button to cycle through the frequency plot
        self.cycle_button = tk.Button(root, text="Cycle Frequency Plot")
        self.cycle_button.pack(pady=10)

    def update_status(self, message):
        """Update the status label to show a message"""
        self.status_label.config(text=message)

    def update_info(self, info_dict):
        """Display audio information"""
        info_text = "\n".join([f"{key}: {value}" for key, value in info_dict.items()])
        self.info_label.config(text=info_text)

    def load_audio(self):
        """Open file dialog to choose an audio file"""
        file_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio Files", "*.wav;*.mp3")]
        )
        if file_path:
            return file_path
        else:
            return None

    def update_frequency(self, frequency):
        """Update the frequency label with the highest resonance frequency"""
        self.frequency_label.config(text=f"Peak Frequency (Hz): {frequency:.2f}")