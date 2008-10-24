# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def getSystem(model, director):
    path = director.dds.abspath(model, 'system.py')
    return open(path).read()


def findModels(matter, db):
    from vnf.dom.BvKModel import BvKModel
    b = BvKModel()
    b.matter = matter
    v = b._getFormattedColumnValue('matter')
    return db.fetchall(BvKModel, where="matter='%s'" % v)


simpleelementarymatters = [
    'Al',
    'Fe',
    'Ni',
    ]
def issimplematter(matter):
    return matter.chemical_formula in simpleelementarymatters



# version
__id__ = "$Id$"

# End of file 
