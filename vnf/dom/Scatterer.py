# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DbObject import DbObject as base
class Scatterer(base):

    name = 'scatterers'

    import pyre.db

    matter_id = pyre.db.varchar( name = 'matter_id', length = 100)
    matter_id.meta['tip'] = 'matter_id'
    
    shape_id = pyre.db.varchar( name = 'shape_id', length = 100)
    shape_id.meta['tip'] = 'shape_id'

    template = pyre.db.boolean( name = 'template', default = False)
    basic = pyre.db.boolean( name = 'basic', default = False)
    basic.meta['tip'] = (
        'Is this scatterer basic? basic scatterers are presented to novice users'
        )

    from ReferenceSet import ReferenceSet
    class Kernels( ReferenceSet ):
        name = 'kernelsforscatterer'
        pass

    pass # end of Scatterer


# version
__id__ = "$Id$"

# End of file 
