from pwn import *
from Crypto.Random import get_random_bytes

HOST = "localhost" # change to the actual host
PORT = 1343 # change to the actual port

def bitsToBytes(bits):
    byte_arr = []

    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (bits[i + j] << (7 - j))
        byte_arr.append(byte)

    return bytes(byte_arr)

def bytesToBits(bytes):
    bits = []
    for byte in bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def xorBytes(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def notBytes(a):
    return bytes([ai ^ 0xff for ai in a])

def andBytes(a, b):
    return bytes([ai & bi for ai, bi in zip(a, b)])

def xor_gmw(sx, ry):
    return xorBytes(sx, ry)

def not_gmw(s):
    return notBytes(s)

def and_table(rx, sy):
    r = get_random_bytes(16)
    table = []
    for i in range(4):
        sx = bitsToBytes([i // 2] * 16 * 8)
        ry = bitsToBytes([i % 2] * 16 * 8)
        table.append(xorBytes(r, andBytes(xorBytes(rx, sx), xorBytes(sy, ry))).hex())

    return table, r

def and_gmw(conn, rx, sy):
    tab, r = and_table(rx, sy)
    for tr in tab:
        conn.sendline(tr.encode())

    return r

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"rx: ")
    rx = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"sy: ")
    sy = bytes.fromhex(conn.recvline().strip().decode())

    [x1, x2, x3, x4] = [[rx[16*i:16*(i+1)], sy[16*i:16*(i+1)]] for i in range(4)]
    
    x2[0] = not_gmw(x2[0])
    x3[1] = not_gmw(x3[1])

    t1 = xor_gmw(x1[0], x1[1])
    t2 = xor_gmw(x2[0], x2[1])
    t3 = xor_gmw(x3[0], x3[1])
    t4 = and_gmw(conn, x4[0], x4[1])

    w1 = and_gmw(conn, t1, t2)
    w2 = xor_gmw(t3, t4)
    
    zx = xor_gmw(w1, w2)

    conn.sendline(zx.hex().encode())
    conn.recvuntil(b"secret share")
    conn.recvline()
    flag = bytes.fromhex(conn.recvline().strip().decode())

    print(flag)
    
    conn.close()

if __name__ == "__main__":
    main()