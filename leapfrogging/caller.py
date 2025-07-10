import traceback
from .resulttree import ResultTree
from utils.linearset import LinearSet
from . import findZeroOrModM
from utils.helper import optionalprint
from utils.subsequences import minimizeLRS

def caller(mylrs, options):
    try:
        returnable = {}

        myNewlrs = minimizeLRS(mylrs)
        optionalprint(options, lambda: "----Input LRS----")
        optionalprint(options, lambda: mylrs)
        optionalprint(options, lambda: "----Minimised LRS----")
        optionalprint(options, lambda: myNewlrs)

        if myNewlrs and myNewlrs.order != mylrs.order:
            optionalprint(options, lambda: "The input LRS was not minimal. The program will minimize it")
            returnable['minimized'] = 'True'
            mylrs = myNewlrs

        if not mylrs.isSimple():
            raise Exception("This is a non-simple LRS. Leapfrogging does not support them.")

        optionalprint(options, lambda: "----First----")
        optionalprint(options, lambda: mylrs.listn(mylrs.order * 3))

        optionalprint(options, lambda: "----Reverse----")
        reverse = optionalprint(options, lambda: mylrs.getNormalisedReverseLRS())

        optionalprint(options, lambda: "----First (backwards) ----")
        optionalprint(options, lambda: reverse.listn(mylrs.order * 3))

        optionalprint(options, lambda: "----Search----")

        resultTree = ResultTree(mylrs, LinearSet(0, 1), LinearSet(0, 1))
        results = findZeroOrModM.findZeroOrModM(mylrs, resultTree, options)

        optionalprint(options, lambda: "-----ResultTree------")
        from pprint import pprint as printpretty
        optionalprint(options, lambda: printpretty(resultTree.getResultObject(options)))

        zeros = list(resultTree.getZeros())
        zeros.sort()

        returnable['resultTree'] = resultTree.getResultObject(options)
        returnable['zeros'] = zeros
        returnable['status'] = 'success'
        if options.get('returnResultTreeClass'):
            returnable['resultTree'] = resultTree

        return returnable

    except Exception as err:
        print(err)
        print(traceback.format_exc())
        return {
            'status': 'fail',
            'error': str(err)
        }
