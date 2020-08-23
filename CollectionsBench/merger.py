import glob
import os

base_path = './'

all_files = glob.glob(os.path.join(base_path, "*.csv"))
all_files = [x for x in all_files if x != base_path + "/merged.csv"]
f = open(base_path + "/merged.csv", "a")

f1 = open(all_files[0])
first_row = f1.readline()
f1.close()
f.write(first_row)

for x in all_files:
    first = False
    y = open(x)
    for line in y:
        if first:
            f.write(line)
        else:
            first = True
    y.close()
f.close()