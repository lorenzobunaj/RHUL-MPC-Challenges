import socket
import threading
import hashlib
from utils import pwn_input_inline, pwn_print

CIRCUITS_NUM = 128
T = 3

PORT = 1365
with open("flag.txt") as f:
    FLAG = f.read().strip()

def H(x, t):
    return hashlib.sha256(x).digest()[:t]

def calculate_root(leafs):
    if len(leafs) == 2:
        return H(leafs[0] + leafs[1], T)
    
    l = len(leafs) // 2
    return H(calculate_root(leafs[:l]) + calculate_root(leafs[l:]), T)

def circuit_evaluation(conn, seed):
    if seed == b"FLAG":
        pwn_print(conn, FLAG)
    else:
        pwn_print(conn, H(seed, T).hex())

def challenge(conn):
    leafs = []

    client_root = pwn_input_inline(conn, f"Enter the root: ")
    client_root = bytes.fromhex(client_root)
    for i in range(CIRCUITS_NUM):
        leaf = pwn_input_inline(conn, f"Enter the {i+1}-th leaf: ")
        leaf = bytes.fromhex(leaf)
        leafs.append(leaf)

    R = calculate_root(leafs)

    if client_root != R:
        conn.close()
        return

    for i in range(CIRCUITS_NUM):
        seed = pwn_input_inline(conn, f"Enter the {i+1}-th seed: ")
        seed = bytes.fromhex(seed)
        if seed == b"FLAG" or H(seed, T) != leafs[i]:
            conn.close()
            return
        
    computation_seed = pwn_input_inline(conn, f"Enter the seed that you want to use: ")
    computation_seed = bytes.fromhex(computation_seed)
    for leaf in leafs:
        if H(computation_seed, T) == leaf:
            circuit_evaluation(conn, computation_seed)
            conn.close()
            return

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