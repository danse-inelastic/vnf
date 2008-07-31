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


# A "form" component is responsible to gather user inputs and
# transfor them to db.


from pyre.components.Component import Component as base


class Form( base ):

    class Inventory( base.Inventory ):
        import pyre.inventory
        submit = pyre.inventory.str( 'submit' )
        pass # end of Inventory


    def __init__(self, name = 'form', facility = 'form'):
        base.__init__(self, name, facility)
        return


    def processUserInputs(self):
        'process user inputs and save them to db'
        raise NotImplementedError


    def expand(self, form):
        'expand the given form with fields from this form component'
        raise NotImplementedError


    def _init(self):
        base._init(self)
        self.submit = self.inventory.submit 
        return

    pass # end of Form


class InputProcessingError(Exception):

    def __init__(self, errors):
        self.errors = errors
        Exception.__init__(self, errors)
        return
    pass


# version
__id__ = "$Id$"

# End of file 
