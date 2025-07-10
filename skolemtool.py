import sys
import traceback
from utils.flags import FlagManager
from utils.lrs import lrs
from utils import lrsreader
from utils import Options
from bakerdavenport import caller as bdcaller
from leapfrogging import caller as lfcaller
from utils.subsequences import minimizeLRS
from utils.helper import optionalprint



def computeFromString(string,options):
	

	try:
		mylrs = lrsreader.lrsreader(string.splitlines())

		options = Options.Options(options)
		result = compute(mylrs,options)
		result['status'] = 'success'
		return result
	except Exception as err:
		print(err)
		return {
			'status': 'fail',
			'error' : str(err)
		}


def compute(mylrs,options):
	""" All options
	defaults
	{
		 "renderfull":false
		 "skipdegeneratecheck":false
		 "mergesubcases":false
		 "reducelrs":false
		 "fastmodm":false
	}
	"""

	myNewlrs = minimizeLRS(mylrs)			
	optionalprint(options, lambda:"----Input LRS----")
	optionalprint(options, lambda: mylrs)
	optionalprint(options, lambda:"----Minimised LRS----")
	optionalprint(options, lambda: myNewlrs)

	returnable = {}

	if not options.get('skipminimisation', False) and myNewlrs and myNewlrs.order != mylrs.order:
		optionalprint(options, lambda:"The input LRS was not minimal. The program will minimize it")
		returnable['minimized'] = 'True'
		mylrs = myNewlrs		


	if all([x == 0 for x in mylrs.initial]):
		raise Exception("This is the zero sequence. Zero in all positions.")


	if not (options.get('skipdegeneratecheck')):
		if mylrs.isDegenerate():
			raise Exception("This LRS is degenerate. The tool does not support them.")


	if (options.get('Leapfrogging')):
		returnable['Leapfrogging'] =  lfcaller.caller(mylrs,options)

	if (options.get('BakerDavenport')):
		returnable['BakerDavenport'] = bdcaller.caller(mylrs,options)

	if (options.get('pAdic')):
		raise Exception("p-adic algorithm is not yet available on this repository.")


	return returnable




if __name__ == "__main__":
	mylrs = lrsreader.readLRS()


	options = Options.Options()


	if len(sys.argv) > 1:
		flags  = sys.argv[1]
	else:
		flags = ''

	flagManager = FlagManager()
	flagManager.setOptions(options,flags)
	print(options.options)
	a = compute(mylrs, options)

	print(a)


