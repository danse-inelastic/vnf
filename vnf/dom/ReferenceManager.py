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



class ReferenceManager:



    def __init__(self, db):
        self.db = db
        import journal
        self._debug = journal.debug('reference-manager')
        return
    

    def deleteRecord(self, record, recursive=False):
        if self.referred(record): return
        self._debug.log('This record %s, %s is not referred. Safe to remove' % (
            record.name, record.id))
        self._deleteRecord(record)

        # need to delete records from hidden table. this should somehow
        # be integrated into the DBManager.
        
        from pyre.db._reference import reference
        from vnf.dom._referenceset import referenceset
        from vnf.dom._geometer import registry as geometerregistry

        for name, descriptor in record.__class__.__dict__.iteritems():
            if not isColumnDescriptor(descriptor): continue
            attr = getattr(record, name)
            
            self._debug.log('attribute: name=%s, attr=%s' % (name, attr))
            if isinstance(attr, reference):
                if recursive: 
                    referred = attr.dereference(self.db)
                    self.deleteRecord(referred, recursive=True)
                    
            elif isinstance(attr, referenceset):
                self._debug.log("reference set")
                refset = attr.dereference(self.db)
                # remove references
                for label, element in refset:
                    self._debug.log('label: %s' % label)
                    attr.delete(element, self.db)
                    continue
                if recursive:
                    #remove referred records
                    for label, element in refset:
                        self.deleteRecord(element, recursive=True)
                        continue
                
            elif isinstance(attr, geometerregistry):
                registry = attr.dereference(self.db)
                for element in registry: attr.delete(element, self.db)
                if recursive:
                    for element in registry.itervalues():
                        self.deleteRecord(element, recursive=True)
            continue
        
        return


    def referred(self, record):
        # need to search all records with references and make sure this record is not referred
        from pyre.db.Reference import Reference
        from pyre.db.VersatileReference import VersatileReference
        from vnf.dom._referenceset import _ReferenceTable
        
        from vnf.dom.registry import tableRegistry
        all = tableRegistry.itertables()
        for table in all:
            for name, attr in table.__dict__.iteritems():
                if isinstance(attr, Reference):
                    if attr.referred_table is record.__class__:
                        where = "%s='%s'" % (attr.name, record.id)
                        records = self.db.fetchall(table=table, where=where)
                        n = len(records)
                        if n: return True
                elif isinstance(attr, VersatileReference):
                    # check if this referral is a self referral in referenceset
                    if table is _ReferenceTable and attr.name == 'container': continue
                    
                    ref = attr._format(record)
                    where = "%s='%s'" % (attr.name, ref)
                    #self._debug.log('VersatileReference: table=%s, where=%s' % (
                    #    table.name, where))
                    records = self.db.fetchall(table=table, where=where)
                    n = len(records)
                    if n: return True
                continue
            continue
        return False


    def _deleteRecord(self, record):
        table = record.__class__
        self.db.deleteRow( table, where="id='%s'" % record.id )
        return



from pyre.db.Column import Column
from vnf.dom.ReferenceSet import ReferenceSet
from vnf.dom.Geometer import Geometer
Descriptors = [
    Column,
    ReferenceSet,
    Geometer,
    ]
del Column, ReferenceSet, Geometer
def isColumnDescriptor(candidate):
    for D in Descriptors:
        if isinstance(candidate, D): return True
        continue
    return False

# version
__id__ = "$Id$"

# End of file 
