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
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Add a label for the highest resonance frequency
        self.frequency_label = tk.Label(root, text="Peak Frequency (Hz): Not computed yet")
        self.frequency_label.pack(pady=20)

        # Add a button to cycle through the frequency plots
        self.cycle_button = tk.Button(self.button_frame, text="Cycle Frequency Plot")
        self.cycle_button.pack(side=tk.LEFT, padx=5)

        # Add a button to combine the plots
        self.combine_button = tk.Button(self.button_frame, text="Combine Plots")
        self.combine_button.pack(side=tk.LEFT, padx=5)

        # Add a button to display the waveform in a new window
        self.display_waveform_button = tk.Button(self.button_frame, text="Display Waveform in New Window")
        self.display_waveform_button.pack(side=tk.LEFT, padx=5)

        # Add a button to display the bar graph
        self.display_bar_graph_button = tk.Button(self.button_frame, text="Display Bar Graph")
        self.display_bar_graph_button.pack(side=tk.LEFT, padx=5)


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