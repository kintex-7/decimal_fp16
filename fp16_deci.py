import struct
import pandas as pd


def fp16_to_decimal(fp16_binary):
    fp16_binary = str(fp16_binary).strip()

    # Make sure it has exactly 16 bits
    fp16_binary = fp16_binary.zfill(16)

    # Binary string -> integer
    fp16_int = int(fp16_binary, 2)

    # Integer -> 2 bytes
    fp16_bytes = fp16_int.to_bytes(2, byteorder="big")

    # FP16 -> decimal
    decimal_value = struct.unpack(">e", fp16_bytes)[0]

    return decimal_value


# Read CSV file
df = pd.read_csv("decimal_to_fp16_test_vectors.csv")

# Get FP16 binary values
test_values = df["FP16_Binary"].tolist()

print("Original Decimal\tFP16 Binary\t\tConverted Decimal")
print("-" * 75)

for i, value in enumerate(test_values):

    converted_decimal = fp16_to_decimal(value)

    original_decimal = df.iloc[i]["Decimal"]

    print(
        f"{original_decimal:<18}\t"
        f"{value}\t"
        f"{converted_decimal}"
    )