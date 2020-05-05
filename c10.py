from Crypto.Cipher import AES
import base64


def ecb_encrypt(msg, key):
    if len(msg) % 16 != 0:
        pad = 16 - len(msg) % 16
        msg = msg + bytes([pad] * pad)
    # print(len(msg))
    cipher = AES.new(key, AES.MODE_ECB)
    cipher_txt = cipher.encrypt(msg)
    return cipher_txt


def ecb_decrypt(cipher_txt, key):
    if len(cipher_txt) % 16 != 0:
        pad = 16 - len(cipher_txt) % 16
        cipher_txt = cipher_txt + bytes([pad] * pad)
    decipher = AES.new(key, AES.MODE_ECB)
    msg = decipher.decrypt(cipher_txt)
    return msg


def xor(x, y):
    out = b""
    for a, b in zip(x, y):
        out += bytes([a ^ b])
    return out


def cbc_encrypt(text, iv, key):
    if len(text) % 16 != 0:
        pad = 16 - len(text) % 16
        text = text + bytes([pad] * pad)
    blocks = [text[i : i + 16] for i in range(0, len(text), 16)]
    cipher_txt = b""
    for block in blocks:
        ct = ecb_encrypt(xor(block, iv), key)
        cipher_txt += ct + b"\n"
        iv = xor(iv, text)
    return cipher_txt


def cbc_decrypt(cipher, iv, key):
    blocks = [cipher[i : i + 16] for i in range(0, len(cipher), 16)]
    msg = b""
    for block in blocks:
        m = xor(ecb_decrypt(block, key), iv)
        iv = block
        msg += m
    return msg


if __name__ == "__main__":
    with open("10.txt") as f:
        encrypted = base64.b64decode("".join([line.strip() for line in f.readlines()]))
        decrypted = cbc_decrypt(encrypted, bytes([0x00] * 16), "YELLOW SUBMARINE")
        print(
            base64.b64encode(
                cbc_encrypt(decrypted, bytes([0x00] * 16), "YELLOW SUBMARINE")
            )
        )
        assert encrypted == base64.b64encode(
            cbc_encrypt(decrypted, bytes([0x00] * 16), "YELLOW SUBMARINE")
        )
