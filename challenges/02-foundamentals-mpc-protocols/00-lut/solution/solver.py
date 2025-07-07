from pwn import *
from Crypto.Protocol.SecretSharing import Shamir

HOST = "localhost" # change to the actual host
PORT = 1342 # change to the actual port

legal_moves = []
gaps = [-2, -1, 1, 2]
for m1 in gaps:
    for m2 in gaps:
        if (abs(m1) != abs(m2)):
            legal_moves.append([m1, m2])

def generateKnightPositionsRec(x, y, n, visited, positions, f):
    if n == 64:
        f[0] = 1
        return
    
    if x in range(8) and y in range(8) and visited[8 * x + y] == 0:
        visited[8 * x + y] = 1
        positions[n] = [x, y]
        for [m1, m2] in legal_moves:
            generateKnightPositionsRec(x + m1, y + m2, n+1, visited, positions, f)
            if f[0] == 1:
                return
        visited[8 * x + y] = 0
 
def generateKnightPositions(x, y):
    visited = [0 for _ in range(64)]
    positions = [[0, 0] for _ in range(64)]
    f = [0]
    generateKnightPositionsRec(x, y, 0, visited, positions, f)

    return positions

def main():
    conn = remote(HOST, PORT)

    x = int(conn.recvline().strip().decode()[-1])
    y = int(conn.recvline().strip().decode()[-1])
    conn.recvuntil(b"key = ")
    key = conn.recvline().strip()
    decrypted_lut = [[-1 for _ in range(8)] for _ in range(8)]

    positions = generateKnightPositions(x, y)

    for p in positions:
        conn.sendline(str(p[0]).encode())
        conn.sendline(str(p[1]).encode())
        conn.sendline(key)

        conn.recvuntil(b"share: ")
        share = bytes.fromhex(conn.recvline().strip().decode())
        conn.recvuntil(b"key: ")
        key = conn.recvline().strip()

        decrypted_lut[p[0]][p[1]] = share

    shares = []
    for i in range(2):
        for j in range(2):
            shares.append([])
            offset = [4*i, 4*j]
            for k in range(16):
                shares[2 * i + j].append((k+1, decrypted_lut[offset[0] + k // 4][offset[1] + k % 4]))

    flag = b""
    for i in range(4):
        flag += Shamir.combine(shares[i])[::-1][:10]

    print(flag)
    
    conn.close()

if __name__ == "__main__":
    main()