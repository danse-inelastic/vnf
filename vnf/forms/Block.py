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


class Block(base):


    class Inventory(base.Inventory):

        import pyre.inventory
        width = pyre.inventory.str( name = 'width', default = 0.05 )
        width.meta['label'] = 'Width'
        width.meta['tip'] = (
            'Width is the horizontal dimension that is perpendicular to',
            'the incident neutron beam',
            )
        width.meta['tiponerror'] = (
            'Please enter width as a positive number. unit: meter',
            )
        
        height = pyre.inventory.str( name = 'height', default = 0.1 )
        height.meta['label'] = 'Height'
        height.meta['tip'] = (
            'Height is the vertical length',
            )
        height.meta['tiponerror'] = (
            'Please enter height as a positive number. unit: meter',
            )
        
        thickness = pyre.inventory.str( name = 'thickness', default = 0.002 )
        thickness.meta['label'] = 'Thickness'
        thickness.meta['tip'] = (
            'Thickness is the length of the dimension parallel',
            'to the neutron beam',
            )
        thickness.meta['tiponerror'] = (
            'Please enter thickness as a positive number. unit: meter',
            )

    parameters = [#'short_description',
        'width', 'height', 'thickness']
    DBTable = 'Block'


    def __init__(self, name = None):
        if name is None:
            name = 'block'

        base.__init__(self, name)

        return


    def processUserInputs(self, *args, **kwds):
        errors = []
        self._verify( 'width', errors )
        self._verify( 'height', errors )
        self._verify( 'thickness', errors )
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
