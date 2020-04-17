# To manage matrices correctly
# At deployment, check if new matrices have been added to old batch sizes

import grid
import orjson
import sys
# Load the matrices from "compute" folder
EXPT_DIR="./compute/"
sys.path.append(EXPT_DIR)
import config
config.root_dir=EXPT_DIR
import get_test_results as expt

# VERSION_FILE
VERSION_FILE = "versioning.json"
# Matrices
MLABELS = expt.get_matrix_sizes_and_labels()
MATRICES = expt.get_matrix_labels_and_matrices()

def readable_string(batch, num_infected, infection_rate):
    m,n = grid.parse_batch(batch)
    return f'{n} Samples (with {m} tests. For {num_infected} infections or {infection_rate}% infection rate)'

def update_cache(mlabels, matrices, jfile):
    old_data = {}
    with open(jfile, 'rb') as reader:
        old_data = orjson.loads(reader.read())
    f = {}
    for batch in mlabels:
        print(batch)
        m,n,i = mlabels[batch]
        mat = matrices[m]
        g, c = grid.generate_grid_and_cell_data(batch, mat)
        f[batch] = {m : {"num_infected" : n, "infection_rate" : i, "readable" : readable_string(batch, n, i), "gridData" : g, "cellData" : c}}
    ob = set(old_data)
    nb = set(f)
    for batch in old_data:
        od = old_data[batch]
        # Batch does not exist in new data
        if batch not in f or not f[batch]:
            print(f"Batch {batch} not in new matrix data, marking as inactive")
            od["metadata"]["active"] = False
            continue
        nd = f[batch]
        oa = od["metadata"]["active"]
        oam = od["metadata"]["matrices"][-1]
        if oam in nd:
            # Currently active matrix in old data is same as new data
            if not oa:
                od["metadata"]["active"] = True
            continue
        # If old batch is not active, check if there is a key in new data
        if not oa:
            for m in nd:
                # Mark m as active, increment version, add to od
                od["metadata"]["latest_version"] += 1
                od["metadata"]["matrices"].append(m)
                od["metadata"]["active"] = True
                od[m] = nd[m]
            continue
        # Make matrix in new data active
        for m in nd:
            # Mark m as active, increment version, add to od
            od["metadata"]["latest_version"] += 1
            od["metadata"]["matrices"].append(m)
            od["metadata"]["active"] = True
            od[m] = nd[m]
    # New batches can be safely added to old_data
    for batch in nb - ob:
        print(f"New batch added - {batch}")
        od = {"metadata" : {}}
        od["metadata"]["active"] = True
        od["metadata"]["latest_version"] = 0
        nd = f[batch]
        for m in nd:
            od["metadata"]["matrices"] = [m]
            od[m] = nd[m]
        old_data[batch] = od
    jstr = orjson.dumps(old_data)
    with open(jfile, "wb") as outfile:
        outfile.write(jstr)

if __name__ == '__main__':
    #init_cache(MLABELS, MATRICES, VERSION_FILE)
    update_cache(MLABELS, MATRICES, VERSION_FILE)