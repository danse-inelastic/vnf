# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def notEmpty(candidate):
    # not an empty string
    s = str(candidate)
    if len(s) == 0: raise ValueError, "Cannot be an empty string"
    return s


def real(candidate):
    try:
        f = float(candidate)
    except:
        raise ValueError
    return f


def positivereal(candidate):
    try:
        f = float(candidate)
    except:
        raise ValueError
    if f<=0: raise ValueError
    return f


def positiveinteger(candidate):
    try:
        f = int(candidate)
    except:
        raise ValueError
    if f<=0: raise ValueError
    return f


def nonnegativereal(candidate):
    try:
        f = float(candidate)
    except:
        raise ValueError
    if f<0: raise ValueError
    return f


def realvector3(candidate):
    try:
        v = tuple(eval(candidate))
    except:
        raise ValueError

    if len(v)!=3: raise ValueError

    for i in v:
        if not isNumber(i): raise ValueError
        continue
    return v


def isNumber(candidate):
    return isinstance(candidate, int) or isinstance(candidate, float)


# version
__id__ = "$Id$"

# End of file 
