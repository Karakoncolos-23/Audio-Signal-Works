import sys
import numpy as np

def ltbe_int16(data):
    bit_mask = 0x100FFFF;                          # The bit mask is used to eliminate possible effects of left shift that may result in a number that occupies more than 16 bits. Also, this mask preserves the original 16 bits.
    intermediate = (data << 8) | (data >> 8);      # The intermediate operation may result in that unintended outcome that yields more than 16 bits.
    result = bit_mask & intermediate;              # The intermediate result is masked so that the byte swap, i.e., endianness conversion is realised.
    print(hex(result));

ltbe_int16(0x12AB);






