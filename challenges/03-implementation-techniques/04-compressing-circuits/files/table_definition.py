import os

table = bytearray()
for _ in range(5):
    table.extend(os.urandom(16))

with open("table.bin", "wb") as f:
    f.write(table)