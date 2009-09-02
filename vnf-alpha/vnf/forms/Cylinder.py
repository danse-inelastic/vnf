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



from DBObjectForm import DBObjectForm as base, InputProcessingError


class Cylinder(base):


    class Inventory(base.Inventory):

        import pyre.inventory
        outerradius = pyre.inventory.str( name = 'outerradius', default = 0.01 )
        outerradius.meta['label'] = 'Outer radius (cm)'
        outerradius.meta['tip'] = (
            'The outer radius of the cylinder',
            )
        outerradius.meta['tiponerror'] = (
            'Please enter outer radius as a positive number. unit: meter',
            )
        
        innerradius = pyre.inventory.str( name = 'innerradius', default = 0.01 )
        innerradius.meta['label'] = 'Inner radius (cm)'
        innerradius.meta['tip'] = (
            'The inner radius of the cylinder',
            )
        innerradius.meta['tiponerror'] = (
            'Please enter inner radius as a positive number. unit: meter',
            )
        
        height = pyre.inventory.str( name = 'height', default = 0.1 )
        height.meta['label'] = 'Height (cm)'
        height.meta['tip'] = (
            'Height is the vertical length',
            )
        height.meta['tiponerror'] = (
            'Please enter height as a positive number. unit: meter',
            )
        

    parameters = [#'short_description',
        'outerradius', 'innerradius', 'height',]
    DBTable = 'Cylinder'


    def __init__(self, name = None):
        if name is None:
            name = 'cylinder'

        base.__init__(self, name)

        return


    def processUserInputs(self, *args, **kwds):
        errors = []
        self._verify( 'outerradius', errors )
        self._verify( 'innerradius', errors )
        self._verify( 'height', errors )
        if len(errors): raise InputProcessingError, errors
        return base.processUserInputs(self, *args, **kwds)


    def _verify(self, prop, errors):
        value = getattr( self.inventory, prop )
        try:
            value = float(value)
            if value < 0: errors.append( prop )
        except:  errors.append(prop)
        return
    

# version
__id__ = "$Id$"

# End of file 
