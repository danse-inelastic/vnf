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


from DbObject import DbObject


class SANS_NG7(DbObject):
    
    name = "SANS_NG7"

    target = 'SANS_NG7' # target of configuration
    
    import pyre.db

    Ei = pyre.db.real( name = 'Ei', default = 70 )
    
    pass # end of Instrument


# version
__id__ = "$Id$"

# End of file 
