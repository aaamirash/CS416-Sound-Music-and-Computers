#Avesta Mirashrafi
#Voice part/ vocal range analyzer
#This program determines the vocal range you are singing in live
#stores the frequencies aka pitches and then determines where your voice
#lies. The program then asks if you want to hear what you just sang as
#a different voice type.

#The actual pitch detection was taken from the program below. I used
#that program as a starting point and built on top of it. I first 
#attempted to do pitch analysis myself using FFTs and magnitude 
#analysis of different frequency peaks, but it proved too complicated
#for me.
#https://www.makeartwithpython.com/blog/vocal-range-python-music21/

import aubio
from aubio import pitch
import queue
import music21
import pyaudio
import numpy as np
import wave
import collections
import librosa
import soundfile as sf

# Parameters
filename = "test.wav"  # Output WAV file name
channels = 1
rate = 44100  #sample rate
frames_per_buffer = 1024  #Larger buffer to reduce noise
win_s = 2048  #FFT window size
hop_s = 512
tolerance = 0.8

# PyAudio object
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,  #16-bit PCM for better quality
                channels=channels, rate=rate, input=True,
                input_device_index=0, frames_per_buffer=frames_per_buffer)

q = queue.Queue()  
current_pitch = music21.pitch.Pitch()

# Create aubio pitch detection object
pitch_o = pitch("yin", win_s, hop_s, samplerate=rate)
pitch_o.set_tolerance(tolerance)

# Total number of frames read
total_frames = 0

# Pitch counter to track the occurrences of each pitch
pitch_counts = collections.Counter()

# Set up the WAV file for recording
wav_file = wave.open(filename, 'wb')
wav_file.setnchannels(channels)
wav_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wav_file.setframerate(rate)

def get_current_note():
    pitches = []
    confidences = []
    current_pitch = music21.pitch.Pitch()

    while True:
        try:
            # Read data from the audio stream
            data = stream.read(hop_s, exception_on_overflow=False)

            # Write the data to the WAV file
            wav_file.writeframes(data)

            # Convert data to samples for pitch detection
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            samples /= 32768.0  # Normalize int16 to float32 range (-1.0 to 1.0)

            # Perform pitch detection
            detected_pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()

            current = 'NaN'
            if detected_pitch > 0 and confidence >= tolerance:
                current_pitch.frequency = float(detected_pitch)
                current = current_pitch.nameWithOctave
                print(f"{detected_pitch:.2f} Hz ---- {current} ---- {current_pitch.microtone.cents:.2f} cents")
                pitch_counts[current] += 1  # Update pitch count

            pitches.append(detected_pitch)
            confidences.append(confidence)

            q.put({'Note': current, 'Cents': current_pitch.microtone.cents, 'Hz': detected_pitch})
        except KeyboardInterrupt:
            break

#Categorize the voice into Bass, Tenor, Alto, or Soprano based on highest and lowest frequencies
def categorize_voice(filtered_pitch_counts):
    highest_freq = None
    lowest_freq = None
    valid_pitches = []
    for pitch_name, count in filtered_pitch_counts.items():
        pitch_obj = music21.pitch.Pitch(pitch_name)
        valid_pitches.append(pitch_obj.frequency)

    if valid_pitches:
        highest_freq = max(valid_pitches)
        lowest_freq = min(valid_pitches)

    #categorizing logic
    if highest_freq and lowest_freq:
        if 65.41 <= lowest_freq <= 220.00 and 220.00 <= highest_freq <= 440.00:
            category = "You are a Bass"
        elif 110.00 <= lowest_freq <= 587.33 and 146.83 <= highest_freq <= 587.33:
            category = "You are a Tenor"
        elif 146.83 <= lowest_freq <= 698.46 and 220.00 <= highest_freq <= 698.46:
            category = "You are an Alto"
        elif 196.00 <= lowest_freq <= 1046.50 and 261.63 <= highest_freq <= 1046.50:
            category = "You are a Soprano"
        else:
            category = "Your voice spanned over more than one voice part"
        print(f"Voice Category: {category}")


if __name__ == '__main__':
    try:
        get_current_note()
    except KeyboardInterrupt:
        pass
    finally:
        # Properly close the audio stream and WAV file
        stream.stop_stream()
        stream.close()
        wav_file.close()
        p.terminate()

        #Filter out frequencies with less than 5 occurrences
        filtered_pitch_counts = {pitch_name: count for pitch_name, count in pitch_counts.items() if count >= 5}

       

        # Print the pitch counts at the end
        print("\nPitch Occurrences:")
        for pitch_name, count in pitch_counts.items():
            print(f"{pitch_name}: {count}")

         # Categorize the voice
        categorize_voice(filtered_pitch_counts)

    # Load the recorded WAV file using librosa
    audio, sr = librosa.load(filename, sr=None)  # Load the original sample rate

    user_input = input("Do you want to pitch shift up or down a voice part? (u/d/n) (up/down/none): ").strip().lower()

    if user_input == 'u':
    #pittch up by 12 semitones (1 octave)
        audio_pitched_up = librosa.effects.pitch_shift(audio, sr=sr, n_steps=7)
        output_file_up = 'pitched_up_octave.wav'
        sf.write(output_file_up, audio_pitched_up, sr)
        print("Pitch shifting completed. Files saved as:")
        print(f" - Pitched Up: {output_file_up}")
    
    if user_input == 'd':
    # Pitch down by 12 semitones (1 octave)
        audio_pitched_down = librosa.effects.pitch_shift(audio, sr=sr, n_steps=-7)
        output_file_down = 'pitched_down_octave.wav' 
        sf.write(output_file_down, audio_pitched_down, sr)
        print("Pitch shifting completed. Files saved as:")
        print(f" - Pitched Down: {output_file_down}")

    
    

   
