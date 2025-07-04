from pwn import *

HOST = "localhost" # change to the actual host
PORT = 5000 # change to the actual port

def main():
    conn = remote(HOST, PORT)
    msg = int(conn.recvline().strip())

    out1 = msg ^ pow(2, 12)
    for _ in range(15):
        out1 //= 3

        flag = hex(out1)[2:]
        if len(flag) % 2 != 0:
            flag = "0" + flag
        
        flag = bytes.fromhex(flag)
        
        if (flag[:4] == b"RHUL"):
            print(flag)
            break

if __name__ == "__main__":
    main()