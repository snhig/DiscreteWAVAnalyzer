# DiscreteWAVAnalyzer

At a high level, I aim to create a python package that enables discrete signal analysis. The user would be able to import the package
into their scripts or object oriented programs to analyze discrete waveform and audio-files. The package would abstract the user from
dealing with byte unpacking, writing their own algorithms, and/or creating spectrograms/graphs.

The specific objectives of this study are to develop a python package that enables the user to perform signal analysis on discrete
waveform and audio-files. The package should provide functions to extract features from the signal, such as frequency, amplitude, and
phase. The user should be able to, optionally, generate visualizations of the signal, including spectrograms (not using pre-built
spectrogram packages) and waveforms.


### [3/13/24 Snapshot 1](https://github.com/snhig/DiscreteWAVAnalyzer/wiki/Snapshot-1)

## Install Instructions

1. Clone this repositry
2. Navigate to the root direcotry .\DiscreteWAVAnalyzer
3. Ensure you have pip and setuptools installed by running:

    `python -m pip install setuptools`
    
4. Install this package with the following commands:
   
    `python .\setup.py bdist_wheel sdist`

    `python -m pip install .`

5. Access packge in python using:
        
```python
from dspwava import SvSignal, high_pass_filter, low_pass_filter, convolve_audio
audio_filepath = '.\\test_samples\\ex_wav.wav'
original = SvSignal(audio_filepath)
original.toMono()
print(audio_filepath)
print(f"Sample Rate: {original.getSampleRate()}")
print(f"Duration: {original.getDuration()} seconds")
print(f"Number of Channels: {original.getNumChannels()}")
print(f"Samples: {original.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(original.estimate_frequency()))
original.visualize()

high = high_pass_filter(original.copy(), 1000)
high.toMono()
print(f"Sample Rate: {high.getSampleRate()}")
print(f"Duration: {high.getDuration()} seconds")
print(f"Number of Channels: {high.getNumChannels()}")
print(f"Samples: {high.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(high.estimate_frequency()))
high.visualize()


low = low_pass_filter(original.copy(), 200)
low.toMono()
print(f"Sample Rate: {low.getSampleRate()}")
print(f"Duration: {low.getDuration()} seconds")
print(f"Number of Channels: {low.getNumChannels()}")
print(f"Samples: {low.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(low.estimate_frequency()))
low.visualize()

print('Convolving... may take some time')
convolved = convolve_audio(
    sample_signal = original, 
    impulse_signal = SvSignal('.\\test_samples\\gtr_ir.wav'), 
    normalize = True )

convolved.visualize()
print('Convolving done.')
print(f"Sample Rate: {convolved.getSampleRate()}")
print(f"Duration: {convolved.getDuration()} seconds")
print(f"Number of Channels: {convolved.getNumChannels()}")
print(f"Samples: {convolved.getSamples()}")
print('Estimated Freq: {:.2f} Hz'.format(convolved.estimate_frequency()))
# convolved.write(os.getcwd() + '\\test_samples\\output_colvolved.wav') 

```