from random import randint

def and_table(rx, sy):
    r = randint(0,1)
    table = []
    for i in range(4):
        sx = i // 2
        ry = i % 2
        table.append(r ^ ((rx ^ sx) * (sy ^ ry)))

    return r, table