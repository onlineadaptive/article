import os

def walk_and_merge(path, f):
    absolute_first = True
    for root, dirs, files in os.walk(path):
        
        for curr_file in files:
            if ".csv" in curr_file:
                file_first = True
                f_handle = open(root + '/' + curr_file)
                for line in f_handle:
                    if not absolute_first and file_first:
                        file_first = False
                    else:
                        f.write(line)
                        absolute_first = False
                f_handle.close()


# Script
base_path = './'

f = open(base_path + "/merged.csv", "a")
walk_and_merge(base_path, f)
f.close()

        

