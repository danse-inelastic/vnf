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


from Actor import Actor, action_link, action, actionRequireAuthentication
from vnf.weaver import action_href
from PyHtmlTable import PyHtmlTable

class Sample(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'sample' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of samples')
        document.description = ''
        document.byline = 'byline'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatterers = clerk.indexScatterers(where='template=True').values()
        scatterers = [ clerk.getHierarchy(scatterer) for scatterer in scatterers]
        samples = scatterers
            
        p = document.paragraph()
        import operator
        generators = [
            operator.attrgetter( 'short_description' ),
            lambda s: s.matter.realmatter.chemical_formula,
            lambda s: format_lattice_parameters(s.matter.realmatter),
            lambda s: format_atoms(s.matter.realmatter),
            lambda s: format_shape(s.shape.realshape),
            ]

        columnTitles = [
            'Sample description','Chemical formula', 'Cartesian lattice', 
            'Atom positions', 'Shape']

        t=PyHtmlTable(len(samples), len(columnTitles), {'width':'90%', 'border':2, 'bgcolor':'white'})
        # first row for labels 
        for colNum, col in enumerate(columnTitles):
            t.setc(0,colNum,col)

        # other rows for values
        for row, sample in enumerate( samples ):
            #first put in the radio button
            #selection = "<input type='radio' name='actor.form-received.kernel_id' value="+sample.id+" id='radio'/>"
            #t.setc(row+1, 0, selection)
            for colNum, generator in enumerate( generators ):
                value = generator( sample )
                t.setc(row+1,colNum,value)
        
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [action_link(
            actionRequireAuthentication(
            'sampleInput', 
            director.sentry,
            label = 'Add a new sample',
            routine = 'default'            
            ),  director.cgihome),'<br>']

        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample, self).__init__(name)
        return



def format_lattice_parameters(matter):
    lattice = matter.cartesian_lattice
    import numpy
    lattice = numpy.array(lattice)
    lattice.shape = -1,3
    return '<br>'.join( [ format_vector( vec ) for vec in lattice ] )


def format_atoms(matter):
    coords = matter.fractional_coordinates
    import numpy
    coords = numpy.array(coords)
    coords.shape = -1,3
    atom_symbols = matter.atom_symbols
    return '<br>'.join(
        [ '%s: %s' % (symbol, format_vector(coord) )
          for symbol, coord in zip(atom_symbols, coords) ]
        )


def format_vector( v ):
    x,y,z = v
    return '%.5f, %.5f, %.5f' % (x,y,z)


class ShapeFormatter:

    def __call__(self, shape):
        handler = 'on%s' % shape.__class__.__name__
        handler = getattr( self, handler )
        return handler( shape )


    def onBlock(self, block):
        texts = [
            'Plate',
            'thickness=%.3fcm' % (block.thickness * 100),
            'height=%.3fcm' % (block.height * 100),
            'width=%.3fcm' % (block.width * 100),
            ]
        return '<br>'.join( texts )
    
    def onCylinder(self, cylinder):
        texts = [
            'Cylinder',
            'height=%.3fcm' % (cylinder.height * 100),
            'inner radius=%.3fcm' % (cylinder.innerradius * 100),
            'outer radius=%.3fcm' % (cylinder.outerradius * 100),
            ]
        return '<br>'.join( texts )

def format_shape( shape ):
    return ShapeFormatter()( shape )

# version
__id__ = "$Id$"

# End of file 
