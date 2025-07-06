from pwn import *

HOST = "localhost" # change to the actual host
PORT = 1340 # change to the actual port

def main():
    conn = remote(HOST, PORT)

    flag = ""
    line = conn.recvline().strip().decode()
    p, cnt = 0, 0
    while line[:27] == "Enter the next choice bit:":
        p = 1 - round(pow(math.sin(p * math.pi / 2), 2))
        conn.sendline(str(p).encode())
        cnt += 1
        line = conn.recvline().strip().decode()

    flag += line[-2]
    for _ in range(cnt-1):
        byte = conn.recvline().strip().decode()[-2]
        flag += byte

    print(flag)

    conn.close()

if __name__ == "__main__":
    main()