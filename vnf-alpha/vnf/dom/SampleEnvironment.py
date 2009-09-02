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

    import dsaw.db

    #unit: K
    temperature = dsaw.db.real( name = 'temperature', default = 300 )

    #unit: Tesla
    magnetic_field = dsaw.db.doubleArray(name = 'magnetic_field', default = [0,0,0] )

    #unit: atm
    pressure = dsaw.db.real( name = 'pressure', default = 1. )
    
    pass # end of SampleEnvironment


# version
__id__ = "$Id$"

# End of file 
