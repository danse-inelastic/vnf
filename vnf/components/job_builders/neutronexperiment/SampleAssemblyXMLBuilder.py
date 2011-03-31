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


    def render(self, sampleassembly, db=None, dds=None, orm=None):
        self.db = db
        self.dds = dds
        self.orm = orm

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

        # get scatterers from db
        scatterers_ref = sampleassembly.scatterers
        if not scatterers_ref:
            raise RuntimeError, "Sample assmebly %s has no scatterers" % sampleassembly.id
        scatterers = [s for n,s in scatterers_ref.dereference(self.db)]

        # calculate absolute coordinates of scatterers
        from vnf.utils.neutron_experiment_simulations.geometry \
             import calculateComponentAbsoluteCoordinates, toangles
        calculateComponentAbsoluteCoordinates(
            scatterers, 
            getname = lambda s: s.scatterername
            )
        
        for scatterer in scatterers:
            self.dispatch( scatterer )
            continue

        self._write( '' )
        self._write( '<LocalGeometer registry-coordinate-system="InstrumentScientist">' )
        self._indent()
        for scatterer in scatterers:
            name = scatterer.short_description.replace( ' ', '_' )
            attrs = {
                'name': name,
                'position': tuple(scatterer.position),
                'orientation': tuple(toangles(scatterer.orientation)),
                }
            self._write( '<Register %s/>' % attribs_str( attrs ) )
            continue
        self._outdent()
        self._write( '</LocalGeometer>' )

        self._postElement( sampleassembly )
        return


    def onScatterer(self, scatterer):
        # at this moment we only know to do polycrystalline sample
        # should add sample phase information into the Scatterer data object
        return self.onPolyCrystalScatterer(scatterer)


    def onPolyCrystalScatterer(self, scatterer):
        name = scatterer.short_description.replace( ' ', '_' )
        attrs = {
            'name': name,
            }
        self._write( '<PowderSample %s>' % attribs_str(attrs) )
        self._indent()
        
        self.onShape(scatterer.shape.dereference(self.db))

        # now need to create a xyz file
        matterrecord = scatterer.matter.dereference(self.db)
        orm = self.orm
        from vnf.dom.AtomicStructure import Structure
        matter = orm.load(Structure, matterrecord.id)
        matter.description = '' # right now mcvine cannot parse description
        xyzfilename = self._create_xyzfile(matter)
        self.filenames.append(xyzfilename)

        self._write('')
        self._write( '<Phase type="crystal">' )
        self._indent()
        self._write( '<ChemicalFormula>%s</ChemicalFormula>' % (
            matter.getChemicalFormula(),) )
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


    def onCylinder(self, cylinder):
        # the cylinder here is actually called hollowcylinder in instrument package
        # convert to "HollowCylinder" that instrument xml renderer recognizes
        class HollowCylinder: pass
        hc = HollowCylinder()
        hc.in_radius = cylinder.innerradius
        hc.out_radius = cylinder.outerradius
        hc.height = cylinder.height
        return self.onHollowCylinder(hc)
    

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


    def _create_xyzfile(self, structure):
        import os
        filename = '%s.xyz' % self.orm(structure).id
        filepath = os.path.join( self.directory, filename )
        
        content = makeXYZfileContent(
            structure,
            use_primitive_unitcell=1,
            use_fractional_coordinates=1,
            latticeAsDescription = True,
            )
        
        open( filepath, 'w' ).write( '\n'.join( content ) )
        return filename


    pass # end of Builder



def attribs_str( attributes ):
    return ' '.join(
        ['%s="%s"' % (k, attributes.get(k)) for k in attributes ] )



from vnf.utils.atomicstructure import makeXYZfileContent


# version
__id__ = "$Id$"

# End of file 
