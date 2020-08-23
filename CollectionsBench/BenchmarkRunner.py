import sys
import os
import datetime
import subprocess
import glob

time = datetime.datetime.now()
timeformat = "%Y%m%d_%H-%M-%S"
timestamp = time.strftime(timeformat)

base_path = timestamp + "_Benchmark"
os.mkdir(base_path)

# No default values for the implementation and benchmark variables
num_arguments = len(sys.argv)
if num_arguments < 3:
    print "You need to supply the following arguments: \n benchmarks implementations test_type [warmup_iterations iterations]\n"

benchmarks = sys.argv[1] if num_arguments > 1 else 'Online'
implementations = ('-p impl=' + sys.argv[2]) if num_arguments > 2 else ''
warmup_iterations = sys.argv[3] if num_arguments > 3 else 20
iterations = sys.argv[4] if num_arguments > 4 else 10
iteration_time = sys.argv[5] if num_arguments > 5 else 10
forks = 4

for impl in ['ONLINE_ADAPTIVE_LIST','ONLINE_ADAPTIVE_MAP','WRAPPED_MAP', 'WRAPPED_LIST']:
	for t in ['update', 'even', 'iterate']:
		for i in range(0,6):
			implementations = '-p impl=' + impl
			threads = 2**i
			file_path = base_path + "/bench_" + impl +'_' + t + "_"+ str(threads) + ".csv"
			bashCommand = "java -jar benchmarks.jar .*{4}.* {3} -p testType={5}  -rff {0} -r {7} -i {1} -wi {2} -t {6} -bm thrpt -gc true -p threads={8} -f {9}".format(file_path, iterations, warmup_iterations, implementations, benchmarks, t, threads, iteration_time, threads, forks)

			process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
			while True:
				output = process.stdout.readline()
				if output == '' and process.poll() is not None:
					break
				if output:
					print output.strip()


#combine files.
all_files = glob.glob(os.path.join(base_path, "*.csv"))
all_files = [x for x in all_files if x != base_path + "/" + timestamp + "-merged.csv"]
f = open(base_path + "/" + timestamp + "-merged.csv", "w+")

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


