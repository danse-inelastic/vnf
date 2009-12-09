#!/usr/bin/env python


def setup():
    from dsaw.db import connect
    db = connect(db='postgres:///vnfa2b')

    from vnfb.components.DOMAccessor import DOMAccessor
    da = DOMAccessor('proxy')
    da.db=db

    from vnf.dom import alltables
    for t in alltables(): db.registerTable(t)
    
    return da


def testAtomicStructure():
    da = setup()
    
    from vnf.dom.AtomicStructure import AtomicStructure
    id = 'TDGMTC'
    struct = da.getRecordByID(AtomicStructure, id)

    import atomicstructure as s
    structp = s.AtomicStructureProxy(struct, da)
    assert structp.id == id

    print structp.getNumberOfAtoms()

    assert structp.__dict__.has_key('_object')
    structp._setObjectObsolete()
    assert not structp.__dict__.has_key('_object')

    structobj = structp._getObject()
    print structobj[0]
    atomp = structobj[0]
    print type(atomp)
    print atomp.record

    print structp.lattice
    return


def testDelete():
    from dsaw.db import connect
    db = connect(db='postgres:///vnfa2b')

    from vnf.dom import alltables
    for t in alltables(): db.registerTable(t)

    import atomicstructure
    da = atomicstructure.Accessor()
    da.db = db
    
    id = '6AGGUMN'
    da.removeAtomicStructure(id)
    return
    

def main():
    # testAtomicStructure()
    testDelete()
    return

main()
