from utils.flags import FlagManager
import sys
from utils import lrsreader
import csv
import skolemtool
import time
from utils import Options
from bakerdavenport.reporter import BakerDavenportReporter
from leapfrogging.reporter import LeapfroggingReporter

#Runs a single LRS on a single algorithm with the required flags and passes to the reporter
# run format: sage unified_runner.py lrsfile csvfile flags


lrs = lrsreader.readLRS(position=1)

options = Options.Options()
options.set('csvoutput', sys.argv[2])
options.set("raiseError", True)

if len(sys.argv) > 3:
	flags  = sys.argv[3]
else:
	flags = ''



flagManager = FlagManager()
flagManager.setOptions(options,flags)


algorithms = ["BakerDavenport", "Leapfrogging","pAdic"]
active = [options.get(x) for x in algorithms if options.get(x) == True]
if len(active) != 1:
	raise ValueError("This must be run with exactly one active algorithm")

if options.get('BakerDavenport'):
	tool = BakerDavenportReporter()
if options.get('Leapfrogging'):
	tool = LeapfroggingReporter()


tool.optionshook(options)

starttime = time.time_ns()
try:
	returnable = skolemtool.compute(lrs,options)
	endtime = time.time_ns()
	successInfo = [True, "Success"]
	returnInfo = tool.success(returnable, options)
except Exception as err:
	endtime = time.time_ns()
	successInfo = [False, str(err)]
	returnInfo = tool.error(err)

row = successInfo +  [(endtime-starttime)/1000000000] + returnInfo
		
with open(options.get("csvoutput"), 'a') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow(row)

