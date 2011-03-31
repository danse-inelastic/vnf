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
    

    def render(self, target, director=None):
        self.director = director
        clerk = director.clerk
        db = clerk.db; orm = clerk.orm
        dds = director.dds
        
        self.db = db; self.dds = dds; self.orm = orm
        handler = '_on%s' % target.__class__.__name__
        return getattr(self, handler)(target)


    def _onScatterer(self, scatterer):
        db = self.db; dds = self.dds; orm = self.orm
        self.dependencies = []
        self.filenames = []
        
        # the sample assembly xml
        from SampleAssemblyXMLfromOneScatterer import Builder
        filename = self.sampleassemblyxmlfilename
        filepath = self._path(filename)
        builder = Builder(filepath)
        builder.render(scatterer, db=db, dds=dds, orm=orm)
        self.filenames.append(filename)
        self.filenames += builder.getFilenames()
        del builder

        # xml files for scatterers
        from McvineScattererXMLBuilder import Builder
        builder = Builder(self.path)
        builder.render(scatterer, director=self.director)
        self.dependencies += builder.getDependencies()
        self.filenames += builder.getFilenames()

        # odb file for the sample assembly
        self.options = self._build_odb( )
        return


    def _onSampleAssembly(self, sampleassembly):
        orm = self.orm; db = self.db; dds = self.dds
        self.dependencies = []
        self.filenames = []
        
        # the sample assembly xml
        from SampleAssemblyXMLBuilder import Builder
        filename = self.sampleassemblyxmlfilename
        filepath = self._path(filename)
        builder = Builder(filepath)
        builder.render(sampleassembly, db=db, dds=dds, orm=orm)
        self.filenames.append(filename)
        self.filenames += builder.getFilenames()
        del builder

        # xml files for scatterers
        from McvineScattererXMLBuilder import Builder
        builder = Builder(self.path)
        scatterers = sampleassembly.scatterers.dereference(db)
        for name, scatterer in scatterers:
            builder.render(scatterer, director=self.director)
            continue
        self.dependencies += builder.getDependencies()
        self.filenames += builder.getFilenames()

        # odb file for the sample assembly
        self.options = self._build_odb( )
        return


    def getOptions(self): return self.options
    def getDependencies(self): return self.dependencies
    def getFilenames(self): return self.filenames


    def _build_odb(self):
        contents = [
            'from mcni.pyre_support import componentfactory',
            
            #the next line should be rendered kernel requirements
            'import mccomponents.sample.phonon.xml',
            
            "def sample(): return componentfactory('samples', 'SampleAssemblyFromXml' )('sampleassembly')",
            ]
        
        filename = 'sampleassembly.odb'
        filepath = self._path(filename)
        open( filepath, 'w').write( '\n'.join( contents ) )
        self.filenames.append(filename)
        
        options = {}
        options[ 'sample' ] = 'sampleassembly'
        options[ 'sampleassembly.xml' ] = self.sampleassemblyxmlfilename

        return options


    def _path(self, filename):
        import os
        return os.path.join(self.path, filename)

    
    pass # Builder


# version
__id__ = "$Id$"

# End of file 
