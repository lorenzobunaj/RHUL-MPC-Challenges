def pwn_print(conn, message: str):
    conn.send(message.encode())

def pwn_input(conn, prompt: str) -> str:
    pwn_print(conn, prompt)
    return conn.recvline().decode().strip()