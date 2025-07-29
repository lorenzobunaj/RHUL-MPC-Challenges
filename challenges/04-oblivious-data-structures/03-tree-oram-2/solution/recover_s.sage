from sage.all import *
from Crypto.Cipher import AES

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

p = 65537
d = pow(2,5)

iv = b'\x88\xb1$\xe1\xf2\xcau\xbbu\x19<\x85\x96q\xd87'
ct = b"\xcb'\xd5j\x9e\x1bm\x92\xed*\x1c\x9a@\xd6f\xe0\xb9_#\xe9\x0bsEQl\x08\xb5I\xb94\x82\t|\xf1\xd1\xeaw\xfeM%.\x02\xfb\x1d|\xd2\xba5"
g_list = [35818, 63995, 8195, 46415, 34352, 17845, 12747, 45103]
A_list = [29283, 7967, 471, 58290, 50849, 8132, 48701, 31096]
B_list = [43503, 39870, 43775, 16020, 52416, 19432, 51560, 47292]

def cheon_attack(g, A, B, p, d):
    phi = euler_phi(p - 1)
    phi_ratio = phi / (p - 1)
    lower_bound = 1 / (6 * log(log(p - 1)))
    check1 = float(phi_ratio) > float(lower_bound)
    if not check1:
        print("Not passed check 1")
        return None
    
    zeta0 = primitive_root(p)
    zeta = power_mod(zeta0, d, p)
    order = Mod(zeta, p).multiplicative_order()
    
    check2 = order == (p - 1) // d
    if not check2:
        print("Not passed check 2")
        return None

    for k0 in range(order):
        if B == power_mod(g, power_mod(zeta, k0, p), p):
            break 

    for k1 in range(p):
        if A == power_mod(g, power_mod(zeta0, (k0 + k1*order) % p, p), p):
            break

    k = k0 + k1*order
    
    return pow(zeta0, k, p)


def main():
    secret = b""
    for i in range(8):
        s = int(cheon_attack(g_list[i], A_list[i], B_list[i], p, d))
        print(s)
        secret += int.to_bytes(s, 2, "big")

    print(decrypt(ct, secret, iv))

if __name__ == "__main__":
    main()