from random import randint
from c10 import cbc_decrypt, cbc_encrypt, ecb_decrypt, ecb_encrypt, xor
import base64
from Crypto.Cipher import AES


def rand_key():
    key = b""
    for i in range(16):
        key += bytes([randint(0, 255)])
    return key


def aes_encrypt(text):
    text = bytes([0x00] * randint(5, 10)) + text + bytes([0x00] * randint(5, 10))
    key = rand_key()
    cipher_txt = b""
    if randint(1, 2) == 1:
        print("ECB")
        blocks = [text[i : i + 16] for i in range(0, len(text), 16)]
        for block in blocks:
            cipher_txt += ecb_encrypt(block, key)
    else:
        print("CBC")
        cipher_txt = cbc_encrypt(text, bytes([0x00] * 16), key)
        # print(cipher_txt)
    return cipher_txt


def detect_cipher(encrypted):
    chunks = [encrypted[i : i + 16] for i in range(0, len(encrypted), 16)]
    reps = len(chunks) - len(set(chunks))
    if reps > 0:
        return "ECB"
    else:
        return "CBC"


if __name__ == "__main__":
    with open("10.txt") as f:
        encrypted = base64.b64decode("".join([line.strip() for line in f.readlines()]))
        decrypted = cbc_decrypt(encrypted, bytes([0x00] * 16), "YELLOW SUBMARINE")
        # print(decrypted)
        encrypted = aes_encrypt(decrypted)
        print(detect_cipher(encrypted))
        # print(aes_encrypt(decrypted))
    # print(rand_key())
