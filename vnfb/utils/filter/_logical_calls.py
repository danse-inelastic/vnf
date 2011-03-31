# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# this is only used by "parser" module

def logical_and(*args):
    if len(args)<2: raise ValueError
    if len(args)==2: return logical_and2(*args)
    left = logical_and(*args[:-1])
    right = args[-1]
    return logical_and2(left, right)
        
def logical_or(*args):
    if len(args)<2: raise ValueError
    if len(args)==2: return logical_or2(*args)
    left = logical_or(*args[:-1])
    right = args[-1]
    return logical_or2(left, right)
        
def logical_and2(a, b):
    return a.__l_and__(b)
def logical_or2(a, b):
    return a.__l_or__(b)


calls = {
    'logical_and': logical_and,
    'logical_or': logical_or,
    }


# version
__id__ = "$Id$"

# End of file 
