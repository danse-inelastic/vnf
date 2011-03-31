# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import *

from vnf.dom.AtomicStructure import StructureTable

def select_matter_clause(db):
    '''create a sqlalchemy select cluase for the atomicstructure(matter) table

    columns:
      * id
      * short_description
    '''
    
    sM = db._tablemap.TableToSATable(StructureTable)
    matterq = sqlalchemy.select(
        [sM.c.short_description.label('short_description'),
         sM.c.id.label('id'),
         ]
        )
    return matterq



# version
__id__ = "$Id$"

# End of file 
