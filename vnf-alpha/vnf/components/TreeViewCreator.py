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



def create( instrument, director ):
    '''given the db hierarchy of instrument, render a teeview
    '''
    return TreeViewCreator( director ).render( instrument )


import vnf.content as factory
class TreeViewCreator:


    def __init__(self, director):
        self.director = director
        return
    

    def render(self, rootcontainer):
        self._rootcontainer = rootcontainer
        return self(rootcontainer)


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onNeutronExperiment(self, experiment):
        db = self.director.clerk.db
        elements = [
            experiment.instrument_configuration.dereference(db),
            ]
        if experiment.sampleassembly:
            elements.append(experiment.sampleassembly.dereference(db))
        #, experiment.job ]
        return self.onContainer( experiment, elements )


    def onJob(self, job):
        #elements = [ job.computation_server ]
        #return self.onContainer( job, elements )
        label = '%s (%s)' % (
            element.short_description, element.__class__.__name__ )
        branch = factory.treeview.branch( label )
        return self.onElement( job )


    def onInstrument(self, instrument):
        db = self.director.clerk.db
        components = instrument.components.dereference(db)
        components = [ c for n,c in components ]
        return self.onContainer(instrument, components )


    onInstrumentConfiguration = onInstrument


    def onSampleComponent(self, component):
        return
    

    def onSampleAssembly(self, sampleassembly):
        db = self.director.clerk.db
        scatterers = [ c for n,c in sampleassembly.scatterers.dereference(db) ]
        return self.onContainer(sampleassembly, scatterers)


    def onScatterer(self, scatterer):
        db = self.director.clerk.db
        
        elements = [
            scatterer.matter.dereference(db),
            scatterer.shape.dereference(db) ]

        kernels = [ k for n,k in scatterer.kernels.dereference(db) ]
        elements += kernels
        return self.onContainer( scatterer, elements )


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        db = self.director.clerk.db
        elements = [ kernel.dispersion.dereference(db) ]
        return self.onContainer( kernel, elements )

    
    def onContainer(self, container, elements):
        if container == self._rootcontainer:
            node = self.rootNode( container )
        else:
            node = self.branchNode( container )
            pass

        self._add_props( container, node )

        for element in elements:
            childnode = self( element )
            if childnode is not None: node.addChild( childnode )
            continue
        
        return node


    def onElement(self, element):

        label = '%s (%s)' % (
            element.short_description, element.__class__.__name__ )
        branch = factory.treeview.branch( label )

        self._add_props( element, branch )
        return branch


    def onAbstractElement(self, element):
        typename = element.__class__.__name__.lower()
        try:
            realelement = getattr( element, 'real%s' % typename )
            return self(realelement)
        except:
            import traceback
            debug.log( traceback.format_exc() )
            return factory.treeview.leaf('Not Yet Established')
        raise RuntimeError, "should not reach here"


    onSNSModerator \
                   = onMonochromaticSource \
                   = onChanneledGuide \
                   = onT0Chopper = onFermiChopper \
                   = onQEMonitor = onQMonitor = onTofMonitor = onEMonitor = onSphericalPSD\
                   = onNeutronRecorder \
                   = onDetectorSystem_fromXML \
                   = onPolyCrystal = onDisordered \
                   = onPhonons \
                   = onSANSSphereModelKernel \
                   = onCrystal \
                   = onBlock = onCylinder \
                   = onElement

    onSQEKernel \
                = onElement
    #onMatter = onPhonons = onScatteringKernel = onComponent = onShape = onElement
    

    def rootNode(self, container):
        return self._node( container, factory.treeview )
    
        
    def branchNode(self, container):
        return self._node( container, factory.treeview.branch )
    
    
    def leafNode(self, record):
        return self._node( record, factory.treeview.leaf )
    
    
    def _node(self, record, nodefactory):
        type = record.__class__.__name__
        
        node = nodefactory(
            '%s (%s)' % (record.short_description, type),
            )
        return node


    def _add_props(self, element, branch, props = None):
        'add properties of element to the given tree view branch'
        excluded_cols = [
            'id', 'creator', 'date', 'short_description',
            ]
        if props is None:
            props = []
            columns = element.getColumnNames()
            for col in columns:
                if col in excluded_cols: continue
                props.append( col )
                continue
            pass # endif

        for prop in props:
            value = getattr( element, prop )
            value = str(value).replace( '\n', '    ' )
            leaf = factory.treeview.leaf( '%s: %s' % (
                prop, value) )
            branch.addChild( leaf )
            continue
        return
        
    pass # end of TreeViewCreator




# version
__id__ = "$Id$"

# End of file 
