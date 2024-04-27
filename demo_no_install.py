"""
Author: Sean Higley

This is a demo that demonstrates this package without running pip install on the local package.
The dependencies will need to be downloaded first. 
check the requirements.txt for such dependencies.

"""

from app.dspwava.Signal import SvSignal
import os, time, logging
from app.dspwava.Filters import high_pass_filter, low_pass_filter, convolve_audio

# create log and log directory for testing
LOG_DIR = os.getcwd() + '\\logs\\'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOGGER = logging.getLogger(__name__)
THIS_SESSION_LOG = LOG_DIR + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt'
logging.basicConfig(filename=THIS_SESSION_LOG,
                    filemode='w',
                    format='%(asctime)s <%(levelname)s> [%(name)s] %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
        
LOGGER.info(f"----------------- Discrete Waveform Analyzer | {time.strftime('%c', time.localtime())} -------------------")
#####
#       DEMO STARTS HERE
# Create a signal
original = SvSignal(filepath=os.getcwd() + '\\test_samples\\ex_wav.wav')
original.toMono()

print(os.getcwd() + '\\test_samples\\ex_wav.wav')
print(f"Sample Rate: {original.getSampleRate()}")
print(f"Duration: {original.getDuration()} seconds")
print(f"Number of Channels: {original.getNumChannels()}")
print(f"Samples: {original.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(original.estimate_frequency()))
print(f'Phase Spectrum: {original.getPhaseSpectrum()}')
print(f'Unwrapped Phase Spectrum: {original.getUnwrappedPhase()}')
print(f"Instantaneous Frequency: {original.getInstantaneousFrequency()}")
original.visualize()
original.visualizePhase()
original.visualizePhaseSpace()

high = high_pass_filter(original.copy(), 1000)
high.toMono()
print(f"Sample Rate: {high.getSampleRate()}")
print(f"Duration: {high.getDuration()} seconds")
print(f"Number of Channels: {high.getNumChannels()}")
print(f"Samples: {high.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(high.estimate_frequency()))
print(f'Phase Spectrum: {high.getPhaseSpectrum()}')
print(f'Unwrapped Phase Spectrum: {high.getUnwrappedPhase()}')
print(f"Instantaneous Frequency: {high.getInstantaneousFrequency()}")
high.visualize()
high.visualizePhase()
high.visualizePhaseSpace()

low = low_pass_filter(original.copy(), 200)
low.toMono()
print(f"Sample Rate: {low.getSampleRate()}")
print(f"Duration: {low.getDuration()} seconds")
print(f"Number of Channels: {low.getNumChannels()}")
print(f"Samples: {low.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(low.estimate_frequency()))
print(f'Phase Spectrum: {low.getPhaseSpectrum()}')
print(f'Unwrapped Phase Spectrum: {low.getUnwrappedPhase()}')
print(f"Instantaneous Frequency: {low.getInstantaneousFrequency()}")
low.visualize()
low.visualizePhase()
low.visualizePhaseSpace()

print('Convolving... may take some time')
convolved = convolve_audio(
    sample_signal = original, 
    impulse_signal = SvSignal(filepath=os.getcwd() + '\\test_samples\\gtr_ir.wav'), 
    normalize = True )

print('Convolving done.')
print(f"Sample Rate: {convolved.getSampleRate()}")
print(f"Duration: {convolved.getDuration()} seconds")
print(f"Number of Channels: {convolved.getNumChannels()}")
print(f"Samples: {convolved.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(convolved.estimate_frequency()))
print(f'Phase Spectrum: {convolved.getPhaseSpectrum()}')
print(f'Unwrapped Phase Spectrum: {convolved.getUnwrappedPhase()}')
print(f"Instantaneous Frequency: {convolved.getInstantaneousFrequency()}")
convolved.visualize()
convolved.visualizePhase()
convolved.visualizePhaseSpace()
# convolved.write(os.getcwd() + '\\test_samples\\output_colvolved.wav')



# resampled_signal:Signal = signal
# resampled_signal.resample(signal.getSampleRate()//2)
# print(f"Sample Rate: {resampled_signal.getSampleRate()}")
# print(f"Duration: {resampled_signal.getDuration()} seconds")
# print(f"Number of Channels: {resampled_signal.getNumChannels()}")
# print(f"Samples: {resampled_signal.getSamples()}")
# print('Estimated Freq: {:.2f} Hz'.format(resampled_signal.estimate_frequency()))
# print(f'Phase Spectrum: {resampled_signal.getPhaseSpectrum()}')
# print(f'Unwrapped Phase Spectrum: {resampled_signal.getUnwrappedPhase()}')
# print(f"Instantaneous Frequency: {resampled_signal.getInstantaneousFrequency()}")





