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

'''Builder to render mcvine code from configurations of a "samplecomponent".
A sample component is an instance of one of the subclasses of
dom.neutron_experiment_simulations.neutron_components.SampleBase, and
not of either SampleAssembly or Scatterer.
'''

class Builder:

    def __init__(self, path):
        self.path = path
        return
    

    def getOptions(self): return self.options
    def getDependencies(self): return self.dependencies
    def getFilenames(self): return self.filenames


    def render(self, sample, db=None, dds=None):
        self.db = db; self.dds = dds
        self.dependencies = []
        self.filenames = []
        self.options = {}
        return self.dispatch(sample)


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onVanadiumPlate(self, sample):
        # odb
        content = [
            'from mcni.pyre_support import componentfactory',
            "def sample():",
            "    f = componentfactory('samples', 'V_sample', supplier='mcstas2')",
            "    return f('vanadium-plate')",
            ]

        filename = 'vanadium-plate.odb'
        filepath = self._path(filename)
        open(filepath, 'w').write('\n'.join(content))
        self.filenames.append(filename)

        # cmdline options
        # 1. set the sample component
        comp = 'vanadium-plate'
        self.options['sample'] = comp
        # 2. set options for the component
        compparams = {
            'radius_i': 0,
            'radius_o': 0,
            'h': 0,
            'focus_r': sample.target_radius,
            'target_x': sample.target_position[0],
            'target_y': sample.target_position[1],
            'target_z': sample.target_position[2],
            'xwidth': sample.width,
            'yheight': sample.height,
            'zthick': sample.thickness,
            }
        for k, v in compparams.iteritems():
            self.options['%s.%s' % (comp, k)] = v
            continue
        return


    def _path(self, filename):
        import os
        return os.path.join(self.path, filename)
    
    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
