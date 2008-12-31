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


# role-(instrument simulation privilege) relation


from ACL_Privilege import ACL_Privilege as base


class ACL_InstrumentSimulationPrivilege(base):

    name = "acl_instrumentsimulationprivileges"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    role = pyre.db.varchar(name='role', length=64)
    role.constraints = 'REFERENCES roles (id)'

    instrument = pyre.db.varchar(name='instrument', length=64)
    instrument.constraints = 'REFERENCES instruments (id)'
    
    pass # end of ACL_InstrumentSimulationPrivilege


def inittable(db):
    grant(
        'roleD00001-coredeveloper',
        ['any'],
        db,
        idgenerator=gid)
    
    grant(
        'roleU00002-demouser',
        ['TestInstrument',
         ],
        db,
        idgenerator=gid)
    return


from Role import Role
from Instrument import Instrument
def grant(roleid, instrumentids, db, idgenerator=None):
    for instrumentid in instrumentids:
        row = ACL_InstrumentSimulationPrivilege()
        row.id = idgenerator()
        row.role = roleid
        row.instrument = instrumentid
        db.insertRow(row)
        continue
    return


import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    prefix = 'acl_instrumentsimulationprivilege-'
    return prefix + ''.join(random.sample(alphabet, 24))


def checkInstrumentSimulationPrivilege(roleid, instrumentid, db):
    '''check if the given role has privilege to run the given instrument
    '''
    Table = ACL_InstrumentSimulationPrivilege
    where = "role='%s' and instrument='%s'" % (roleid, instrumentid)
    return bool(db.fetchall(Table, where=where))
from Instrument import Instrument
from acl import registerPrivilegeCheckingHandler
registerPrivilegeCheckingHandler(Instrument, checkInstrumentSimulationPrivilege)


# version
__id__ = "$Id$"

# End of file 
