#!usr/bin/python3
from collections import OrderedDict
import base64


def get_score(text):
    letter_frequency = {
        "a": 0.08167,
        "b": 0.01492,
        "c": 0.02782,
        "d": 0.04253,
        "e": 0.12702,
        "f": 0.02228,
        "g": 0.02015,
        "h": 0.06094,
        "i": 0.06094,
        "j": 0.00153,
        "k": 0.00772,
        "l": 0.04025,
        "m": 0.02406,
        "n": 0.06749,
        "o": 0.07507,
        "p": 0.01929,
        "q": 0.00095,
        "r": 0.05987,
        "s": 0.06327,
        "t": 0.09056,
        "u": 0.02758,
        "v": 0.00978,
        "w": 0.02360,
        "x": 0.00150,
        "y": 0.01974,
        "z": 0.00074,
        " ": 0.13000,
    }
    score = 0
    # length = len(text)
    for c in text.lower():
        score += letter_frequency.get(chr(c), 0)
    return score


def single_char_xor(input_bytes, char_value):
    output_bytes = b""
    for byte in input_bytes:
        output_bytes += bytes([(byte) ^ char_value])
    return output_bytes


def get_key(input_str):
    b = input_str
    # print(input_str)
    # b = bytes.fromhex(b).decode("utf-8")
    max_score = 0
    message = ""
    key = ""
    for i in range(256):
        text = single_char_xor(b, i)
        score = get_score(text)
        if score > max_score:
            max_score = score
            message = text
            key = chr(i)
    # print(message)
    return key


def hammingDistance(s1, s2):
    s1 = bin(int(s1.hex(), 16))
    s2 = bin(int(s2.hex(), 16))
    distance = 0
    for i in range(len(s1) - 1):
        if s1[i] != s2[i]:
            distance += 1
    return distance


def find_keysize(encrypted):
    key_dist = {}
    keysizes = []
    for keysize in range(2, 40):
        distances = []
        chunks = [encrypted[i : i + keysize] for i in range(0, len(encrypted), keysize)]
        while True:
            try:
                chunk_1 = chunks[0]
                chunk_2 = chunks[1]
                distance = hammingDistance(chunk_1, chunk_2)
                distances.append(distance / keysize)
                del chunks[0]
                del chunks[1]
            except Exception:
                break
        dist = sum(distances) / len(distances)
        key_dist[dist] = keysize
        # print(key_dist)
    i = 0
    sorted_key_dist = sorted(key_dist)
    # print(key_dist)
    for key in sorted_key_dist:
        if i > 3:
            break
        keysizes.append(key_dist[key])
        i += 1
    # print(keysizes)
    return keysizes


def repeated_char_xor(input_bytes, key):
    output_bytes = b""
    i = 0
    key = key
    for byte in input_bytes:
        char_value = ord(key[i])
        output_bytes += bytes([ord(byte) ^ char_value])
        i = (i + 1) % len(key)

    return output_bytes


def decrypt_vignere_cipher(encrypted, keysize):
    key = ""

    encrypted = base64.b64decode(encrypted)
    # print(encrypted)
    # print(encrypted.__class__)
    # encrypted = (base64.b64decode(encrypted)).decode("utf-8")
    # print(encrypted)
    for i in range(keysize):
        block = b""
        for j in range(i, len(encrypted), keysize):
            block += bytes([encrypted[j]])
        # print(block)
        key += get_key(block)
    # print(key)

    message = repeated_char_xor(encrypted.decode(), key)
    # print(message)
    return message


if __name__ == "__main__":
    with open("6.txt") as f:
        encrypted = f.read().strip().encode("ascii")
        keysizes = find_keysize(encrypted)
        # print(keysizes)
        max_score = 0
        message = ""
        for keysize in keysizes:
            # print(keysize)
            text = decrypt_vignere_cipher(encrypted, keysize)
            score = get_score(text)
            if score > max_score:
                max_score = score
                message = text
    print(message)
