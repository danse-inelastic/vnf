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


from AbstractForm import AbstractForm as base, InputProcessingError, formactor_action_prefix


class Form( base ):

    class Inventory( base.Inventory ):
        import pyre.inventory
        submit = pyre.inventory.str( 'submit' )
        pass # end of Inventory


    parameters = [] # parameters to edit in the form


    def expand(self, form, errors=None, properties=None, values=None):
        '''expand an existing form with fields from this component'''

        prefix = formactor_action_prefix
        
        if errors:
            p = form.paragraph( cls = 'error' )
            p.text = [
                'The form you filled out contained some errors.',
                'Please look through the values you have entered',
                'and correct any mistakes.',
                ]

        if properties is None: properties = self.parameters
        
        if not values:
            values = [self.inventory.getTraitValue(prop) for prop in properties]
            
        for property, value in zip(properties, values):
            
            meta = self.inventory.getTrait(property).meta

            label = meta.get('label') or property
            name='%s.%s' % (prefix, property)
            id = 'edit_%s' % property
            
            field = form.text(id = id, name = name, label = label, value = value)
            
            tip = _combine( meta.get('tip') )
            if tip: field.help = tip
            
            if errors and property in errors:
                try:
                    msg = errors[property]
                except:
                    msg = meta['tiponerror']
                field.error = _combine(msg)
                pass # end if
            
            continue

        return


    def processUserInputs(self, properties=None):
        '''process user inputs
        '''

        if not properties:
            properties = self.parameters
            
        # check user inputs
        errors = []
        for prop in properties:
            trait = self.inventory.getTrait(prop)
            meta = trait.meta
            validator = meta.get('validator')
            if not validator: continue
            value = self.inventory.getTraitValue(prop)
            try:
                value = validator(value)
            except:
                errors.append(prop)
            else:
                trait.__set__(self.inventory, value)
            continue
        if errors: raise InputProcessingError, errors

        # no error, return the user inputs
        return self.inventory


    pass # end of Form


def _combine(text):
    if text is None: return ''
    if isinstance(text, str): return text
    if isinstance(text, list) or isinstance(text, tuple):
        return ' '.join( text )
    raise NotImplementedError, text


# version
__id__ = "$Id$"

# End of file 
