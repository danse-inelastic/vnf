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
class SampleEnvironment(DbObject):

    name = 'sampleenvironments'

    import pyre.db

    #unit: K
    temperature = pyre.db.real( name = 'temperature', default = 300 )

    #unit: Tesla
    magnetic_field = pyre.db.doubleArray(name = 'magnetic_field', default = [0,0,0] )

    #unit: atm
    pressure = pyre.db.real( name = 'pressure', default = 1. )
    
    pass # end of SampleEnvironment


# version
__id__ = "$Id$"

# End of file 
