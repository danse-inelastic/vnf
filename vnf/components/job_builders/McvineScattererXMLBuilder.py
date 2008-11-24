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


class Builder(XMLMill):


    def __init__(self, path):
        '''
        path: the run directory where all files about the run should be placed.
        '''
        self.path = path
        XMLMill.__init__(self)
        return
    

    def render(self, scatterer):
        self.dispatch(scatterer)
        contents = self._rep

        name = scatterer.short_description.replace( ' ', '_' )
        import os
        filename = os.path.join( self.path, '%s-scatterer.xml' % name )

        open( filename, 'w').write( '\n'.join( contents ) )
        return
    

    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onConfiguredScatterer(self, configured ):
        prototype = configured.scatterer
        configuration = configured.configuration
        from ScattererConfigurationApplyer import applyer
        applyer( prototype ).apply( configuration )
        return self.dispatch( prototype )


    def onScatterer(self, scatterer):
        matter = scatterer.matter.realmatter
        mattertype = matter.__class__.__name__
        handler = 'on%sScatterer' % mattertype
        return getattr(self, handler)( scatterer )


    def onPolyCrystalScatterer(self, scatterer):
        name = scatterer.short_description.replace( ' ', '_' )

        self._write( '<!DOCTYPE scatterer>' )

        attrs = {
            'mcweights': (0,1,0),
            }
            
        self._write( '<homogeneous_scatterer %s>' % attribs_str( attrs ) )
        self._indent()
        
        for kernel in scatterer.kernels:
            self.dispatch( kernel )
            continue

        self._outdent()
        self._write( '</homogeneous_scatterer>' )
        return


    def onScatteringKernel(self, kernel):
        realscatteringkernel = kernel.realscatteringkernel
        self.dispatch( realscatteringkernel )
        return


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        attrs = {
            #'Ei': kernel.Ei,
            'Ei': '60*meV',
            'max-omega': '%s*meV' % kernel.max_energy_transfer,
            'max-Q': '%s*angstrom**-1' % kernel.max_momentum_transfer,
            'nMCsteps_to_calc_RARV': 10000,
            }

        self._write( '<Phonon_CoherentInelastic_PolyXtal_Kernel %s>' %
                     attribs_str( attrs ) )

        self._indent()
        dispersion = kernel.dispersion
        self.dispatch( dispersion )
        self._outdent()

        self._write( '</Phonon_CoherentInelastic_PolyXtal_Kernel>' )
        return 


    def onPhononDispersion(self, dispersion):
        realphonondispersion = dispersion.realphonondispersion
        self.dispatch( realphonondispersion )
        return
    

    def onIDFPhononDispersion(self, dispersion):
        self._write( '<LinearlyInterpolatedDispersion idf-data-path="%s"/>' % dispersion.id )
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
