Voice Part/ Vocal Range Analyzer:

IMPORTANT: Please install Microsoft C++ Build Tools in order to use the aubio
python library. Select development tools when installing. 
https://visualstudio.microsoft.com/visual-cpp-build-tools/
I'm not too sure how this would with a linux machine or mac so
I will include a screen recording of how it works on my windows pc.

PROJECT DEMO: https://media.pdx.edu/media/t/1_ch8jx0nh

This program determines the vocal range you are singing in live.
It stores the frequencies aka pitches and then determines where your voice
lies. It has some simple logic to determine the voice part you would have in a 
traditional 4 part choir (AKA SATB).
The program then asks if you want to hear what you just sang either
pitched up or down. Right now I have a hard coded to 7 half step,
which moves the recording up or down a fifth.
