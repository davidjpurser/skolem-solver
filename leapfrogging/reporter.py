from collections import Counter
from utils.reporter import Reporter
import csv

class LeapfroggingReporter(Reporter):

	returnVars = 9

	def get_headers(self, options):
		# Order	Recurrence	Initial	Flags	Algorithm	Success	Status	Time	Algorithm	prime	N	zeros	r	i	f	t	unique	max_multiplicity
		# ["Order", "Recurrence", "Initial", "Flags", "Algorithm", "Success",
		    # "Status", "Time"]
		return [
		    "zeros", "num_zero", "last_zero", "tree_depth", "max_mod", "avg_mod", "mode_mod", "jumps", "mods"
		]

	def optionshook(self,options):
		options.set('returnResultTreeClass', True)

	def success(self, returnable, options=None):
		
		#  Success T/F, error message (if F), time of computation, list of zeros, zero count, max zeros depth of tree, max modm, mean modm, any modal modm

		if returnable['Leapfrogging']['status'] == 'fail' :
			raise Exception(returnable['Leapfrogging']['error'])

		resultTree = returnable['Leapfrogging']['resultTree']
			
		modms = list(resultTree.getModMs())
		modmsc = Counter(modms)
		jumps = [x[1] for x in resultTree.getSplitInfo()]
		if len(jumps) > 0:
			maxjumps = max(jumps)
		else:
			maxjumps = None

		zeroLst = list(resultTree.getZeros())
		zeroLst.sort()
		returnInfo = [ 
			" ".join([str(x) for x in zeroLst]), 
			len(zeroLst), 
			zeroLst[-1] if len(zeroLst) > 0 else '', 
			resultTree.getDepth(), 
			max(modms),
			sum(modms)//len(modms),
			modmsc.most_common(1)[0][0], 
			jumps,
			list(resultTree.getModuloInfo())
		]

		if options and options.get("everychild"):
			for child in resultTree.getAllChildren():
				if child.type == "modm":
					with open(options.get("everychild"), 'a') as csvfile:
						row = []
						lrs = child.actualLrs
						row.append(child.modm)
						row.append(child.period)
						row.append(lrs.order)
						row.extend(lrs.recurrence)
						# row.extend(lrs.listn(30))
						csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						csvwriter.writerow(row)
		return returnInfo



	def error(self, err):
		returnInfo = [None for i in range(LeapfroggingReporter.returnVars)]
		return returnInfo

