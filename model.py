import librosa
import numpy as np
import pandas as pd
import os
import tempfile
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import soundfile as sf  # Add this import

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

            # Remove metadata from WAV file
            if file_path.lower().endswith('.wav'):
                file_path = self.remove_metadata(file_path)

            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)
            self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)

            # Clean the audio data (e.g., handle missing values and channels)
            self.clean_data()

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

    def remove_metadata(self, wav_file_path):
        """Remove metadata from WAV file"""
        try:
            # Read the audio data and sample rate
            audio_data, sample_rate = sf.read(wav_file_path)
            # Create a temporary file path for the cleaned WAV file
            temp_wav_path = tempfile.mktemp(suffix=".wav")
            # Write the audio data to the new file without metadata
            sf.write(temp_wav_path, audio_data, sample_rate, format='WAV', subtype='PCM_16')
            return temp_wav_path
        except Exception as e:
            print(f"Error removing metadata from WAV file: {e}")
            raise

    def clean_data(self):
        """Clean the audio data by checking for missing values and handling channels."""
        if np.any(np.isnan(self.audio_data)):
            #Fill NaN values with zeros (can be customized as needed)
            self.audio_data = np.nan_to_num(self.audio_data)
            print("Missing values in audio data have been replaced with zeros.")

        #Remove metadata from the audio data
        self.audio_data = self.audio_data[librosa.get_duration(y=self.audio_data, sr=self.sample_rate):]

        # Conversion to mono
        if len(self.audio_data.shape) > 1:
            if self.audio_data.shape[0] > 1:
                print("Stereo to mono conversion: Averaging channels.")
                self.audio_data = np.mean(self.audio_data, axis=0)



    def get_audio_info(self):
        """Return basic audio info as a dictionary"""
        return {
            'Duration (s)': self.duration,
            'Sample Rate (Hz)': self.sample_rate,
            'Number of Samples': len(self.audio_data)
        }

    def compute_highest_resonance(self):
        """Compute the highest resonance frequency from the audio signal"""
        # Apply FFT to convert the time-domain signal into the frequency domain
        fft_result = np.fft.fft(self.audio_data)
        fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT result
        frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / self.sample_rate)  # Frequency values for FFT

        # Ignore the negative frequencies
        positive_frequencies = frequencies[:len(frequencies)//2]
        positive_magnitudes = fft_magnitude[:len(frequencies)//2]

        # Find the index of the highest peak in the positive frequencies
        peak_index = np.argmax(positive_magnitudes)

        # The frequency corresponding to the highest peak
        peak_frequency = positive_frequencies[peak_index]

        return peak_frequency
    
    def compute_low_mid_high_freq(self):
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

        # Compute the total power in each frequency range
        low_freq_power = np.sum(fft_magnitude[low_freq_indices])
        mid_freq_power = np.sum(fft_magnitude[mid_freq_indices])
        high_freq_power = np.sum(fft_magnitude[high_freq_indices])

        return low_freq_power, mid_freq_power, high_freq_power