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
                configuredscatterer = clerk.getConfiguredScatterer( id )
                label = configuredscatterer.short_description
            # get configuration container
            return 'Settings of %r' % label
        
        
        def expand(self, form, errors = None, scattererlabel = 'sample'):
            '''expand an existing form with fields from this component'''

            director = self.director
            clerk = director.clerk
            configured = clerk.getConfiguredScatterer( self.inventory.id )
            
            p = form.paragraph()
            p.text = [
                'In this form, you can fine-tune your %s.' % scattererlabel,
                ]
            
            p = form.paragraph()
            p.text = [
                'You can change the dimensions of the shape of this %s' % (
                scattererlabel,),
                ]

            configured = clerk.getHierarchy( configured )
            applyconfiguration( configured )
            
            # get shape
            realshape = configured.scatterer.shape.realshape
            # the shape form
            self.inventory.id = realshape.id
            self.parameters = shapeform.parameters
            shapeform.expand(self, form, errors = errors )

            prefix = formactor_action_prefix
            # id should be scatterer's id
            id_field = form.hidden(
                name = '%s.id' % prefix, value = configured.id)

            return
        
        
        def processUserInputs(self):
            'process user inputs and save them to db'

            director = self.director
            clerk = director.clerk

            #get the thing to be edited
            configured = clerk.getConfiguredScatterer( self.inventory.id )
            configured = clerk.getHierarchy( configured )
            
            #get shape configuration
            self.inventory.id = ''
            self.DBTable = shapetype
            shapeinput = shapeform.processUserInputs(self, commit = False)

            # make sure we have a configuration
            if configured.configuration is None:
                #create a configuration
                from vnf.dom.Scatterer import Scatterer
                configuration = clerk.new_dbobject( Scatterer )
                configuration = clerk.getHierarchy( configuration )
                #connect to parent
                configured.configuration_id = configuration.id
                clerk.updateRecord( configured )
                configured.configuration = configuration
                pass # endif

            configuration = configured.configuration
            # is shape in the configuration?
            if configuration.shape is None:
                #compare inputs to old configuration
                old = configured.scatterer.shape.realshape
                if equal_record(old, shapeinput, shapeform.parameters):
                    #nothing to do. no need to create shape configuration
                    pass
                else:
                    #new shape
                    shape = clerk.makeShape( shapetype )
                    shape = clerk.getHierarchy( shape )
                    #transfer user inputs
                    transfer( shapeinput, shape.realshape, shapeform.parameters )
                    #update db
                    clerk.updateRecord( shape.realshape )

                    #attach shape to configuration
                    configuration.shape_id = shape.id
                    clerk.updateRecord( configuration )
                    clerk.getHierarchy(configuration)
                    pass # endif                
            else:
                # there is an existing shape configuration
                if equal_record( configured.scatterer.shape.realshape,
                                 shapeinput, shapeform.parameters ):
                    #this means that the user inputs equal to defaults
                    #remove shape configuration
                    clerk.destroyShape( configured.configuration.shape )
                    configured.configuration.shape_id = ''
                    clerk.updateRecord( configured.configuration )
                    clerk.getHierarchy( configured.configuration )
                    
                else:
                    #update configuration
                    transfer( shapeinput, configured.configuration.shape.realshape,
                              shapeform.parameters )
                    clerk.updateRecord( configured.configuration.shape.realshape )

            return


        def __init__(self):
            shapeform.__init__(self, formname)
            return

        pass # end of Form

    return Form()


def applyconfiguration( configuredscatterer):
    if configuredscatterer.configuration:
        from vnf.components.ScattererConfigurationApplyer import applyer
        applyer( configuredscatterer.scatterer ).apply(
            configuredscatterer.configuration )
        pass # end if
    return


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
