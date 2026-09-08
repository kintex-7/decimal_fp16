import struct
import numpy as np
import pandas as pd

def decimal_to_fp16(value):
    # Convert Python float (FP32) to IEEE-754 FP16
    value = float(value)

    if value < -65504 or value > 65504:
        print(f"Error: {value} is outside the FP16 finite range.")
        return

    
    fp16_bytes = struct.pack('>e', float(value))

    # Convert the 2 bytes into a 16-bit integer
    fp16_int = int.from_bytes(fp16_bytes, byteorder='big')

    # Binary representation
    binary = format(fp16_int, '016b')

    # Hexadecimal representation
    hexadecimal = format(fp16_int, '04X')

    # Separate sign, exponent and mantissa
    sign = binary[0]
    exponent = binary[1:6]
    mantissa = binary[6:16]

    return binary, hexadecimal, sign, exponent, mantissa

df=pd.read_csv("decimal_to_fp16_test_vectors.csv")
test_values = df['Decimal'].tolist()

print("Decimal\t\tFP16 Binary\t\tHex\tSign\tExponent\tMantissa")
print("-" * 90)

for value in test_values:
    binary, hexadecimal, sign, exponent, mantissa = decimal_to_fp16(value)

    print(
        f"{value:<12}\t"
        f"{binary}\t"
        f"{hexadecimal}\t"
        f"{sign}\t"
        f"{exponent}\t"
        f"{mantissa}"
    )