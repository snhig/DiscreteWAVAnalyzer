import soundfile as sf
import numpy as np
from scipy import signal
import logging, time, os, sys
LOGGER = logging.getLogger(__name__)
MONO = 'Mono'
STEREO = 'Stereo'
class Signal:
    """Signal Object class for reading audio waveforms and performing signal processing operations"""
    def __init__(self, filepath:str=None, data=None, sr=None, channels = 1) -> None:
        self.filepath = filepath
        self.data = data
        self.samplerate = data
        self.channels = channels
        if filepath != None:
            self.filepath = filepath
            self.data, self.samplerate = sf.read(filepath)
            self.channels = len(self.data.shape)
            
    def validDataCheck(self):
        """checks if the signal has valid data. If not, raises a ValueError"""
        if self.data is None:
            LOGGER.error('No signal data')
            raise ValueError("No signal data")
               
    def getSampleRate(self)->int:
        """returns sample rate of the signal"""
        self.validDataCheck()
        return self.samplerate
    
    def getSamples(self)->np.ndarray:
        """returns the samples of the signal as a numpy array"""
        self.validDataCheck()
        return self.data
    
    def getDuration(self)->float:
        """returns the duration of the signal in seconds"""
        self.validDataCheck()
        return len(self.data) / self.samplerate
    
    def getNumChannels(self)->int:
        """returns the number of channels in the signal"""
        self.validDataCheck()
        return self.channels
    
    def toMono(self):
        """converts the signal to mono if it is stereo. Does nothing if it is already mono"""
        self.validDataCheck()
        if self.channels == 2:
            self.data = np.mean(self.data, axis=1)
            self.channels = 1
        else:
            LOGGER.info(f'Already in mono')
            
    def resample(self, new_samplerate):
        """resamples the signal to the new sample rate"""
        self.validDataCheck()
        if self.samplerate == new_samplerate:
            LOGGER.info(f'Already at {new_samplerate} Hz')
            return
        old_length = len(self.data)
        num_channels = self.data.shape[1] if len(self.data.shape) > 1 else 1
        # Calculate the ratio between old and new lengths
        ratio = new_samplerate / old_length
        # Generate the indices for the new signal
        indices = np.arange(new_samplerate) / ratio
        # Compute the integer and fractional parts of the indices
        int_indices = indices.astype(int)
        frac_indices = indices - int_indices
        # Linear interpolation for each channel
        resampled_signal = np.zeros((new_samplerate, num_channels))
        for i in range(num_channels):
            if num_channels == 1:
                channel_signal = self.data
            else:
                channel_signal = self.data[:, i]
            resampled_signal[:, i] = (1 - frac_indices) * channel_signal[int_indices] + frac_indices * channel_signal[int_indices + 1]
        self.data = resampled_signal
        self.samplerate = new_samplerate
    
    def getResample(self, new_samplerate):
        """Returns a resampled version of the signal to the new sample rate. The original signal is not modified."""
        self.validDataCheck()
        if self.samplerate == new_samplerate:
            LOGGER.info(f'Already at {new_samplerate} Hz')
            return
        old_length = len(self.data)
        num_channels = self.data.shape[1] if len(self.data.shape) > 1 else 1
        # Calculate the ratio between old and new lengths
        ratio = new_samplerate / old_length
        # Generate the indices for the new signal
        indices = np.arange(new_samplerate) / ratio
        # Compute the integer and fractional parts of the indices
        int_indices = indices.astype(int)
        frac_indices = indices - int_indices
        # Linear interpolation for each channel
        resampled_signal = np.zeros((new_samplerate, num_channels))
        for i in range(num_channels):
            if num_channels == 1:
                channel_signal = self.data
            else:
                channel_signal = self.data[:, i]
            resampled_signal[:, i] = (1 - frac_indices) * channel_signal[int_indices] + frac_indices * channel_signal[int_indices + 1]
        return resampled_signal
    
    def getAmplitude(self)->float:
        self.validDataCheck()
        if len(self.data.shape) == 1:  # Mono signal
            amplitude = np.abs(self.data)
        elif len(self.data.shape) == 2:  # Stereo or multi-channel signal
            amplitude = np.abs(self.data).max(axis=1)
        else:
            raise ValueError("Unsupported number of signal channels")
        return amplitude
    

    def normalize(self, target_amplitude=1.0):
        """normalizes the signal to the specified target amplitude. The original signal is modified."""
        self.validDataCheck()
        if len(self.data.shape) == 1:  # Mono signal
            max_amplitude = self.getAmplitude()
            if max_amplitude == 0:
                return
            scaling_factor = target_amplitude / max_amplitude
            normalized_signal = self.data * scaling_factor
            
        elif len(self.data.shape) == 2:  # Stereo or multi-channel signal
            max_amplitude_per_channel = np.max(np.abs(self.data), axis=0)
            silent_channels = max_amplitude_per_channel == 0
            scaling_factors = np.where(silent_channels, 1.0, target_amplitude / max_amplitude_per_channel)
            normalized_signal = self.data * scaling_factors
        
        else:
            raise ValueError("Unsupported number of signal channels")
        
        self.data = normalized_signal
        
    def getNormalized(self, target_amplitude=1.0)->np.ndarray:
        """returns a normalized version of the signal with the specified target amplitude. The original signal is not modified."""
        if len(self.data.shape) == 1:  # Mono signal
            max_amplitude = self.getAmplitude()
            if max_amplitude == 0:
                return
            scaling_factor = target_amplitude / max_amplitude
            normalized_signal = self.data * scaling_factor
            
        elif len(self.data.shape) == 2:  # Stereo or multi-channel signal
            max_amplitude_per_channel = np.max(np.abs(self.data), axis=0)
            silent_channels = max_amplitude_per_channel == 0
            scaling_factors = np.where(silent_channels, 1.0, target_amplitude / max_amplitude_per_channel)
            normalized_signal = self.data * scaling_factors
        
        else:
            raise ValueError("Unsupported number of signal channels")
        
        return normalized_signal
    
    def getPitchEstimate(self):
        # uisng parabolic interpolation https://ccrma.stanford.edu/~jos/sasp/Sinusoidal_Peak_Interpolation.html
        pass
    
    def getSpectrogram(self, nperseg=256, noverlap=None, nfft=None, window='hann', scaling='density')->tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Returns (f, t, spectrogram) the  array of sample freqs, array of segment lines, and computed spectrogram array of the signal"""
        self.validDataCheck()
        f, t, spectrogram = signal.spectrogram(self.data, fs=self.samplerate, nperseg=nperseg, noverlap=noverlap, nfft=nfft, window=window, scaling=scaling)
        # f: array of sample frequencies
        # t: array of segment times
        # spectrogram: 2D array of power spectral density
        return f,t, spectrogram