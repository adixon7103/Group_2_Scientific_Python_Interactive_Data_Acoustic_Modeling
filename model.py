import librosa
import numpy as np
import pandas as pd
import os
import tempfile
from scipy.io.wavfile import write
from pydub.utils import mediainfo  # This can help us gather metadata information


class SoundData:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.duration = None
        self.file_path = None

    def load_audio(self, file_path):
        """Load audio file"""
        try:
            self.file_path = file_path
            # Check if the file is MP3 and convert to WAV
            if file_path.lower().endswith('.mp3'):
                file_path = self.convert_mp3_to_wav(file_path)

            # Check for metadata (optional)
            self.check_metadata(file_path)

            # Load the audio file with librosa
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)

            # Handle multi-channel audio and metadata
            self.clean_data()

            self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)

            return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False

    def convert_mp3_to_wav(self, mp3_file_path):
        """Convert MP3 to WAV format using librosa"""
        try:
            # Using librosa to load MP3 and then save it as WAV
            audio_data, sample_rate = librosa.load(mp3_file_path, sr=None)
            # Create a temporary file path for the WAV file
            temp_wav_path = tempfile.mktemp(suffix=".wav")
            # Save the WAV file using scipy
            write(temp_wav_path, sample_rate, (audio_data * 32767).astype(np.int16))  # Save as 16-bit PCM
            return temp_wav_path
        except Exception as e:
            print(f"Error converting MP3 to WAV: {e}")
            raise

    def check_metadata(self, file_path):
        """Check and print metadata information (optional)"""
        try:
            # Using pydub's mediainfo to gather metadata from the file
            metadata = mediainfo(file_path)
            print("Metadata:", metadata)  # Prints metadata for debugging

            # You can add checks for specific metadata here if needed
            # For example, checking if there is any non-empty title, artist, etc.
            if 'tags' in metadata and metadata['tags']:
                print("Tags found in metadata:", metadata['tags'])
            else:
                print("No metadata tags found.")
        except Exception as e:
            print(f"Error reading metadata: {e}")
            pass  # Metadata handling is optional, so we can skip if this fails

    def clean_data(self):
        """Clean the audio data by checking for missing values and handling channels."""
        if np.any(np.isnan(self.audio_data)):
            # Fill NaN values with zeros (can be customized as needed)
            self.audio_data = np.nan_to_num(self.audio_data)
            print("Missing values in audio data have been replaced with zeros.")

        # Handle multi-channel (stereo) to mono conversion
        if len(self.audio_data.shape) > 1:
            if self.audio_data.shape[0] > 1:
                print("Stereo to mono conversion: Averaging channels.")
                self.audio_data = np.mean(self.audio_data, axis=0)
                # Ensure that the audio data is now mono (1D array)
            else:
                print("Single channel audio detected.")

        # Optional: Perform any other required cleaning steps

    def get_audio_info(self):
        """Return basic audio info as a dictionary"""
        return {
            'Duration (s)': self.duration,
            'Sample Rate (Hz)': self.sample_rate,
            'Number of Samples': len(self.audio_data),
            'Channels': 1 if len(self.audio_data.shape) == 1 else 2  # Add channel info
        }