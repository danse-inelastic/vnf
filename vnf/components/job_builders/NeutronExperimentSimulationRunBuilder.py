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
        self.db = db
        self.dds = dds
        return self.dispatch(experiment)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onNeutronExperiment(self, experiment):
        configured_instrument = experiment.instrument_configuration.dereference(self.db)
        pyscriptcontents, options, odbs = self.dispatch(configured_instrument)

        sampleassembly = experiment.sampleassembly
        if sampleassembly:
            options1 = self.dispatch( sampleassembly )
            options.update( options1 )
            pass
        
        parameters = [ 'ncount' ]
        for parameter in parameters:
            options[ parameter ] = getattr(experiment, parameter )
            continue

        pyscriptname = self.pyscriptname
        command = '. ~/.mcvine && python %s %s' % (pyscriptname, ' '.join(
            ['--%s="%s"' % (item, options.get(item))
             for item in options ] ) )

        #######################
        # this is only for debuggiing purpose:
        # command = 'ls'
        #######################

        shscriptname = self.shscriptname
        files = [ (pyscriptname, pyscriptcontents),
                  (shscriptname, [command] ),
                  ]
        files += odbs
        self._createdatadir()
        self._createfiles(files)
        return [f for f,c in files]


    def onInstrumentConfiguration(self, configuration):
        from InstrumentSimulationAppBuilder import Builder
        return Builder(self.path).render(configuration, db = self.db, dds = self.dds)


    def onSampleAssembly(self, sampleassembly):
        if sampleassembly.__class__.__name__ == 'SampleAssembly':
            from McvineSampleAssemblyBuilder import Builder
        else:
            from McstasSampleBuilder import Builder
            pass
        return Builder(self.path).render(sampleassembly, db = self.db, dds = self.dds)


    def _createdatadir(self):
        import os
        try:
            os.makedirs(self.path)
        except OSError, msg:
            debug.log('failed to make path %r: %s' % (self.path, msg))
        return


    def _createfiles( self, files):
        path = self.path

        import os
        for filename, filecontents in files:
            filepath = self._path(filename)
            open( filepath, 'w' ).write( '\n'.join( filecontents ) )
            continue
        return

    
    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
