import itertools as it
import orjson
import numpy as np
import string

# 8 x 12 array
C = [f'{t[0]}{t[1]}' for t in it.product(string.ascii_uppercase,range(1,13))]

def generate_grid(a):
    l = []
    aa = a.T
    for r in aa:
        ones = np.nonzero(r)[0] * 2
        l.append({ "screenData" : [C[i] for i in ones]})
    return {"gridData" : l}

def generate_grid_json(a):
    return orjson.dumps(generate_grid(a))

def cells_from_grid(a):
    g = generate_grid(a)["gridData"]
    return { "cellData" : sorted(set(it.chain.from_iterable((r["screenData"] for r in g))))}

def cells_from_grid_json(a):
    return orjson.dumps(cells_from_grid(a))
