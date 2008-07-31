#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import journal
debug = journal.debug( 'treeviewcreator' )



def create( instrument, actor, director ):
    '''given the db hierarchy of instrument, render a teeview
    '''
    return TreeViewCreator( director, actor ).render( instrument )


import vnf.content as factory
class TreeViewCreator:


    def __init__(self, director, actor):
        self.director = director
        self.actor = actor
        return
    

    def render(self, rootcontainer):
        self._rootcontainer = rootcontainer
        return self(rootcontainer)


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onInstrument(self, instrument):
        return self.onContainer(instrument, instrument.components )
    

    def onSampleAssembly(self, sampleassembly):
        return self.onContainer(sampleassembly, sampleassembly.scatterers)


    def onConfiguredScatterer(self, configured):
        elements = [ configured.scatterer ]
        configuration = configured.configuration
        if configuration: elements.append( configuration )
        return self.onContainer( configured, elements )
        
        
    def onPolyXtalScatterer(self, scatterer):
        elements = [ scatterer.crystal, scatterer.shape ] + scatterer.kernels
        return self.onContainer( scatterer, elements )


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        elements = [ kernel.dispersion ]
        return self.onContainer( kernel, elements )

    
    def onContainer(self, container, elements):
        if container == self._rootcontainer:
            node = self.rootNode( container )
        else:
            node = self.branchNode( container )
            pass

        for element in elements:
            childnode = self( element )
            node.addChild( childnode )
            continue
        
        return node


    def onElement(self, element):
        node =  self.leafNode( element )
        return node


    def onAbstractElement(self, element):
        typename = element.__class__.__name__.lower()
        try:
            realelement = getattr( element, 'real%s' % typename )
            return self(realelement)
        except:
            import traceback
            debug.log( traceback.format_exc() )
            
            director = self.director
            actor = self.actor
            return factory.treeview.leaf(
                'Not Yet Established', 
                factory.actionRequireAuthentication(
                    actor,
                    director.sentry,
                    routine='edit',
                    id = self._rootcontainer.id,
                    editee = "%s,%s" % (typename, element.id)
                    )
                )
        raise RuntimeError, "should not reach here"


    onIDFPhononDispersion = onMonochromaticSource = onIQEMonitor = onCrystal = onBlock = onElement
    onPhononDispersion = onScatteringKernel = onComponent = onScatterer = onShape = onAbstractElement
    

    def rootNode(self, container):
        return self._node( container, factory.treeview )
    
        
    def branchNode(self, container):
        return self._node( container, factory.treeview.branch )
    
    
    def leafNode(self, record):
        return self._node( record, factory.treeview.leaf )
    
    
    def _node(self, record, nodefactory):
        director = self.director
        actor = self.actor
        
        type = record.__class__.__name__
        
        node = nodefactory(
            '%s (%s)' % (record.short_description, type),
            factory.actionRequireAuthentication(
            actor,
            director.sentry,
            routine='edit',
            editee = '%s,%s' % (type.lower(), record.id),
            id = self._rootcontainer.id,
            arguments = { '%s.id' % type.lower(): record.id },
            )
            )
        return node
        
    pass # end of TreeViewCreator




# version
__id__ = "$Id$"

# End of file 
