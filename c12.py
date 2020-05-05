import base64
import sys
from c10 import ecb_encrypt, ecb_decrypt
from c11 import rand_key, detect_cipher

key = rand_key()


def encrypt(text):
    string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
YnkK"
    string = base64.b64decode(string)
    text += string
    blocks = [text[i : i + 16] for i in range(0, len(text), 16)]
    out = b""
    for block in blocks:
        out += ecb_encrypt(block, key)
    return out


def find_block_size():
    prev_txt = encrypt(b"A")
    for i in range(2, 20):
        curr_txt = encrypt(b"A" * i)
        if prev_txt[:4] == curr_txt[:4]:
            return i - 1
        prev_txt = curr_txt


def find_payload_length():
    prev_length = len(encrypt(b""))
    for i in range(1, 20):
        data = b"A" * i
        length = len(encrypt(data))
        if prev_length != length:
            return length - i


def find_one_more_byte(known, block_size):
    l = len(known)
    padding_length = (-l - 1) % block_size
    padding = b"A" * padding_length

    target_slice = slice(l * block_size, (l + 1) * block_size)
    target_block = encrypt(padding)[target_slice]

    for i in range(0, 256):
        message = padding + known + bytes([i])
        block = encrypt(message)[target_slice]
        if block == target_block:
            return bytes([i])


def find_byte_by_byte(block_size):
    known = b""
    payload_length = find_payload_length()
    print(payload_length)
    for _ in range(payload_length):
        next_byte = find_one_more_byte(known, block_size)
        # print(known)
        known += next_byte
    return known


if __name__ == "__main__":
    block_size = find_block_size()
    assert block_size == 16
    mode = detect_cipher(encrypt(b"A" * 50))
    assert mode == "ECB"
    secret = find_byte_by_byte(block_size)

    print(secret.decode())
