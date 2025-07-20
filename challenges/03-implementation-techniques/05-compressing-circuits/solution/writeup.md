# Compressing Circuits

**Challenge name**: Compressing Circuits\
**Category**: Implementation Techniques\
**Author**: Lorenzo Bunaj

## Challenge

This challenge implements a PCF Compiler in Python. It's offline, so we already know the operations, in bytecode format, that were fed to it and the corresponding output.

If we take a closer look and carefully analyze the bytecode and what each operation does, we can se that it XORs together a list of 16-bytes words.

In the source code, this compiler is used to XOR together the entries of a table imported from the file `table.bin`. At the end, the result of the operations set is given.

The flag is encrypted using a secret key `secret`, which is appended to the table as an additional entry before the evaluation starts.

## Solution

The vulnerabilty of the bytecode lies in the instruction `LTE`, which check if a value is less **or equal** than a given value.
Since the instruction is used to check the counter in a for loop, that means it doesn't only XOR the entries of the table, but also an additional one, which is the secret added after the table initialization.

Once we understood the logic behind the bytecode, recovering the secret (and therefore decrypt the flag) follows trivially by XORing the original table entries with the output of the compiler.