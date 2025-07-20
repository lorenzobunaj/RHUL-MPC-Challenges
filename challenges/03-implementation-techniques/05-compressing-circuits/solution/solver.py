from Crypto.Cipher import AES

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

with open("table.bin", "rb") as f:
    raw = f.read()
    assert len(raw) == 5 * 16
    table = [list(raw[i*16:(i+1)*16]) for i in range(5)]

def main():
    # output.txt
    accumulator = bytes.fromhex("df939abda0adda6669f7ada9130a52a0")
    iv = bytes.fromhex("98093f1a7d22fb0c94887353934ab555")
    ct = bytes.fromhex("890d980b81cb7a928259a544d73f15bd1687e6ab35649ec26015d095628945a7df4695e5ee80ef0971ed47a7bd87b313")

    accumulator = [b for b in accumulator]
    for tr in table:
        accumulator = [accumulator[i] ^ tr[i] for i in range(16)]

    secret = bytes(accumulator)

    print(decrypt(ct, secret, iv))

if __name__ == "__main__":
    main()
