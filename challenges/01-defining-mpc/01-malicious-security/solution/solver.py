from sympy import primerange, discrete_log, isprime

def build_p():
    product = 1
    bits = 256

    for p in primerange(2, pow(10, 6)):
        product = product * p
        if product.bit_length() > bits and isprime(product + 1):
            break
    
    return product + 1

def main():
    g = 2
    p = build_p()
    # print(p)
    # output got by sending p to the other party
    y = 650006737127527372108396261801295300471519523314325907733275145001495424662724795184069841246750473010860742298790550817059367718297017911057807651024396
    
    x = discrete_log(p, y, g)
    print(x)

if __name__ == "__main__":
    main()
