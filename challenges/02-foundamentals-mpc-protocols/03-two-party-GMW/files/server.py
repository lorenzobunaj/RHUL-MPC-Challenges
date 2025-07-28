import socket
import threading
from Crypto.Random import get_random_bytes
from utils import *
from private.gmw_gates import xor_gmw

PORT = 1343
with open("flag.txt") as f:
    FLAG = f.read().strip()

def circuit(x, y):
    assert len(x) == len(y)

    l = len(x) // 4
    x1, x2, x3, x4 = [x[l*i : l*(i+1)] for i in range(4)]
    y1, y2, y3, y4 = [y[l*i : l*(i+1)] for i in range(4)]

    x2 = notBytes(x2)
    y3 = notBytes(y3)

    t1 = xorBytes(x1, y1)
    t2 = xorBytes(x2, y2)
    t3 = xorBytes(x3, y3)
    t4 = andBytes(x4, y4)

    w1 = andBytes(t1, t2)
    w2 = xorBytes(t3, t4)

    z = xorBytes(w1, w2)

    return z

def and_gmw(conn, sx, ry):
    bits = []
    table = []
    for _ in range(4):
        tr = bytesToBits(bytes.fromhex(pwn_input(conn, "Table row (hex): ")))
        table.append(tr)
    
    bits_sx = bytesToBits(sx)
    bits_ry = bytesToBits(ry)
    for i in range(len(table[0])):
        bits.append(table[2 * bits_sx[i] + bits_ry[i]][i])

    return bitsToBytes(bits)

def challenge(conn):
    # input sharing
    x = get_random_bytes(16 * 4)
    y = get_random_bytes(16 * 4)
    rx = get_random_bytes(16 * 4)
    ry = get_random_bytes(16 * 4)
    sx = xorBytes(x, rx)
    sy = xorBytes(y, ry)

    secret = circuit(x, y)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)
    
    pwn_print(conn, f"rx: {rx.hex()}")
    pwn_print(conn, f"sy: {sy.hex()}")

    # circuit evalutation
    [y1, y2, y3, y4] = [[sx[16*i:16*(i+1)], ry[16*i:16*(i+1)]] for i in range(4)]

    t1 = xor_gmw(y1[0], y1[1])
    t2 = xor_gmw(y2[0], y2[1])
    t3 = xor_gmw(y3[0], y3[1])
    t4 = and_gmw(conn, y4[0], y4[1])

    w1 = and_gmw(conn, t1, t2)
    w2 = xor_gmw(t3, t4)
    
    zy = xor_gmw(w1, w2)

    zx = bytes.fromhex(pwn_input(conn, "secret share: "))
    secret_guess = xorBytes(zx, zy)

    pt = decrypt(ct, secret_guess, iv).hex()
    pwn_print(conn, pt)

    conn.close()

def handle_client(conn):
    try:
        challenge(conn)
    except Exception as e:
        print(f"Error handling client: {repr(e)}")
    finally:
        conn.close()

def main():
    print(f"[+] Server listening on port {PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"[*] New connection received from {addr}")
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()