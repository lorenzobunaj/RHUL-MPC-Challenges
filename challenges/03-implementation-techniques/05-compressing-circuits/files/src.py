from Crypto.Random import get_random_bytes
from bytecode import bytecode
from utils import *

TABLE_FILE = "table.bin"
NUM_ROWS = 6
NUM_COLS = 16

with open("flag.txt") as f:
    FLAG = f.read().strip()

with open(TABLE_FILE, "rb") as f:
    raw = f.read()
    assert len(raw) == (NUM_ROWS - 1) * NUM_COLS
    table = [list(raw[i*NUM_COLS:(i+1)*NUM_COLS]) for i in range(NUM_ROWS - 1)]

def main():
    secret = [b for b in get_random_bytes(16)]
    table.append(secret)

    accumulator = [0] * NUM_COLS
    vars = {}
    stack = []

    labels = {instr[1]: idx for idx, instr in enumerate(bytecode) if instr[0] == "LABEL"}

    pc = 0
    while pc < len(bytecode):
        instr = bytecode[pc]
        op = instr[0]

        if op == "PUSH_CONST":
            stack.append(instr[1])

        elif op == "STORE":
            vars[instr[1]] = stack.pop()

        elif op == "LOAD":
            stack.append(vars[instr[1]])

        elif op == "INC":
            stack[-1] += 1

        elif op == "LT":
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a < b))

        elif op == "LTE":
            b = stack.pop()
            a = stack.pop()
            stack.append(int(a <= b))

        elif op == "JMP_IF_FALSE":
            cond = stack.pop()
            if not cond:
                pc = labels[instr[1]]
                continue

        elif op == "JMP":
            pc = labels[instr[1]]
            continue

        elif op == "LOOKUP":
            j = stack.pop()
            i = stack.pop()
            stack.append(table[i][j])

        elif op == "LOAD_ACC":
            j = vars["j"]
            stack.append(accumulator[j])

        elif op == "STORE_ACC":
            j = vars["j"]
            accumulator[j] = stack.pop()

        elif op == "XOR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a ^ b)

        elif op == "LABEL":
            pass

        elif op == "RETURN":
            break

        else:
            raise ValueError(f"Unknown opcode: {op}")

        pc += 1

    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), bytes(secret), iv)

    with open("output.text", "w") as f:
        f.writelines([
            bytes(accumulator).hex() + "\n",
            iv.hex() + "\n",
            ct.hex() + "\n"
        ])

if __name__ == "__main__":
    main()