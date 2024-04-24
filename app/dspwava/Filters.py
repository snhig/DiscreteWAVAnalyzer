from scipy.signal import butter, filtfilt
from .Signal import SvSignal
import numpy as np
def high_pass_filter(signal:SvSignal, cutoff_freq, order=5) -> SvSignal: 
    """In Place modification of the SvSignal object. Applies a high pass filter to the signal.
    
    Uses the butterworth filter to apply the high pass filter.
    """
    signal.validDataCheck()
    nyquist = 0.5 * signal.getSampleRate()
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    signal.data = filtfilt(b, a, signal.data, axis=0)
    return signal

def low_pass_filter(signal:SvSignal, cutoff_freq, order=5) -> SvSignal:
    """In Place modification of the SvSignal object. Applies a low pass filter to the signal.
    
    Uses the butterworth filter to apply the low pass filter.
    """ 
    signal.validDataCheck()
    nyquist = 0.5 * signal.getSampleRate()
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    signal.data = filtfilt(b, a, signal.data, axis=0)
    return signal



def forward_backward_filtering(b, a, data):
    """Applies zero-phase digital filtering using a forward and reverse filter process."""
    # forward pass
    y = apply_filter(b, a, data)
    # reverse data
    y = y[::-1]
    # backward pass
    y = apply_filter(b, a, y)
    # reverse data
    return y[::-1]

def apply_filter(b, a, data):
    """Applies a single pass of the filter using the coefficients b and a."""
    n = max(len(a), len(b))
    x = np.pad(data, (n-1, 0), mode='constant')
    y = np.zeros_like(data)
    # direct form II dig transp
    for i in range(len(data)):
        y[i] = b[0] * x[i+n-1] + np.dot(b[1:], x[i+n-2:i-1:-1]) - np.dot(a[1:], y[i+n-2:i-1:-1])
    return y


def convolve_audio(sample_signal:SvSignal, impulse_signal:SvSignal, normalize:bool=False) -> SvSignal:
    # Load the audio file and impulse response file
    audio, audio_sr = sample_signal.getSamples(), sample_signal.getSampleRate()
    impulse, impulse_sr = impulse_signal.getSamples(), impulse_signal.getSampleRate()

    # Check if sample rates match
    if audio_sr != impulse_sr:
        raise ValueError("Sample rates of audio and impulse response do not match.")
    
    # Handle stereo audio by converting to mono (if necessary)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    if impulse.ndim > 1:
        impulse = np.mean(impulse, axis=1)
    
    # Perform the convolution using numpy's convolve function
    result = np.convolve(audio, impulse, mode='full')
    signal:SvSignal = SvSignal(data=result, sr=audio_sr, channels=1)
    if normalize:
        signal.normalize()
    # Save the resulting audio
    return signal