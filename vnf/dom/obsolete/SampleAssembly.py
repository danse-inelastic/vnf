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
    
    from ReferenceSet import ReferenceSet
    class Scatterers( ReferenceSet ):
        name = 'scatterersinsampleassembly'
        import pyre.db
        label = pyre.db.varchar( name = 'label', default = 'sample', length = 16)
        label.meta['tip'] = 'label: sample/sample_holder/furnace'
        pass

    pass # end of SampleAssembly


# version
__id__ = "$Id$"

# End of file 
