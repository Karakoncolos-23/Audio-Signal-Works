import sys
import numpy as np

num1 = [180];                          # bytearray() and bytes() functions only return hexadecimal representations of decimals if they are inside a list of any size. 
num2 = [160];
num1_byte_array = bytearray(num1);
num2_byte_array = bytearray(num2);
num1_bytes = bytes(num1_byte_array);
num2_bytes = bytes(num2_byte_array);

print(num1_bytes);
print(num2_bytes);