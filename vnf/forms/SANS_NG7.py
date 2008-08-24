# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from DBObjectForm import DBObjectForm as base, InputProcessingError


class SANS_NG7(base):


    class Inventory(base.Inventory):

        import pyre.inventory
        Ei = pyre.inventory.str( name = 'Ei', default = 70 )
        Ei.meta['label'] = 'Incident energy'
        Ei.meta['tip'] = (
            'Nominal energy of incident neutrons',
            )
        Ei.meta['tiponerror'] = (
            'Please enter Ei as a positive number. unit: meV',
            )
        

    parameters = [#'short_description',
        'Ei',]
    DBTable = 'SANS_NG7'


    def __init__(self, name = None):
        if name is None:
            name = 'configure_sans_ng7_instrument'

        base.__init__(self, name)

        return


    def processUserInputs(self, *args, **kwds):
        errors = []
        self._verify( 'Ei', errors )
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
