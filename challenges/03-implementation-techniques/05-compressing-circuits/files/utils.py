from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))