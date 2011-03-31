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




"""
render sample assembly xml file from just one scatterer by treating scatterer
as a sample assembly with one scatterer
"""


from SampleAssemblyXMLBuilder import Builder as base, attribs_str
class Builder(base):
    

    def render(self, scatterer, db=None, dds=None, orm=None):
        self.db = db
        self.dds = dds
        self.orm = orm

        self.filenames = []
        
        self._render(scatterer)
        contents = self._rep
        open(self.filepath, 'w').write( '\n'.join( contents ) )
        return


    def _render(self, scatterer):
        # name of the sample assembly
        sa_name = scatterer.short_description.replace( ' ', '_') + '_sample_assembly'

        self._write( '<!DOCTYPE sampleassembly>' )

        attrs = {
            'name': sa_name,
            }

        class SampleAssembly: pass
        sampleassembly = SampleAssembly()
        self._preElement( sampleassembly, attrs )

        self.onScatterer(scatterer)

        self._write( '' )
        self._write( '<LocalGeometer registry-coordinate-system="InstrumentScientist">' )
        self._indent()
        # scatterer name
        name = scatterer.short_description.replace( ' ', '_' )

        # position
        position = scatterer.position
        if position is None: position = 0,0,0
        else: position = tuple(position)
        
        # orientation
        orientation = scatterer.orientation
        from vnf.utils.neutron_experiment_simulations.geometry import toangles
        orientation = toangles(orientation)
        
        attrs = {
            'name': name,
            'position': position ,
            'orientation': orientation,
            }
        self._write( '<Register %s/>' % attribs_str( attrs ) )
        self._outdent()
        self._write( '</LocalGeometer>' )

        self._postElement( sampleassembly )
        return


    pass # end of Builder



# version
__id__ = "$Id$"

# End of file 
