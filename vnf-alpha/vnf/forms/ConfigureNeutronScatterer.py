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
    
    mattertable = getattr(
        __import__( 'vnf.dom.%s' % mattertype, {}, {}, [''] ), mattertype)
    matterform = getattr(
        __import__( 'vnf.forms.%s' % mattertype, {}, {}, [''] ), mattertype)
    
    
    class Form( shapeform, matterform ):

        class Inventory( shapeform.Inventory, matterform.Inventory ):
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

            form.paragraph().text = ['<h2>Shape</h2>']
            
            p = form.paragraph()
            # get shape
            shape = scatterer.shape.dereference(director.clerk.db)
            p.text = [
                'Your %s is a %s (id=%s).' % (
                scattererlabel, shapetype.lower(), shape.id),
                'You can change the dimensions here:',
                ]

            # the shape form
            # all shape forms are dbobject forms. they need following
            # class varaibles:
            #    parameters
            #    DBTable
            self.parameters = shapeform.parameters
            self.DBTable = shapetable
            shapeform.expand(self, form, errors = errors, id = shape.id)

            form.paragraph().text = ['<h2>Matter form</h2>']
            p = form.paragraph()
            p.text = [
                'Your %s is a %s (id=%s).' % (
                scattererlabel, mattertype.lower(), scatterer.matter.id),
                ]

            # the matter form
            #self.parameters = matterform.parameters
            #self.DBTable = mattertable
            matterform.expand(self, form, id = scatterer.matter.id, errors = errors)

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
            self.inventory.id = scatterer.shape.id
            self.DBTable = shapetype
            shapeinput = shapeform.processUserInputs(self)

            #transfer user inputs
            #shape = scatterer.shape.dereference( director.clerk.db )
            #transfer( shapeinput, shape, shapeform.parameters )
            #update db
            #clerk.updateRecord( shape )

            #matter
            self.inventory.id = scatterer.matter.id
            self.DBTable = mattertype
            matterinput = matterform.processUserInputs(self)
            #matter = scatterer.matter.dereference(director.clerk.db)
            #transfer(matterinput, matter, matterform.parameters)
            return


        def __init__(self):
            shapeform.__init__(self, formname)
            matterform.__init__(self, formname)
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
