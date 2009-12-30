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


def create(db):
    newInstrument(
        db=db,
        id='Pharos',
        short_description='Pharos. place holder',
        long_description='long description here',
        category='ins',
        creator='vnf', date='08/11/2008',
        componentinfos=[],
        )
    return


from _utils import new_id, newInstrument, componentinfo as ci


# version
__id__ = "$Id$"

# End of file 
