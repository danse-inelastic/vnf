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
        import os
        self.directory = os.path.dirname(filepath)
        XMLMill.__init__(self)
        return


    def render(self, sampleassembly, db=None, dds=None):
        self.db = db
        self.dds = dds

        self.filenames = []
        
        self.dispatch(sampleassembly)
        contents = self._rep
        open(self.filepath, 'w').write( '\n'.join( contents ) )
        return


    def getFilenames(self): return self.filenames


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

        scatterers_ref = sampleassembly.scatterers
        if not scatterers_ref:
            raise RuntimeError, "Sample assmebly %s has no scatterers" % sampleassembly.id
        scatterers = scatterers_ref.dereference(self.db)
        
        for name, scatterer in scatterers:
            self.dispatch( scatterer )
            continue

        self._write( '' )
        self._write( '<LocalGeometer registry-coordinate-system="InstrumentScientist">' )
        self._indent()
        for name, scatterer in scatterers:
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


    def onScatterer(self, scatterer):
        matter = scatterer.matter.dereference(self.db)
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
        
        self.onShape(scatterer.shape.dereference(self.db))

        # now need to create a xyz file
        polyxtal = scatterer.matter.dereference(self.db)
        xyzfilename = self._create_xyzfile(polyxtal)
        self.filenames.append(xyzfilename)

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
        class Shape: pass
        _ = Shape()
        self._preElement( _, {} )
        self.dispatch( shape )
        self._postElement( _ )
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


    def _create_xyzfile(self, crystal):
        import os
        filename = '%s.xyz' % crystal.id
        filepath = os.path.join( self.directory, filename )

        contents = crystal2xyz( crystal )

        open( filepath, 'w' ).write( '\n'.join( contents ) )
        return filename


    pass # end of Builder



def attribs_str( attributes ):
    return ' '.join(
        ['%s="%s"' % (k, attributes.get(k)) for k in attributes ] )



def crystal2xyz( crystal ):
    # convert a crystal db record to a xyz file
    lattice = crystal.cartesian_lattice
    coords= crystal.fractional_coordinates
    atoms = crystal.atom_symbols
    
    from numpy import array
    coords = array(coords)
    coords.shape = -1,3
    
    assert len(atoms) == len(coords)

    contents = []
    contents.append( '%d' % len(atoms) )
    contents.append( ' '.join( [ '%s' % a for a in lattice ] ) )
    for atom, coord in zip( atoms, coords):
        contents.append(
            '%s %s' % (atom, ' '.join( [ '%s' % x for x in coord] ) )
            )
        continue
    
    return contents


# version
__id__ = "$Id$"

# End of file 
