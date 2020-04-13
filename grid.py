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

def cells_from_matrix(a):
    return cells_from_grid(generate_grid(a))

def cells_from_grid(g):
    return { "cellData" : sorted(set(it.chain.from_iterable((r["screenData"] for r in g["gridData"]))), key=lambda s: (s[0], int(s[1:])))}

def cells_from_grid_json(g):
    return orjson.dumps(cells_from_grid(g))

def generate_grid_and_cell_data_json(mlabels, matrices):
    grid_dict = {}
    cell_dict = {}
    for batch in mlabels:
        label = mlabels[batch]
        if label in matrices:
            a = matrices[label]
            g = generate_grid(a)
            cell_dict[batch] = cells_from_grid_json(g)
            grid_dict[batch] = orjson.dumps(g)
        else:
            cell_dict[batch] = '{}'
            grid_dict[batch] = '{}'
    return grid_dict, cell_dict