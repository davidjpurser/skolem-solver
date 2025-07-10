from utils.reporter import Reporter

class BakerDavenportReporter(Reporter):
	returnVars = 5

	def get_headers(self, options):
		# Order	Recurrence	Initial	Flags	Algorithm	Success	Status	Time	Algorithm	prime	N	zeros	r	i	f	t	unique	max_multiplicity
		# ["Order", "Recurrence", "Initial", "Flags", "Algorithm", "Success",
		    # "Status", "Time"]
		return [
		    "zeros", "num_zero", "last_zero", "bound"
		]


	def success(self, returnable, options = None):
		if returnable['BakerDavenport']['status'] == 'fail' :
			raise Exception(returnable['BakerDavenport']['error'])


		bound = returnable['BakerDavenport']['bound']
		if 'zeros' in returnable['BakerDavenport']:				
			zeroLst = returnable['BakerDavenport']['zeros']
		else: 
			zeroLst = []

		returnInfo = [ 
			" ".join([str(x) for x in zeroLst]), 
			len(zeroLst), 
			zeroLst[-1] if len(zeroLst) > 0 else '', 
			bound
		]
		return returnInfo

	def error(self, err):

		returnInfo = [None for i in range(BakerDavenportReporter.returnVars)]
		return returnInfo

