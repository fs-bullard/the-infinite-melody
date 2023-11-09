import os
from midi_extract import extract
from os.path import join
import numpy as np

dataset = []

save_dir = "maestro-v3.0.0"

dirs = os.walk(save_dir)
for d in dirs:
    print("Directory: "+d[0])
    for f in d[2]:
        if f[-5:] == ".midi":
            e = extract(join(d[0],f))
            dataset.append(e)
    
    # f = open("dataset_maestro.txt", "w")
    # f.write(str(dataset))
    # f.close()
    np.save("dataset_maestro.npy", np.array(dataset, dtype=object))