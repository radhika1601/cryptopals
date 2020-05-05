from Crypto.Cipher import AES
import base64

if __name__ == "__main__":

    with open("7.txt") as f:
        encrypted = f.read()
        encrypted = base64.b64decode(encrypted)
        key = b"YELLOW SUBMARINE"
        decipher = AES.new(key, AES.MODE_ECB)
        print(decipher.decrypt(encrypted))
