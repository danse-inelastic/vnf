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


class ARCSconfiguration(DbObject):
    
    name = "arcsconfigurations"
    
    import pyre.db

    Ei = pyre.db.real( name = 'Ei', default = 70 )
    Eiresolution = pyre.db.real( name = 'Eiresolution', default = 0.03 )
    
    pass # end of Instrument


# version
__id__ = "$Id$"

# End of file 
