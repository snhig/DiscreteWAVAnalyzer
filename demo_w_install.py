"""
Author: Sean Higley

This is a file that demonstrates this package after installing via the setup.bat(windows) 
 or the install isnstructions found in the README.md .

"""

import os, time, logging
from dspwava import SvSignal, high_pass_filter, low_pass_filter, convolve_audio

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
print(' ')
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


