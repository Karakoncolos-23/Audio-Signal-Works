import sys
import wave
import pyaudio

with wave.open("Recording-5.wav", "rb") as wf:
    p = pyaudio.PyAudio();
    FRAMES = wf.getnframes();                             # Frames are used to fit in them file information without loading up all of them onto a single variable and possibly exceeding a pre-specified memory size of it.
    whole_binary_information = wf.readframes(FRAMES);     # Apparently, which seems proven though, the software reads only the raw audio sample values.
    print(whole_binary_information);                      # print() function returns decimal correspondings of those hex values.
    wf.close();

