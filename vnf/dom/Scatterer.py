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

    matter = pyre.db.versatileReference( name = 'matter', tableRegistry = tableRegistry)
    shape = pyre.db.versatileReference( name = 'shape', tableRegistry = tableRegistry)

    basic = pyre.db.boolean( name = 'basic', default = False)
    basic.meta['tip'] = (
        'Is this scatterer basic? basic scatterers are presented to novice users'
        )

    import vnf.dom
    kernels = vnf.dom.referenceSet( name = 'kernels' )

    pass # end of Scatterer


# version
__id__ = "$Id$"

# End of file 
