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
        radius = pyre.inventory.str( name = 'radius', default = 0.01 )
        radius.meta['label'] = 'Radius'
        radius.meta['tip'] = (
            'The radius of the cylinder',
            )
        radius.meta['tiponerror'] = (
            'Please enter radius as a positive number. unit: meter',
            )
        
        height = pyre.inventory.str( name = 'height', default = 0.1 )
        height.meta['label'] = 'Height'
        height.meta['tip'] = (
            'Height is the vertical length',
            )
        height.meta['tiponerror'] = (
            'Please enter height as a positive number. unit: meter',
            )
        

    parameters = [#'short_description',
        'radius', 'height',]
    DBTable = 'Cylinder'


    def __init__(self, name = None):
        if name is None:
            name = 'cylinder'

        base.__init__(self, name)

        return


    def processUserInputs(self, *args, **kwds):
        errors = []
        self._verify( 'radius', errors )
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
