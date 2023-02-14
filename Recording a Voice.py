import sys
import math
import wave
import pyaudio

CHUNKS = 1024;                            # Amount of chunks that divides the whole aural information into 1024 sections.
SAMPLE_VALUE_FORMAT = pyaudio.paInt16;    # ADC output sample length setting which is 16-bit long binary number configuration. Also, those values are converted to integers.
CHANNELS = 2;                             # Two-channel (stereo) audio transmission because of the nature of the PC.
FRAME_RATE = 44100;                       # Here, frames are actually samples. In accordance with the Nyquist-Shannon sampling theorem, sampling frequency/frame rate is set to be a little more than twice the bandwidth of the analog audio signal which ensures slight oversampling.
RECORD_DURATION = 5;                      # The recording is 5 secs. long.

with wave.open("Recording-6.wav", "wb") as wf:
    p = pyaudio.PyAudio();
    wf.setsampwidth(p.get_sample_size(SAMPLE_VALUE_FORMAT));
    wf.setnchannels(CHANNELS);
    wf.setframerate(FRAME_RATE);
    stream = p.open(format = SAMPLE_VALUE_FORMAT, channels = CHANNELS, rate = FRAME_RATE, input = True);
    print("Recording...");

    for a in range(0, math.floor(FRAME_RATE / CHUNKS) * RECORD_DURATION):
        wf.writeframes(stream.read(CHUNKS));

    print("Done!");
    stream.close();
    p.terminate();