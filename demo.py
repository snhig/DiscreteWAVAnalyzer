from core.Signal import Signal
import numpy as np
import matplotlib.pyplot as plt
import os, time, logging
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
signal = Signal(filepath=os.getcwd() + '\\test_samples\\ex_wav.wav')

print(os.getcwd() + '\\test_samples\\ex_wav.wav')
print(f"Sample Rate: {signal.getSampleRate()}")
print(f"Duration: {signal.getDuration()} seconds")
print(f"Number of Channels: {signal.getNumChannels()}")
print(f"Samples: {signal.getSamples()}")

# resampled_signal:Signal = signal
# resampled_signal.resample(signal.getSampleRate()//2)
# print(f"Sample Rate: {resampled_signal.getSampleRate()}")
# print(f"Duration: {resampled_signal.getDuration()} seconds")
# print(f"Number of Channels: {resampled_signal.getNumChannels()}")
# print(f"Samples: {resampled_signal.getSamples()}")




