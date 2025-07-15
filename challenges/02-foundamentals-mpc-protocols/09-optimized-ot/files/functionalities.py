from hashlib import sha256

def ot_functionality(messages, choice):
    return messages[choice]

def random_oracle(x, l):
    out = sha256(x).digest()[:l]

    return out