from pwn import *

HOST = "localhost" # change to the actual host
PORT = 1343 # change to the actual port

def bitsToBytes(bits):
    byte_arr = bytearray()

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
    bits = bytesToBits(a)
    for i in range(len(bits)):
        bits[i] = 1 - bits[i]
    
    return bitsToBytes(bits)

def andBytes(a, b):
    return bytes([ai & bi for ai, bi in zip(a, b)])

def xor_gmw(sx, ry):
    return xorBytes(sx, ry)

def not_gmw(ry):
    return notBytes(ry)

def and_table(rx, sy):
    r = bytes([0] * 16)
    table = []
    for i in range(4):
        sx = bytes([i // 2] * 16)
        ry = bytes([i % 2] * 16)
        table.append(xorBytes(r, andBytes(xorBytes(rx, sx), xorBytes(sy, ry))).hex())

    return table

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"rx: ")
    rx = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"sy: ")
    sy = bytes.fromhex(conn.recvline().strip().decode())

    [x1, x2, x3, x4] = [[rx[16*i:16*(i+1)], sy[16*i:16*(i+1)]] for i in range(4)]
    
    t1 = xor_gmw(x1[0], x1[1])
    t2 = xor_gmw(x2[0], x2[1])
    t3 = xor_gmw(x3[0], not_gmw(x3[1]))

    tab1 = and_table(x4[0], x4[1])
    for tr in tab1:
        conn.sendline(tr.encode())
    t4 = bytes([0] * 16)

    ssx = xor_gmw(t2, t3)
    ssx = xor_gmw(ssx, t4)

    tab2 = and_table(ssx, t1)
    for tr in tab2:
        conn.sendline(tr.encode())
    ssx = bytes([0] * 16)

    conn.sendline(ssx.hex().encode())
    conn.recvuntil(b"secret share")
    conn.recvline()
    flag = bytes.fromhex(conn.recvline().strip().decode())

    print(flag)
    
    conn.close()

if __name__ == "__main__":
    main()