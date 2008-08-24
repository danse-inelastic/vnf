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


from vnf.forms.DBObjectForm import InputProcessingError, formactor_action_prefix
from vnf.components.Actor import action_link, actionRequireAuthentication


def form( name, mattertype, shapetype ):

    formname = name

    shapetable = getattr(
        __import__( 'vnf.dom.%s' % shapetype, {}, {}, [''] ), shapetype)
    shapeform = getattr(
        __import__( 'vnf.forms.%s' % shapetype, {}, {}, [''] ), shapetype)
    
    #mattertable = getattr(
    #    __import__( 'vnf.dom.%s' % mattertype, {}, {}, [''] ), mattertype)
    #matterform = getattr(
    #    __import__( 'vnf.forms.%s' % mattertype, {}, {}, [''] ), mattertype)
    
    
    class Form( shapeform ):

        class Inventory( shapeform.Inventory ):
            import pyre.inventory
            pass # end of Inventory


        def legend(self):
            'return a legend string'
            id = self.inventory.id
            if empty_id( id ):
                label = "neutron scatterer"
            else:
                clerk = self.director.clerk
                scatterer = clerk.getScatterer( id )
                label = scatterer.short_description
            # get configuration container
            return 'Settings of %r' % label
        
        
        def expand(self, form, errors = None, scattererlabel = 'sample'):
            '''expand an existing form with fields from this component'''

            director = self.director
            clerk = director.clerk
            scatterer = clerk.getScatterer( self.inventory.id )
            
            p = form.paragraph()
            p.text = [
                'In this form, you can fine-tune your %s.' % scattererlabel,
                ]
            
            p = form.paragraph()
            p.text = [
                'You can change the dimensions of the shape of this %s' % (
                scattererlabel,),
                ]

            # get shape
            shape = scatterer.shape.dereference(director.db)
            # the shape form
            self.inventory.id = shape.id
            self.parameters = shapeform.parameters
            shapeform.expand(self, form, errors = errors )

            prefix = formactor_action_prefix
            # id should be scatterer's id
            id_field = form.hidden(
                name = '%s.id' % prefix, value = scatterer.id)

            return
        
        
        def processUserInputs(self):
            'process user inputs and save them to db'

            director = self.director
            clerk = director.clerk

            #get the thing to be edited
            scatterer = clerk.getScatterer( self.inventory.id )
            
            #get shape configuration
            self.inventory.id = ''
            self.DBTable = shapetype
            shapeinput = shapeform.processUserInputs(self, commit = False)

            #transfer user inputs
            shape = scatterer.shape.dereference( director.db )
            transfer( shapeinput, shape, shapeform.parameters )
                
            #update db
            clerk.updateRecord( shape )
            return


        def __init__(self):
            shapeform.__init__(self, formname)
            return

        pass # end of Form

    return Form()


def transfer( src, target, props ):
    for prop in props:
        setattr( target, prop, getattr( src, prop ) )
        continue
    return

def equal_record( record1, record2, props):
    f = open( '/tmp/debug-linjiao1.log', 'w' )
    for prop in props:
        print >>f, '%r:%r' % (getattr(record1, prop), getattr(record2, prop) )
        if getattr( record1, prop ) != getattr( record2, prop ): return False
        continue
    return True

from vnf.components.misc import empty_id


# version
__id__ = "$Id$"

# End of file 
