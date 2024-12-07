Avesta Mirashrafi

10/15: Played around with more frequency creation. Figured out how to build a chord with a python program. It involved storing different frequencies in an array and having a loop iterate over it, adding each one to the sound being played. 

10/18: Attempting to get a grasp on fourier and dft's.

10/24: Learned about different filtration. Different forms of "pass" filters means 
that different ranges of frequencies are filtered out of a sound. For example, low pass means that only certain low frequencies
don't get filtered out of a sound.

10/29: Playing around with creating a python program that plays a canon but running into issues with having multiple lines 
play at the same time. I might look into multithreading.

11/10: I'm starting to decide what kind of final project ideas sound good. A voice part changer sounds interesting. It would 
involve some kind of frequency control where certain frequency ranges are adjusted, mainly the fundamental. I'm also considering
making some kind of canon generative player. There would be simple harmonies like I IV V I and it would pick notes from each chord
and play it in some kind of assigned rhythm. The user could then choose to offset the melody creating the canon. Food for thought.

11/15: Last class we went over MIDI. I've had a lot of enounters with MIDI in my time. Key take aways:
It uses a 5-pin DIN connector with an 8N1 protocol at 31,250 bps, with 1-3 byte messages consisting of status and data bytes.
Supports:  note on/off (with velocity), pitch bend, controllers for volume/pan/expression, and instrument sound changes.

12/3: Today I tried to create my own pitch analysis using FFT's and measuring magnitude of
peaks. I was able to get within the ball park but it turned out to be messy business. I'll
probably turn to a library that is better at it.

12/7: Wrapping up my course work today. My course project is working reasonably well. Lower frequencies are harder to capture and identify accurately.
I think this could be due to lower frequencies having larger wavelengths and having lower energy.
