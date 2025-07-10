import traceback
from utils.helper import optionalprint
from . import BakerDavenport

def runOneWay(mylrs, options):

		# Divide initial values by their greatest common divisor
		if options.get('reducelrs'):
			mylrs = mylrs.getReducedLrs()

		returnable = {
			'status': 'success'
		}
		returnable['lrs'] = mylrs


		if options.get("fixedbound"):
			bound = options.get("fixedbound")
		else: 
			
			success, bound = BakerDavenport.findDominantRoots(mylrs)

		returnable['bound'] = bound

		if not options.get('boundonly'):
			numbers = mylrs.listn(bound + 1)
			zeros = [x for x,y in enumerate(numbers) if y == 0 ]
			returnable['zeros'] =zeros

			if options.get('listn'):
				total = bound + 1
				if not (options.get('renderfull')):
					total = min(400,total)
				returnable['listn'] = [str(x) for x in numbers[:total]]
		return returnable


def getNegativeDirection(mylrs,options):
		mylrs = mylrs.getShiftedNormalisedReverseLRS()
		optionalprint(options, lambda:mylrs)
		returnable = runOneWay(mylrs,options)
		returnable['lrs'] = mylrs.negStr();
		returnable['bound'] = -returnable['bound']
		if not options.get('boundonly'):
			returnable['zeros'] = [-i for i in returnable['zeros']]
		return returnable

def caller(mylrs,options):
	try:

		if options.get('bidirectional', False):
			returnablePos = runOneWay(mylrs,options)
			returnableNeg = getNegativeDirection(mylrs,options)

			returnable = {
				'status': 'success',
				'lrs': returnablePos['lrs']	,
				'bound': max(returnableNeg['bound'], returnablePos['bound']),
				'boundPos':  returnablePos['bound'],
				'boundNeg':  returnableNeg['bound']
			}
			if not options.get('boundonly'):
				if 0 in returnablePos['zeros']:
					returnable['zeros'] = returnableNeg['zeros'][::-1] + returnablePos['zeros'][1:]
				else: 
					returnable['zeros'] = returnableNeg['zeros'][::-1] + returnablePos['zeros']
				if options.get('listn'):
					returnable['listn'] = returnableNeg['listn'][::-1] + returnablePos['listn'][1:]
			return returnable
		else: 

			isReversed = options.get('reverseLRS')
			if isReversed:
				return getNegativeDirection(mylrs,options)
			else:
				return runOneWay(mylrs,options)

	except Exception as err:
		print(err)
		print(traceback.format_exc())
		if options.get('raiseError'):
			raise err
		return {
			'status': 'fail',
			'error' : str(err)
		}

