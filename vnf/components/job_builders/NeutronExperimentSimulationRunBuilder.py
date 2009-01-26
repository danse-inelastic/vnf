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
debug = journal.debug('jobbuilder')

from JobBuilder import JobBuilder as base

class Builder(base):


    pyscriptname = 'simapp.py'


    def __init__(self, path):
        self.path = path
        return
    

    def render(self, experiment, db=None, dds=None):
        self.computation = self.experiment = experiment
        self.db = db
        self.dds = dds
        
        self.dependencies = []
        self.filenames = []
        self.pyscriptcontents = []
        self.options = {}
        return self.dispatch(experiment)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onNeutronExperiment(self, experiment):
        configured_instrument = experiment.instrument_configuration.dereference(self.db)
        self.dispatch(configured_instrument)

        sampleassembly = experiment.sampleassembly
        if sampleassembly:
            sampleassembly = sampleassembly.dereference(self.db)
        if sampleassembly:
            self.dispatch( sampleassembly )

        samplecomponent = experiment.samplecomponent
        if samplecomponent:
            samplecomponent = samplecomponent.dereference(self.db)
        if samplecomponent:
            self.onSampleComponent(samplecomponent)
        
        parameters = [ 'ncount' ]
        for parameter in parameters:
            self.options[ parameter ] = getattr(experiment, parameter )
            continue

        pyscriptname = self.pyscriptname

        #construct command line
        command = '. ~/.mcvine && python %s %s' % (pyscriptname, ' '.join(
            ['--%s="%s"' % (item, self.options.get(item))
             for item in self.options ] ) )

        #######################
        # this is only for debuggiing purpose:
        # command = 'ls'
        #######################

        shscriptname = self.shscriptname
        files = [ (pyscriptname, self.pyscriptcontents),
                  (shscriptname, [command] ),
                  ]
        self._createfiles(files)
        self.filenames += [pyscriptname, shscriptname]

        # register dependencies
        for dep in self.dependencies: self.registerDependency(dep)
        
        return self.filenames


    def onInstrumentConfiguration(self, configuration):
        from InstrumentSimulationAppBuilder import Builder
        builder = Builder(self.path)
        builder.computation = self.experiment
        pyscriptcontents, options, odbs = builder.render(configuration, db = self.db, dds = self.dds)
        self.pyscriptcontents += pyscriptcontents
        self.options.update(options)
        for odb, content in odbs:
            self._createfile(odb, content)
        self.filenames += [odb for odb, c in odbs]
        return


    def onSampleAssembly(self, sampleassembly):
        from vnf.dom.SampleAssembly import SampleAssembly
        if not isinstance(sampleassembly, SampleAssembly):
            raise RuntimeError
        from McvineSampleAssemblyBuilder import Builder
        builder = Builder(self.path)
        builder.render(sampleassembly, db = self.db, dds = self.dds)
        self.dependencies += builder.getDependencies()
        self.filenames += builder.getFilenames()
        self.options.update(builder.getOptions())
        return


    def onSampleComponent(self, samplecomponent):
        from SampleComponentBuilder import Builder
        builder = Builder(self.path)
        builder.render(samplecomponent, db = self.db, dds = self.dds)
        self.dependencies += builder.getDependencies()
        self.filenames += builder.getFilenames()
        self.options.update(builder.getOptions())
        return


    def _createfiles( self, files):
        for filename, filecontents in files:
            self._createfile(filename, filecontents)
        return


    def _createfile(self, filename, contents):
        filepath = self._path(filename)
        open( filepath, 'w' ).write( '\n'.join( contents ) )
        return

    
    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
