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


def setSystem(model, system, director):
    dir = director.dds.abspath(model)
    import os
    if not os.path.exists(dir): os.makedirs(dir)
    path = director.dds.abspath(model, 'system.py')
    return open(path, 'w').write(system)


def findModels_exact(matter, db):
    from vnf.dom.ins.BvKModel import BvKModel
    b = BvKModel()
    b.matter = matter
    v = b._getFormattedColumnValue('matter')
    return db.fetchall(BvKModel, where="matter='%s'" % v)


from vnf.dom.hash import hash
def findModels(matter, db):

    matter_key = hash(matter, db)

    from vnf.dom.ins.BvKModel import BvKModel
    candidates = db.fetchall(BvKModel)
    #ids = [c.id for c in candidates]
    #matter_keys = [hash(model.matter.dereference(db), db) for model in candidates]
    #raise "%s, %s" % (matter_key, matter_keys)

    def good(model):
        matterref = model.matter
        if not matterref: return False
        matter = matterref.dereference(db)
        return hash(matter, db) == matter_key
    return filter(good, candidates)


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
