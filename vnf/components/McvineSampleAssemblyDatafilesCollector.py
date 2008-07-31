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


class Collector:


    def __init__(self, path):
        '''
        path: the run directory where all files about the run should be placed.
        '''
        self.path = path
        return
    

    def render(self, sampleassembly):
        self.dispatch(sampleassembly)
        return
    

    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onSampleAssembly(self, sampleassembly):
        for scatterer in sampleassembly.scatterers:
            self.dispatch( scatterer )
            continue
        return 


    def onConfiguredScatterer(self, configured ):
        prototype = configured.scatterer
        configuration = configured.configuration
        from ScattererConfigurationApplyer import applyer
        applyer( prototype ).apply( configuration )
        return self.dispatch( prototype )


    def onScatterer(self, scatterer):
        matter = scatterer.matter.realmatter
        self.dispatch( matter )
        shape = scatterer.shape
        self.dispatch( shape )
        for kernel in scatterer.kernels:
            self.dispatch( kernel )
            continue
        return


    def onShape(self, shape):
        realshape = shape.realshape
        #self.dispatch( realshape )
        return


    def onPolyCrystal(self, polycrystal):
        self._create_xyzfile( polycrystal )
        return


    def onScatteringKernel(self, kernel):
        realscatteringkernel = kernel.realscatteringkernel
        self.dispatch( realscatteringkernel )
        return


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        dispersion = kernel.dispersion
        self.dispatch( dispersion )
        return 


    def onPhononDispersion(self, dispersion):
        realphonondispersion = dispersion.realphonondispersion
        self.dispatch( realphonondispersion )
        return
    

    def onIDFPhononDispersion(self, dispersion):
        idfdispersion_dir = self._datadir( dispersion )
        #make a symbolic link in the run directory to the dispersion
        link = os.path.join( self.path, dispersion.id )
        self._link( idfdispersion_dir, link )
        return
    

    def _link(self, linked, link):
        cmd = 'ln -s %s %s' % (linked, link )
        from spawn import spawn
        spawn( cmd )
        return


    def _datadir(self, obj):
        from misc import datadir
        datadir = os.path.abspath( datadir() )
        path = os.path.join(
            datadir,
            obj.__class__.__name__.lower(),
            obj.id,
            )
        return path


    def _create_xyzfile(self, crystal):
        import os
        filename = '%s.xyz' % crystal.id
        filepath = os.path.join( self.path, filename )

        contents = crystal2xyz( crystal )

        open( filepath, 'w' ).write( '\n'.join( contents ) )
        return filename


    pass # end of Builder


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
            '%s %s' % (atom, ' '.join( [ '%s' % x for x in coords] ) )
            )
        continue
    
    return contents


import os


# version
__id__ = "$Id$"

# End of file 
