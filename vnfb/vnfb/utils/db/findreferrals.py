#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# find all objects that referred to the given db record


import journal
debug = journal.debug('db.findreferrals')

def findreferrals(record, clerk):
    '''find all referalls of the given record

    return: yield referal_record, description
    '''
    #
    clerk.importAllDataObjects()
    orm = clerk.orm

    #
    Table = record.__class__
    id = record.id
        
    # find all talbes that could refer to this record
    debug.log( 'Gather references' )
    refs = []; vrefs = []
    from dsaw.db.Reference import Reference
    from dsaw.db.VersatileReference import VersatileReference
    for Table1 in orm.db.iterAllTables():
        debug.log( ' * on table %s' % Table1.getTableName() )
        if Table1 is Table: continue
        for name, col in Table1._columnRegistry.iteritems():
            if isinstance(col, Reference) and col.referred_table is Table:
                refs.append((Table1, col))
            elif isinstance(col, VersatileReference):
                vrefs.append((Table1, col))
        continue

    db = orm.db
    # for reference, we need to search each table that could refer to the given record,
    # and find those records that refer to the given record.
    debug.log( 'In References' )
    refrecords = []
    for Table1, col in refs:
        debug.log( ' * searching %s %s ...' % (Table1.getTableName(), col.name) )
        where = "%s='%s'" % (col.name, record.id)
        refrecords += db.query(Table1).filter(where).all()
        continue

    # for versatile reference, we need to search thru global pointer
    if hasattr(record, 'globalpointer'):
        debug.log( 'In Polymorphic References' )
        gp = record.globalpointer and record.globalpointer.id
        if gp:
            for Table1, col in vrefs:
                debug.log( ' * searching %s %s' % (Table1.getTableName(), col.name) )
                where = "%s='%s'" % (col.name, gp)
                refrecords += db.query(Table1).filter(where).all()
                continue

    # go through the __referenceset__ table and exclude the records
    # that refers to the given record as container
    from dsaw.db._referenceset import _ReferenceSetTable
    refsettablename = _ReferenceSetTable.getTableName()
    def refascontainer(r):
        tname = r.getTableName()
        if tname == refsettablename:
            container = r.container.dereference(db)
            return container.__class__ is Table and container.id == record.id
    #
    refrecords = filter(lambda r: not refascontainer(r), refrecords)
    
    for r in refrecords:
        tname = r.getTableName()
        if tname == refsettablename:
            container = r.container.dereference(db)
            element = r.element.dereference(db)
            desc = 'refset %s: %s(%s).%s#%s %s %s(%s)' % (
                r.id,
                container.getTableName(), container.id,
                r.containerlabel,
                r.elementindex,
                r.elementlabel,
                element.getTableName(), element.id,
                )
        else:
            desc = '%s %s' % (r.getTableName(), r.id)
            
        yield r, desc
            
    return


def hasreferral(record, clerk):
    for t in findreferrals(record, clerk):
        return True
    return False


# version
__id__ = "$Id$"

# End of file 
