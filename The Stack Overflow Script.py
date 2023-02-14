import sys
import wave
import pyaudio

bit_depth = 2;
FRAMES = 1024;
float_normalise = 1.0 / float(2**((8*bit_depth) - 1))

with wave.open("Recording-1.wav", "rb") as file:

    f = pyaudio.PyAudio();

    whole_data = file.readframes(FRAMES);

    int16_samples = [int.from_bytes(sample, byteorder='little', signed=True) for sample in [whole_data[i:i+bit_depth] for i in range(0, len(whole_data), bit_depth)]]
    float_samples = [float(sample) * float_normalise for sample in int16_samples]
    
    print(whole_data);
    print(int16_samples);
    print(float_samples);

    file.close();