import socket
import threading
from utils import pwn_input, pwn_print
from party1 import Party1
from party2 import Party2

PORT = 1338
with open("flag.txt") as f:
    FLAG = f.read().strip().encode().hex()

def challenge(conn):
    party1 = Party1()
    party2 = Party2()

    in1 = party1.int1()
    in2 = party2.int1()
    if in2 == [1, 1]:
        in2 = [0, 0]

    pwn_print(conn, "|".join(map(str, in2)))
    
    in11 = in1[in2[0] + 2 * in2[1]]
    in12 = list(in1[3:])
    in12.pop(in2[0] + 2 * in2[1])
    in3 = [in11] + in12

    pwn_print(conn, "|".join(map(str, in3)))

    guess = int(pwn_input(conn, "Insert the product of the coefficients a, b and c: "))
    p = in1[0] * in1[1] * in1[2]

    if guess == p:
        pwn_print(conn, FLAG)

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