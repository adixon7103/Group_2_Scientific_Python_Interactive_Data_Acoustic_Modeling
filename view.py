## view.py
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
            filetypes=[("Audio Files", "*.wav;*mp3")]
        )
        if file_path:
            return file_path
        else:
            return None