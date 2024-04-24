import soundfile as sf
import numpy as np
from scipy import signal
import logging
from .SimplePlot import SvSimplePlot
from .SvSpectrogram import SvSpectrogram
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
LOGGER = logging.getLogger(__name__)
MONO = 'Mono'
STEREO = 'Stereo'
class SvSignal:
    """Signal Object class for reading audio waveforms and performing signal processing operations"""
    def __init__(self, filepath:str=None, data=None, sr=None, channels = 1) -> None:
        self.filepath = filepath
        self.data = data
        self.samplerate = sr
        self.channels = channels
        if filepath != None:
            self.filepath = filepath
            self.data, self.samplerate = sf.read(filepath)
            self.channels = len(self.data.shape)
     
    def copy(self):
        """Returns a copy of the signal object"""
        return SvSignal(filepath=self.filepath, data=self.data.copy(), sr=self.samplerate, channels=self.channels)
            
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
    
    def getAmplitude(self) -> float:
        """Returns the maximum amplitude of the audio signal."""
        self.validDataCheck()
        if self.data.ndim == 1 or self.data.ndim == 2:  # Check for mono or multi-channel data
            amplitude = np.max(np.abs(self.data))
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
    
    
    def visualize(self):
        """Visualizes the signal in a plot"""
        app = QApplication.instance()
        if app == None:
            app = QApplication()
            
        if self.channels == 2:
            plot_l = SvSimplePlot()
            plot_r = SvSimplePlot()
            lay = QVBoxLayout()
            lay.addWidget(plot_l)
            lay.addWidget(plot_r)
            plot = QWidget()
            plot.setLayout(lay)
            samples_l = self.getSamples()[0]
            samples_r = self.getSamples()[1]
            plot_l.draw_signal(np.linspace(0, self.getDuration(), len(samples_l)), samples_l)
            plot_r.draw_signal(np.linspace(0, self.getDuration(), len(samples_r)), samples_r)
            
        else:
            plot = SvSimplePlot()
            plot.draw_signal(np.linspace(0, self.getDuration(), len(self.data)), self.getSamples())
        plot.setWindowTitle('Signal')
        plot.show()
        app.exec()
        
    def visualize_Spect(self):
        """Visualizes the spectrogram of the signal"""
        app = QApplication.instance()
        if app == None:
            app = QApplication()
        spec = SvSpectrogram()
        spec.setWindowTitle('Spectrogram')
        spec.draw(self.getSpectrogram()[2])
        spec.show()
        app.exec()
        
        
    def estimate_frequency(self, frame_size:int=2048, hop_size:int=1024)->float:
        """
         A basic approach to frequency estimation. Adjust the frame_size, hop_size, or other parameters. 
         This function also assumes that the most prominent frequency over time is the one of interest, 
         which works well for signals with a clear and stable dominant frequency.
         
         
         frame_size parameter, also known as the window size, 
         determines the length of each segment of the audio signal that is analyzed at a time
         
         
         hop_size parameter specifies the number of samples to skip before starting a new frame. 
         This defines the overlap between consecutive frames.
         
        """
        self.validDataCheck()
        data = self.data.copy()
        samplerate = self.samplerate
        # If stereo, convert to mono by averaging the two channels
        if len(data.shape) > 1:
            data = data.mean(axis=1)

        # Initialize variables
        max_frequency = 0
        max_magnitude = 0

        # Process audio in frames
        for start in range(0, len(data), hop_size):
            end = start + frame_size
            if end > len(data):
                break
            frame = data[start:end]

            # Apply a window function to reduce spectral leakage
            windowed = frame * np.hanning(len(frame))

            # Compute the FFT and get the magnitude spectrum
            spectrum = np.fft.rfft(windowed)
            magnitude = np.abs(spectrum)

            # Find the peak in the magnitude spectrum
            peak = np.argmax(magnitude)
            frequency = peak * samplerate / len(windowed)

            # Update maximum frequency based on magnitude
            if magnitude[peak] > max_magnitude:
                max_magnitude = magnitude[peak]
                max_frequency = frequency

        return max_frequency
    
    
    def write(self, filepath:str):
        """Writes the signal to a file"""
        self.validDataCheck()
        sf.write(filepath, self.data, self.samplerate)
        LOGGER.info(f'Signal written to {filepath}')
    
    
    