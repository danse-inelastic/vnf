# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Supported filter types
TYPES   = ("pw",)



def filterFactory(type):
    package     = type.lower()+"filter"
    filterClass = type.upper()+"Filter"
    module      = _import(package)
    return getattr(module, filterClass)()


def _import(package):
    return __import__(package, globals(), locals(), [''], -1)


__date__ = "$Aug 6, 2010 12:50:09 PM$"


