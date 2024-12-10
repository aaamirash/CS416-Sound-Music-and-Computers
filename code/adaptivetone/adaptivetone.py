#Avesta Mirashrafi

#This program adaptively adjusts the energy of different frequency ranges 
#of an audio file to create a more balanced "sound" across frequency 
#ranges. The different frequency ranges are defined below.

import scipy.fftpack as fftpack
from scipy.signal import butter, lfilter
from scipy.io import wavfile as wf
import numpy as np
import sounddevice as sd

LOWBAND = (1,300) #I had to set  to the lowband min to 1 because 0 gave me an error
MIDBAND = (300,2000)
HIGHBAND = (2000,20000)

fft_window = 2048 #samples per window

#load audio
sample_rate, data = wf.read('singing_sample.wav')
data = data[:, 0]

#Audio before filter
sd.play(data)
sd.wait()

#https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
#got this next bit from stackoverflow for the scipy butter filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

fft_freq = fftpack.fftfreq(fft_window, 1 / sample_rate)

#define the masks for different freq ranges
low_mask = (np.abs(fft_freq) >= LOWBAND[0]) & (np.abs(fft_freq) < LOWBAND[1])
mid_mask = (np.abs(fft_freq) >= MIDBAND[0]) & (np.abs(fft_freq) < MIDBAND[1])
high_mask = (np.abs(fft_freq) >= HIGHBAND[0]) & (np.abs(fft_freq) < HIGHBAND[1])

def measure_band_energy(fft_result, curr_mask):
    band_energy = np.sum(np.abs(fft_result[curr_mask])**2)  #energy = magnitude squared
    return band_energy

adjusted_audio = []
num_windows = (len(data) - fft_window) // (fft_window // 2) + 1

for i in range(num_windows):
    #Extract a window of audio data
    start = i * (fft_window // 2)
    window_data = data[start:start + fft_window]
    
    #Perform FFT and measure band energies
    fft_result = fftpack.fft(window_data)
    
    #aquire band energy using fft and masks
    low_energy = measure_band_energy(fft_result, low_mask)
    mid_energy = measure_band_energy(fft_result, mid_mask)
    high_energy = measure_band_energy(fft_result, high_mask)

    #Calculate average energy across bands
    avg_energy = (low_energy + mid_energy + high_energy) / 3

    #Calculate gain adjustments to equalize energies
    #sqrt()
    low_gain = np.sqrt(avg_energy / low_energy) if low_energy > 0 else 1
    mid_gain = np.sqrt(avg_energy / mid_energy) if mid_energy > 0 else 1
    high_gain = np.sqrt(avg_energy / high_energy) if high_energy > 0 else 1

    #apply band-pass filters with gain adjustments to each frequency range
    low_band_signal = low_gain * butter_bandpass_filter(window_data, *LOWBAND, fs=sample_rate)
    mid_band_signal = mid_gain * butter_bandpass_filter(window_data, *MIDBAND, fs=sample_rate)
    high_band_signal = high_gain * butter_bandpass_filter(window_data, *HIGHBAND, fs=sample_rate)
    
    #Combine adjusted frequency ranges together
    adjusted_window = low_band_signal + mid_band_signal + high_band_signal
    adjusted_audio.extend(adjusted_window)

#Convert the adjusted audio back to int16 format and save as a new file
adjusted_audio = np.array(adjusted_audio)
max_val = np.max(np.abs(adjusted_audio))

#Normalize the adjusted audio to fit within int16 bounds
if max_val > 32767:  # Only normalize if values exceed int16 range
    adjusted_audio = adjusted_audio * (32767 / max_val)

# Convert to int16 format and save
adjusted_audio = adjusted_audio.astype(np.int16)

#Audio after filter
sd.play(data)
sd.wait()
wf.write("adjusted_audio.wav", sample_rate, adjusted_audio)