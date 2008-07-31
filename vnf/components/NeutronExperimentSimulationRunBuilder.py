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


class Builder:


    pyscriptname = 'simapp.py'
    shscriptname = 'run.sh'


    def __init__(self, path):
        self.path = path
        return
    

    def render(self, experiment):
        return self.dispatch(experiment)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onNeutronExperiment(self, experiment):
        configured_instrument = experiment.instrument
        pyscriptconents, options = self.dispatch( configured_instrument )

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
        files = [ (pyscriptname, pyscriptconents),
                  (shscriptname, [command] ),
                  ]
        self._createfiles( files )
        return


    def onConfiguredInstrument(self, instrument):
        from InstrumentSimulationAppBuilder import Builder
        return Builder( self.path ).render( instrument )


    def onSampleAssembly(self, sampleassembly):
        if sampleassembly.__class__.__name__ == 'SampleAssembly':
            from McvineSampleAssemblyBuilder import Builder
        else:
            from McstasSampleBuilder import Builder
            pass
        return Builder(self.path).render( sampleassembly )


    def _createfiles( self, files):
        path = self.path

        import os
        for filename, filecontents in files:
            filepath = os.path.join( path, filename )
            open( filepath, 'w' ).write( '\n'.join( filecontents ) )
            continue
        return

    
    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
