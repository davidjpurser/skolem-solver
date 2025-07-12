from functools import partial
from multiprocessing import Pool
from ast import literal_eval as make_tuple
import sys
from utils.flags import FlagManager
from sys import platform
from multiprocessing import Process
import multiprocessing as mp
import csv
import skolemtool
import time
from utils import lrs
import random
from collections import Counter
import subprocess
from utils import Options



# CSV Format:
# order, recurrence, initial, flags, Success T/F, error message (if F), time of computation, list of zeros, zero count, max zeros depth of tree, max modm, mean modm, any modal modm



returnVars = 4

def run(lrs, options):


	import tempfile
	  
	temp = tempfile.NamedTemporaryFile()
	response = tempfile.NamedTemporaryFile()

	with open(temp.name, 'a') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(lrs.recurrence)
		csvwriter.writerow(lrs.initial)

	setup = [lrs.order, " ".join([str(x) for x in lrs.recurrence]), " ".join([str(x) for x in lrs.initial])]


	flagManager = FlagManager()
	flags = flagManager.getFlags(options)

	setup = setup + [flags]


	if options.get("Leapfrogging"):
		# runner = "lfoperate.py"
		setup += ["LF"]
	elif options.get("BakerDavenport"):
		# runner = "bdoperate.py"
		setup += ["BD"]
	elif options.get("pAdic"):
		setup += ["pA"]
	else:
		raise ValueError("no algorithm selected")





	runner = "unified_runner.py"

	if platform == "darwin":
		timeoutproc = 'gtimeout'
	else:
		timeoutproc = 'timeout'


	process = [timeoutproc, str(options.get("singleInstanceTimeout")), "sage", runner, temp.name, response.name, flags]

	print(process)

	starttime = time.time_ns()
	result = subprocess.call(process)

	print("RESULT", result)
	if result == 0:
		with open(response.name) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			row = next(reader)
	else: 
		endtime = time.time_ns()
		if result == 124:
			status = "Timeout"
		else:
			status = "unknown error"
		row = [False, status, (endtime-starttime)/1000000000] + [None for i in range(returnVars)]

	temp.close()
	response.close()
	
	row = setup + row
			
	with open(options.get("csvoutput"), 'a') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(row)


def doOneInstance( options, lrs):

	algorithms = ["Leapfrogging", "BakerDavenport"]

	for alg in algorithms:

		if options.get(alg):
			thisrunoptions = options.copy()
			for alg_not in algorithms:
				if alg != alg_not:
					thisrunoptions.set(alg_not,False)
			run(lrs, thisrunoptions)



if __name__ == '__main__':

	print(sys.argv)

	# 1: csvoutput
	# 4: input file
	# 5: flags
	options = Options.Options()

	options.set('csvoutput', sys.argv[1])

	starttime = time.time_ns()

	options.set('returnResultTreeClass', True)
	options.set("raiseError", True)

	if len(sys.argv) > 3:
		flags  = sys.argv[3]
	else:
		flags = ''

	flagManager = FlagManager()
	flagManager.setOptions(options,flags)
	lrss = []

	print(options.options)

	assert options.get('singleInstanceTimeout')
	assert options.get('cores')


	print('singleInstanceTimeout', options.get('singleInstanceTimeout'))

	extension = sys.argv[2].split(".")[-1]

	with open(sys.argv[2]) as f:
		
		if extension == "tpls":
			for line in f:
				tpl = make_tuple(line)
				lr = lrs.lrs(tpl[0], list(tpl[2]), list(tpl[1]))
				lrss.append(lr)
			
		elif extension == "csv":
			reader = csv.reader(f)
			for line in reader:
				order = int(line[0])
				recurrence = [int(x) for x in line[1].split(" ")]
				initial = [int(x) for x in line[2].split(" ")]
				lr = lrs.lrs(order,initial,recurrence)
				lrss.append(lr)

	print("LRS:", len(lrss))

	func = partial(doOneInstance, options)

	with Pool(options.get("cores")) as p:
		print(p.map(func, lrss))


	# 	while (time.time_ns() - starttime)/1000000000 < duration:
	# 		doOneInstance(options)








