from model import SoundData
from view import View
import tkinter as tk

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
            else:
                self.view.update_status("Failed to load or process audio file.")