import sys
import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

def ltbe_int16(data: np.int16) -> np.int16:
    bit_mask = 0x100FFFF;                          # The bit mask is used to eliminate possible effects of left shift that may result in a number that occupies more than 16 bits. Also, this mask preserves the original 16 bits.
    intermediate = (data << 8) | (data >> 8);      # The intermediate operation may result in that unintended outcome that yields more than 16 bits.
    result = bit_mask & intermediate;              # The intermediate result is masked so that the byte swap, i.e., endianness conversion is realised.
    return result;

with wave.open("C:/Users/Hamdi/Desktop/Diğer Belgeler/Kodlar/Audio Signal Works/Recordings/Alo Alo.wav", "rb") as wf:
    p = pyaudio.PyAudio();
    FRAMES = wf.getnframes();
    FRAME_RATE = wf.getframerate();
    CHANNELS = wf.getnchannels();
    BYTES = wf.getsampwidth();
    BITS = BYTES * 8;
    DURATION = np.floor(FRAMES / FRAME_RATE);
    whole_binary_information = wf.readframes(FRAMES);
    wf.close();

i = 0;
V_REF = 5;                                                                     # Reference voltage of the ADC is assumed to be 5 V.
mono_data = np.zeros(len(whole_binary_information), np.int16);
left_channel_data = np.zeros(len(whole_binary_information), np.int16);
right_channel_data = np.zeros(len(whole_binary_information), np.int16);
modified_mono_bytes = np.zeros(len(whole_binary_information), np.int16);
modified_left_bytes = np.zeros(len(whole_binary_information), np.int16);
modified_right_bytes = np.zeros(len(whole_binary_information), np.int16);
mono_voltage_levels = np.zeros(len(whole_binary_information), np.float32);     # Here, when we use floats instead of integers, the details are covered as a means to keep the resolution while showing decimal ADC output values.
left_voltage_levels = np.zeros(len(whole_binary_information), np.float32);
right_voltage_levels = np.zeros(len(whole_binary_information), np.float32);
filtered_left_voltage_levels = np.zeros(len(whole_binary_information), np.float32);

while i < len(whole_binary_information):
    if CHANNELS == 1:
        mono_data[i] = mono_data[i] + whole_binary_information[i];
        modified_mono_bytes[i] = ltbe_int16(mono_data[i]);
        mono_voltage_levels[i] = (modified_mono_bytes[i] * V_REF) / (pow(2, BITS) * 0.5);
        i = i + 1;

    else:
        if i % 2 == 0:
            left_channel_data[i] = left_channel_data[i] + whole_binary_information[i];
            modified_left_bytes[i] = ltbe_int16(left_channel_data[i]);
            left_voltage_levels[i] = (modified_left_bytes[i] * V_REF) / (pow(2, BITS) * 0.5);
            i = i + 1;
        
        else:
            right_channel_data[i] = right_channel_data[i] + whole_binary_information[i];
            modified_right_bytes[i] = ltbe_int16(right_channel_data[i]);
            right_voltage_levels[i] = (modified_right_bytes[i] * V_REF) / (pow(2, BITS) * 0.5);
            i = i + 1;

INITIAL_VALUE_1 = 0;
INITIAL_VALUE_2 = 0;
j = 0;

for j in range(0, len(whole_binary_information)):
    if j == 0:
        filtered_left_voltage_levels[j] = filtered_left_voltage_levels[j] + FRAME_RATE * ((0.000051 * left_voltage_levels[j]) - (0.0001 * INITIAL_VALUE_1) + (0.000051 * INITIAL_VALUE_2));
        j = j + 1;

    elif j == 1:
        filtered_left_voltage_levels[j] = filtered_left_voltage_levels[j] + FRAME_RATE * ((0.000051 * left_voltage_levels[j]) - (0.0001 * left_voltage_levels[j - 1]) + (0.000051 * INITIAL_VALUE_1));
        j = j + 1;

    else:
        filtered_left_voltage_levels[j] = filtered_left_voltage_levels[j] + FRAME_RATE * ((0.000051 * left_voltage_levels[j]) - (0.0001 * left_voltage_levels[j - 1]) + (0.000051 * left_voltage_levels[j - 2]));
        j = j + 1;

time = np.linspace(0, DURATION, len(whole_binary_information));

if CHANNELS == 1:
    plt.plot(time, mono_voltage_levels);
    plt.title("The Audio Signal");
    plt.xlabel("Time (s)");
    plt.ylabel("ADC Output (V)");
    plt.show();

else:
    plt.subplot(2, 1, 1);
    plt.plot(time, filtered_left_voltage_levels);
    plt.title("Left Channel Audio Signal");
    plt.xlabel("Time (s)");
    plt.ylabel("ADC Output (V)");
    plt.subplot(2, 1, 2);
    plt.plot(time, right_voltage_levels);
    plt.title("Right Channel Audio Signal");
    plt.xlabel("Time (s)");
    plt.ylabel("ADC Output (V)");
    plt.tight_layout();
    plt.show();



















