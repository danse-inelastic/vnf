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


class Builder:

    sampleassemblyxmlfilename = 'sampleassembly.xml'

    def __init__(self, path):
        self.path = path
        return
    

    def render(self, sampleassembly):
        
        # the sample assembly xml
        from SampleAssemblyXMLBuilder import Builder
        import os
        filename = os.path.join( self.path, self.sampleassemblyxmlfilename )
        Builder(filename).render(sampleassembly)

        # xml files for scatterers
        from McvineScattererXMLBuilder import Builder
        builder = Builder(self.path)
        scatterers = sampleassembly.scatterers
        for scatterer in scatterers:
            builder.render( scatterer )
            continue

        # other data files
        from McvineSampleAssemblyDatafilesCollector import Collector
        collector = Collector(self.path)
        collector.render( sampleassembly )

        # odb file for the sample assembly
        options = self._build_odb( )
        
        return options


    def _build_odb(self):
        contents = [
            'from mcni.pyre_support import componentfactory',
            
            #the next line should be rendered kernel requirements
            'import mccomponents.sample.phonon.xml',
            
            "def sample(): return componentfactory('samples', 'SampleAssemblyFromXml' )('sampleassembly')",
            ]
        
        path = self.path
        filename = 'sampleassembly.odb'
        import os
        filepath = os.path.join( path, filename )
        open( filepath, 'w').write( '\n'.join( contents ) )
        
        options = {}
        options[ 'sample' ] = 'sampleassembly'
        options[ 'sampleassembly.xml' ] = self.sampleassemblyxmlfilename
        
        return options


    pass # Builder


# version
__id__ = "$Id$"

# End of file 
