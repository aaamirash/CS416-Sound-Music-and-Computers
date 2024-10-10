#Avesta Mirashrafi

import scipy.io.wavfile as wf
import sounddevice as sd
import numpy as np

amplitude = 8192
frequency = 440
duration = 1
sample_rate = 48000

#t = duration / sample_rate, I realized this logic was wrong and that I would
#need linspace to create an array of points
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

#Sin Wave Equation 
wave_output = amplitude * np.sin(2 * np.pi * frequency * t)

#reformat to 16 bit int for wavs file format
converted_wave = wave_output.astype(np.int16)

wf.write("sine.wav", sample_rate, converted_wave)

sd.play(converted_wave, sample_rate)
sd.wait()

#clipped wave
amplitude_clipped = 16384

wave_output_2 = amplitude_clipped * np.sin(2 * np.pi * frequency * t)

#clip wave at indicated range
clipped_wave_output = np.clip(wave_output_2, -8192, 8192)
converted_clipped_wave = clipped_wave_output.astype(np.int16)

wf.write("clipped.wav", sample_rate, converted_clipped_wave)

sd.play(converted_clipped_wave, sample_rate)
sd.wait()
