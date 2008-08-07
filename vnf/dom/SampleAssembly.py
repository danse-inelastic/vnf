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


from OwnedObject import OwnedObject


class SampleAssembly(OwnedObject):

    name = "sampleassemblies"
    
    import pyre.db

    status = pyre.db.varchar( name = 'status', default = 'new', length = 16 )
    template = pyre.db.boolean( name = 'template', default = False)

    import vnf.dom
    scatterers = vnf.dom.referenceSet( name = 'scatterers' )

    pass # end of SampleAssembly


# version
__id__ = "$Id$"

# End of file 
