from pwn import *

HOST = "localhost" # change to the actual host
PORT = 5000 # change to the actual port

def main():
    
    conn = remote(HOST, PORT)
    msg = int(conn.recvline().strip().decode())

    for r in range(8, 16):
        mask = []
        for i in range(r):
            mask.append(1 if i % 2 == 0 else 0)
        k = int("".join(str(b) for b in mask), 2)
        
        msg ^= k

        for _ in range(r):
            msg //= 3

        flag = hex(msg)[2:]
        if len(flag) % 2 != 0:
            flag = "0" + flag
        
        flag = bytes.fromhex(flag)
        print(flag)
        
        if (flag[:4] == b"RHUL"):
            print(flag)
            break

    conn.close()

if __name__ == "__main__":
    main()