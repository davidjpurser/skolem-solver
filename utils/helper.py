# Generic helper functions that have no other home.



def optionalprint(options, functionToPrint):
    if options.get('print'):
        x = functionToPrint()
        print(x)
        return x

def sign(number):
    #helper function
    if number == 0:
        return 0
    elif number >0:
        return 1
    else: 
        return -1


from functools import reduce
from math import gcd

def gcdlist(List):
    #Computes the gcd of a list of integers
    return reduce(gcd, List)
