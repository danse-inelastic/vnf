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


# a special instrument for the purpose of supporting privilege checking

def create(db):
    newInstrument(
        db=db,
        id='any',
        short_description='Special instrument for privilege checking',
        long_description='''Special fake instrument for privilege checking''',
        category='Test',
        creator='vnf',
        date='12/29/2008',
        componentinfos=[],
        status = 'offline',
        )
    
    return


from _utils import new_id, newInstrument, componentinfo as ci


# version
__id__ = "$Id$"

# End of file 
