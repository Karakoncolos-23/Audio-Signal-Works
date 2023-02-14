import sys
import wave
import pyaudio 
import numpy as np

with wave.open("C:/Users/Hamdi/Desktop/Diğer Belgeler/Kodlar/Audio Signal Works/Recordings/Recording-4.wav", "rb") as wf:
    p = pyaudio.PyAudio();
    FRAMES = wf.getnframes();
    CHANNELS = wf.getnchannels();
    FRAME_RATE = wf.getframerate();
    whole_binary_information = wf.readframes(FRAMES);
    wf.close();

whole_data = np.zeros(len(whole_binary_information), np.int16);
left_channel_data = np.zeros(len(whole_binary_information), np.int16);
right_channel_data = np.zeros(len(whole_binary_information), np.int16);
i = 0;
j = 0;

for i in range(0, len(whole_binary_information)):
    whole_data[i] = whole_data[i] + whole_binary_information[i];

while j < len(whole_binary_information):
    if j % 2 == 0:
        left_channel_data[j] = left_channel_data[j] + whole_binary_information[j];
        j = j + 1;
        
    else:
        right_channel_data[j] = right_channel_data[j] + whole_binary_information[j];
        j = j + 1;

whole_data_list = whole_data.tolist();
left_channel_data_list = left_channel_data.tolist();
right_channel_data_list = right_channel_data.tolist();
whole_byte_array_LE = bytearray(whole_data_list);
left_channel_byte_array_LE = bytearray(left_channel_data_list);
right_channel_byte_array_LE = bytearray(right_channel_data_list);
whole_bytes_LE = bytes(whole_byte_array_LE);
left_channel_bytes_LE = bytes(left_channel_byte_array_LE);
right_channel_bytes_LE = bytes(right_channel_byte_array_LE);

with wave.open("Recording-4 (ORIGINAL).wav", "wb") as wf_ed:
    p = pyaudio.PyAudio();
    SAMPLE_VALUE_FORMAT = pyaudio.paInt16;
    wf_ed.setsampwidth(p.get_sample_size(SAMPLE_VALUE_FORMAT));
    wf_ed.setnchannels(CHANNELS);
    wf_ed.setframerate(FRAME_RATE);
    wf_ed.writeframes(whole_bytes_LE);
    wf_ed.close();
    p.terminate();

   

