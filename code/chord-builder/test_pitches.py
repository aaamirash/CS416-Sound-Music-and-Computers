import scipy.io.wavfile as wf
import sounddevice as sd
import numpy as np
import time

amplitude = 8192
frequencies = [(440), (523.25), (329.6)]
duration = 1
sample_rate = 48000

#t = duration / sample_rate, I realized this logic was wrong and that I would
#need linspace to create an array of points
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
combined_wave = np.zeros_like(t)
converted_wave = combined_wave
#Sin Wave Equation 
for frequency in frequencies:
    one_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    combined_wave += one_wave
    converted_wave = combined_wave.astype(np.int16)
    sd.play(converted_wave, sample_rate)
    time.sleep(1)
print(converted_wave)
wf.write("chord1.wav", sample_rate, converted_wave)

sd.wait()
