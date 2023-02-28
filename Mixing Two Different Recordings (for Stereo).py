import sys
import wave
import pyaudio 
import numpy as np

def ltbe_int16(data: np.uint8) -> np.int16:                   # Little- to big-endian conversion function is here.
    big_endian_sign_test_mask = 0x80;                         # Since we can't directly tell Python to decide on whether a binary number is actually representing a negative number by looking at the sign bit, this mask is used to shed light onto the nature of the big-endian version of the unsigned 8-bit number.
    if data & big_endian_sign_test_mask == 0:                 # If the MSB (most significant bit) of the unsigned 8-bit number is 0, the big-endian correspondence of that number (which is the ADC output value in the decimal form) is positive.
        result = (data << 8) & 0xFF00;
        return result;

    else:                                                     # Otherwise, if the MSB is 1, then the ADC output is a negative decimal number.
        intermediate = (data << 8) & 0xFF00;
        result = -1 * ((intermediate ^ 0xFFFF) + 1);          # However, since Python can't produce a correct decimal value as a result of ambiguity during interpreting sign bits of binary numbers, we tell it what to do so that the result becomes a decimal number in the signed 16-bit representation. 
        return result;

def btle_int16(data: np.int16) -> np.uint8:                   # Big- to little-endian conversion is done here.
    result = data >> 8;                                       ###
    return result;

with wave.open("Rhythm.wav", "rb") as wf_1:                   
    p = pyaudio.PyAudio();                        
    FRAMES_1 = wf_1.getnframes();                             # In the PyAudio documentation, the word "FRAMES" refer to the audio samples so a frame is actually a sample. I didn't say "SAMPLES" in order to avoid confusion.
    CHANNELS_1 = wf_1.getnchannels();                         # Amount of channels the audio file includes. In our case, our WAVE files are in the one-channel or mono configuration.
    FRAME_RATE_1 = wf_1.getframerate();                       # The frame rate is the sampling rate or frequency. 44,1 kHz is used for all files.
    raw_audio_information_1 = wf_1.readframes(FRAMES_1);
    wf_1.close();

with wave.open("Tone.wav", "rb") as wf_2:
    p = pyaudio.PyAudio();
    FRAMES_2 = wf_2.getnframes();
    CHANNELS_2 = wf_2.getnchannels();
    FRAME_RATE_2 = wf_2.getframerate();
    raw_audio_information_2 = wf_2.readframes(FRAMES_2);
    wf_2.close();

raw_audio_information_1_array_LE = np.frombuffer(raw_audio_information_1, np.uint8);               
raw_audio_information_2_array_LE = np.frombuffer(raw_audio_information_2, np.uint8);
raw_audio_information_1_array_BE = np.zeros(len(raw_audio_information_1_array_LE), np.int16);
raw_audio_information_2_array_BE = np.zeros(len(raw_audio_information_2_array_LE), np.int16);
i = 0;

for i in range(0, len(raw_audio_information_1_array_BE)):
    raw_audio_information_1_array_BE[i] = raw_audio_information_1_array_BE[i] + ltbe_int16(raw_audio_information_1_array_LE[i]);
    raw_audio_information_2_array_BE[i] = raw_audio_information_2_array_BE[i] + ltbe_int16(raw_audio_information_2_array_LE[i]);

combined_raw_audio_information_array_BE = np.zeros(2 * len(raw_audio_information_1_array_BE), np.int16);
combined_raw_audio_information_array_LE = np.zeros(len(combined_raw_audio_information_array_BE), np.uint8);                                #####
j = 0;

while j < len(combined_raw_audio_information_array_BE):
    if j % 2 == 0:
        combined_raw_audio_information_array_BE[j] = combined_raw_audio_information_array_BE[j] + raw_audio_information_1_array_BE[int(j / 2)];
        combined_raw_audio_information_array_LE[j] = combined_raw_audio_information_array_LE[j] + btle_int16(combined_raw_audio_information_array_BE[j]);
        j = j + 1;

    else:
        combined_raw_audio_information_array_BE[j] = combined_raw_audio_information_array_BE[j] + raw_audio_information_2_array_BE[int((j - 1) / 2)];
        combined_raw_audio_information_array_LE[j] = combined_raw_audio_information_array_LE[j] + btle_int16(combined_raw_audio_information_array_BE[j]);
        j = j + 1;

combined_raw_audio_information_LE_list = combined_raw_audio_information_array_LE.tolist();
combined_raw_audio_information_LE_byte_array = bytearray(combined_raw_audio_information_LE_list);
combined_raw_audio_information_LE_bytes = bytes(combined_raw_audio_information_LE_byte_array);

with wave.open("Combined (Rhythm and Tone).wav", "wb") as wf_3:
    p = pyaudio.PyAudio();
    SAMPLE_VALUE_FORMAT = pyaudio.paInt16;
    CHANNELS_3 = 2;
    FRAME_RATE_3 = 44100;
    wf_3.setsampwidth(p.get_sample_size(SAMPLE_VALUE_FORMAT));
    wf_3.setnchannels(CHANNELS_3);
    wf_3.setframerate(FRAME_RATE_3);
    wf_3.writeframes(combined_raw_audio_information_LE_bytes);
    wf_3.close();
    p.terminate();