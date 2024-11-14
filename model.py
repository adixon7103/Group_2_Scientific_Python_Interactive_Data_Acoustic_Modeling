## model.py
import librosa
import numpy as np
import pandas as pd

class SoundData:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.duration = None

    def load_audio(self, file_path):
        """Load the audio file and store the necessary data"""
        try:
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)
            self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)
            return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False

    def get_audio_info(self):
        """Return basic audio info as a dictionary"""
        return {
            'Duration (s)': self.duration,
            'Sample Rate (Hz)': self.sample_rate,
            'Number of Samples': len(self.audio_data)
        }