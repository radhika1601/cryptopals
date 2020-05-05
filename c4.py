#!/usr/bin/python3


def single_char_xor(input_bytes, char_value):
    output_bytes = b""
    for byte in input_bytes:
        output_bytes += bytes([ord(byte) ^ char_value])
    return output_bytes


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
    length = len(text)
    for c in text:
        score += letter_frequency.get(chr(c), 0) * length
    return score


def get_msg(input_str):
    b = input_str
    b = bytes.fromhex(b).decode("utf-8")
    max_score = 0
    message = ""
    for i in range(256):
        text = single_char_xor(b, i)
        score = get_score(text)
        if score > max_score:
            max_score = score
            message = text
    return message


if __name__ == "__main__":

    max_score = 0
    message = ""
    with open("4.txt") as fp:
        line = fp.readline()
        count = 1
        while line:
            try:
                text = get_msg(line.strip())
                score = get_score(text)
            except Exception:
                text = ""
                score = 0
            if max_score < score:
                max_score = score
                message = text
            line = fp.readline()
            count += 1
    print(message, count)
