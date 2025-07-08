import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(a, b)])

def H(label1: bytes, label2: bytes) -> bytes:
    return hashlib.sha256(label1 + label2).digest()

wires = [[(b'd\x96\xe1\xc95\x90\xda6s\xf7+\xbd\xe2\x02?\x92\xfa\x7fi\x1dU\n2\xe8r\xd7\x92\x8eT\xbf\x06\x94', 1), (b'>L\xb1\xfbbvL\x9f3Z\x89\x1a\xe1+_B\x19\xf7\xac\xa7X\xf9\x11c\x97/\x81T\xbd\x92W\xd9', 0)], [(b"\x8d\x8f\xa8\x82\xc4X\x07\xe5\xac\x00\xf2}\xf3\t\xee)\xaa\x9f\xa7\x97'\xccyL4\x85\x81\x82LX\xe6m", 0), (b'\xb2\xbd\x84\x97\xa1\x0f\xa9\x0c\x9e\xfb\xadzV\x1c\xbb\xacG9\x9f,\x0f\xfd-SD\x11\xa4\x1c\x19\xac\xfc\xcc', 1)]]
gg = [b"'^\xc7\xac\x0f\xc9\x1b\xa8\xfe\xfbZy}\x9b\x00\x07L\xe2\x10\xcc{\x95\x91y\xfd\x161\xcc!4\xba\xbf", b'u\x8c\xe0>\x95\x06\x84\x12\x90\x8aP\xc3\xebA6aj\x9c\xeb=x\x9e8\xd6\x10\x11`\xb0\xd5\x03fA', b'\x06\x0bf!\x82\xe6&;X^\x12L\x9c\xbe\x7f\x8e\xf0\xbax\xc0\xa8~\x02U\xcc\x82w1\xbe\x0f\xb0\xc3', b"\xabg\x81\x8fy!=\x0f%'*\x16\x99O\x8d\xfb1i\xadC\xad2\x89\xf6\r\xd1\xbbm\x1f\x99\xb2K"]
iv = bytes.fromhex("93bac7c5b86361d90dcc54c172859538")
ct = bytes.fromhex("5635ababd9e732bb8b2737989910cbed29f4b57086b79cb797613a99cf03998e")

def evaluate_gg(wires, gate):
    Wc = [None] * 2

    for a in [0, 1]:
        for b in [0, 1]:
            La, pa = wires[0][a]
            Lb, pb = wires[1][b]
            
            pc = pa * pb

            Lc = xor(H(La, Lb), gate[2*pa + pb])
            Wc[pc] = (Lc, pc)

    return Wc

def generate_secret(wires, gg):
    Wc = evaluate_gg(wires, gg) 

    secret, pc = Wc[1]

    return secret

def main():
    secret = generate_secret(wires, gg)
    
    cipher = AES.new(secret[-16:], AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(ct), AES.block_size)

    print("RHUL{" + flag.decode() + "}")

if __name__ == "__main__":
    main()