# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from PhononDispersion import PhononDispersion as base
class IDFPhononDispersion(base):

    name = 'idfphonondispersions'

    import pyre.db

    origin = pyre.db.varchar( name = 'origin', length = 1024 )
    origin.meta['tip'] = 'origin of this dispersion. BvK? or else?'

    pass # end of IDFPhononDispersion



def inittable(db):
    def disp( id, origin ):
        r = IDFPhononDispersion()
        r.id = id
        r.origin = origin
        return r

    records = [
        disp( 'idf-phonon-dispersion-fccNi-0', 'bvk' ),
        ]
    
    for r in records: db.insertRow( r )
    return


# version
__id__ = "$Id$"

# End of file 
