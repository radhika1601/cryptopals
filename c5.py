#!/usr/bin/python3


def repeated_char_xor(input_bytes):
    output_bytes = b""
    array = [ord("I"), ord("C"), ord("D")]
    i = 0
    for byte in input_bytes:
        char_value = array[i]
        output_bytes += bytes([ord(byte) ^ char_value])
        i = (i + 1) % 3
    return output_bytes


if __name__ == "__main__":
    with open("5.txt") as f:
        line = f.read().strip()
        encrypted_text = repeated_char_xor(line)
        print(encrypted_text.hex())
