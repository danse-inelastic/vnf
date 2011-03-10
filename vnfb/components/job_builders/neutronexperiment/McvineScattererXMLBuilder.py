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
from _ import JobBuilder


class Builder(JobBuilder, XMLMill):


    def __init__(self, path):
        '''
        path: the run directory where all files about the run should be placed.
        '''
        self.path = path
        XMLMill.__init__(self)
        
        self.filenames = []
        self.dependencies = []
        return
    

    def render(self, scatterer, director=None):
        self.db = director.clerk.db
        self.dds = director.dds
        self.director = director
        
        self.dispatch(scatterer)

        del self.db, self.dds
        
        contents = self._rep

        name = scatterer.short_description.replace( ' ', '_' )
        filename = '%s-scatterer.xml' % name 
        import os
        filepath = os.path.join(self.path, filename)
        open( filepath, 'w').write( '\n'.join( contents ) )
        self.filenames.append(filename)
        return


    def getDependencies(self): return self.dependencies
    def getFilenames(self): return self.filenames
    

    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onScatterer(self, scatterer):
        # at this moment we can only deal with polycrystalline sample
        return self.onPolyCrystalScatterer(scatterer)


    def onPolyCrystalScatterer(self, scatterer):
        name = scatterer.short_description.replace( ' ', '_' )

        self._write( '<!DOCTYPE scatterer>' )

        attrs = {
            'mcweights': (0,1,0),
            }
            
        self._write( '<homogeneous_scatterer %s>' % attribs_str( attrs ) )
        self._indent()
        
        for name, kernel in scatterer.kernels.dereference(self.db):
            self.dispatch( kernel )
            continue

        self._outdent()
        self._write( '</homogeneous_scatterer>' )
        return


    def onPowderDiffractionKernel(self, kernel):
        attrs = {
            "Dd_over_d": kernel.dfraction,
            "DebyeWaller_factor": kernel.dwfactor,
            "peaks-py-path": "peaks.py"
            }

        self._write( '<SimplePowderDiffractionKernel %s>' %
                     attribs_str( attrs ) )
        self._write( '</SimplePowderDiffractionKernel>' )        
        return 


    def onIsotropicElasticKernel(self, kernel):
        attrs = {
            }


        self._write( '<IsotropicKernel %s>' %
                     attribs_str( attrs ) )
        self._write( '</IsotropicKernel>' )
        return


    def onSQEKernel(self, kernel):
        attrs = {
            'Q-range': '%s*angstrom**-1,%s*angstrom**-1' % (kernel.Qmin, kernel.Qmax),
            'energy-range': '%s*meV,%s*meV' % (kernel.Emin, kernel.Emax),
            }

        self._write( '<SQEkernel %s>' % attribs_str( attrs ) )

        self._indent()
        sqe = kernel.sqe.dereference(self.db)
        self.dispatch( sqe )
        self._outdent()

        self._write( '</SQEkernel>' )
        return


    def onSQE(self, sqe):
        self.dependencies.append(sqe)

        # this is done by assuming the <table>/<id> directory structure for data storage
        # should be replaced later
        import os
        relpath = os.path.join( '..', '..', self.dds.path(sqe, sqe.histogramh5))
        self._write( '<GridSQE histogram-hdf-path="%s/S(Q,E)"/>' % relpath )
        return


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        attrs = {
            'Ei': '%s*meV' % kernel.Ei,
            'max-omega': '%s*meV' % kernel.max_energy_transfer,
            'max-Q': '%s*angstrom**-1' % kernel.max_momentum_transfer,
            'nMCsteps_to_calc_RARV': 10000,
            }

        self._write( '<Phonon_CoherentInelastic_PolyXtal_Kernel %s>' %
                     attribs_str( attrs ) )

        self._indent()
        phonons = kernel.phonons.dereference(self.db)
        self.dispatch( phonons )
        self._outdent()

        self._write( '</Phonon_CoherentInelastic_PolyXtal_Kernel>' )
        return 


    def onPhonons(self, phonons):
        self.dependencies.append(phonons)
        
        # this is done by assuming the <table>/<id> directory structure for data storage
        # should be replaced later
        import os
        relpath = os.path.join( '..', '..', self.dds.path(phonons), 'data.idf')

        # somewhat hackish
        # have to check the Qgridinfo file to make sure it is right etc
        director = self.director
        domaccess = director.retrieveDOMAccessor('material_simulations/phonons')
        domaccess.standardizeDataInIDFFormat(phonons.id)
        
        self._write( '<LinearlyInterpolatedDispersion idf-data-path="%s"/>' % relpath )
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


    pass # end of Builder


def attribs_str( attributes ):
    return ' '.join(
        ['%s="%s"' % (k, attributes.get(k)) for k in attributes ] )


# version
__id__ = "$Id$"

# End of file 
