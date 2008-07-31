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


from pyre.weaver.mills.XMLMill import XMLMill
from instrument.geometry.pml.Renderer import Renderer as ShapeRenderer


class Builder(ShapeRenderer, XMLMill):
    

    def __init__(self, filepath):
        self.filepath = filepath
        XMLMill.__init__(self)
        return


    def render(self, sampleassembly):
        self.dispatch(sampleassembly)
        contents = self._rep
        open(self.filepath, 'w').write( '\n'.join( contents ) )
        return


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onSampleAssembly(self, sampleassembly):
        name = sampleassembly.short_description.replace( ' ', '_' )

        self._write( '<!DOCTYPE sampleassembly>' )

        attrs = {
            'name': name,
            }
            
        self._preElement( sampleassembly, attrs )
        
        for scatterer in sampleassembly.scatterers:
            self.dispatch( scatterer )
            continue

        self._write( '' )
        self._write( '<LocalGeometer registry-coordinate-system="InstrumentScientist">' )
        self._indent()
        for scatterer in sampleassembly.scatterers:
            name = scatterer.short_description.replace( ' ', '_' )
            attrs = {
                'name': name,
                'position': (0,0,0),
                'orientation': (0,0,0),
                }
            self._write( '<Register %s/>' % attribs_str( attrs ) )
            continue
        self._outdent()
        self._write( '</LocalGeometer>' )

        self._postElement( sampleassembly )
        return


    def onConfiguredScatterer(self, configured):
        prototype = configured.scatterer
        configuration = configured.configuration
        from ScattererConfigurationApplyer import applyer
        applyer( prototype ).apply( configuration )
        return self.dispatch( prototype )


    def onScatterer(self, scatterer):
        matter = scatterer.matter.realmatter
        mattertype = matter.__class__.__name__
        handler = 'on%sScatterer' % mattertype
        return getattr(self, handler)( scatterer )


    def onPolyCrystalScatterer(self, scatterer):
        name = scatterer.short_description.replace( ' ', '_' )
        attrs = {
            'name': name,
            }
        self._write( '<PowderSample %s>' % attribs_str(attrs) )
        self._indent()
        
        self.dispatch(scatterer.shape)

        # now need to create a xyz file
        polyxtal = scatterer.matter.realmatter
        xyzfilename = '%s.xyz' % polyxtal.id

        self._write('')
        self._write( '<Phase type="crystal">' )
        self._indent()
        self._write( '<ChemicalFormula>%s</ChemicalFormula>' % (
            polyxtal.chemical_formula,) )
        self._write( '<xyzfile>%s</xyzfile>' % xyzfilename )
        self._outdent()
        self._write( '</Phase>' )
        self._write('')

        self._outdent()
        self._write( '</PowderSample>' )
        return


    def onShape(self, shape):
        self._preElement( shape, {} )
        realshape = shape.realshape
        self.dispatch( realshape )
        self._postElement( shape )
        return


    def _preElement(self, element, attributes):
        self._write( '' )
        t = element.__class__.__name__
        self._write(
            "<%s %s>" % (t, attribs_str( attributes ) ) )
        self._indent()
        return


    def _postElement(self, element):
        t = element.__class__.__name__

        self._outdent()

        self._write( '</%s>' % t )
        self._write( '' )
        return


    pass # end of Builder


def attribs_str( attributes ):
    return ' '.join(
        ['%s="%s"' % (k, attributes.get(k)) for k in attributes ] )


# version
__id__ = "$Id$"

# End of file 
