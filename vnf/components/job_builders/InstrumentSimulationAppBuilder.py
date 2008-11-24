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


    def __init__(self, path):
        'path: path in which data files are generated'
        self.path = path
        return
    

    def render(self, instrument, db=None, dds=None):
        self.db = db
        self.dds = dds
        
        self.appscript = []
        self.cmdline_opts = {}
        self.indent_level = 0
        self.dispatch( instrument )

        self.db = self.dds = None
        return self.appscript, self.cmdline_opts


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onInstrumentConfiguration(self, configuration):
        
        components = configuration.components.dereference(self.db)
        instrument = configuration.target.dereference(self.db)
        
        self._write( 'import mccomponents.pyre_support' )
        self._write( 'from mcni.pyre_support.Instrument import Instrument as base' )
        self._write( 'class Instrument(base):' )

        self._indent()
        self._write(
            'class Inventory(base.Inventory):'
            )

        self._indent()
        self._write( 'import pyre.inventory' )
        self._write( 'from mcni.pyre_support import facility, componentfactory as component')
        
        for name, component in components:
            component.label = name
            self.dispatch( component )
            continue

        sequence = instrument.componentsequence
        
        if 'sample' in sequence:
            self.onSample( )
            pass # end if

        self._outdent()

        #need to get geometer right
        self._write('def _defaults(self):')
        self._indent()
        self._write('base._defaults(self)')
        self._write('geometer = self.inventory.geometer')
        self._outdent()

        self.cmdline_opts[ 'sequence' ] = sequence

        geometer = instrument.geometer.dereference(self.db)
        for component in sequence:
            
            record = geometer[ component ]
            
            reference = record.reference_label
            if reference is not None and reference != '':
                raise NotImplementedError
            
            position = record.position
            orientation = record.orientation

            value = '%s,%s' % (position, orientation)
            
            self.cmdline_opts[ 'geometer.%s' % component ] = value

            continue

        self._outdent()
        self._write('')

        self._write( 'if __name__ == "__main__":' )
        self._indent()
        self._write( 'app = Instrument( "Instr%s" )' % instrument.id )
        self._write( 'app.run()' )
        self._outdent()
        self._write( '' )
        return


    def onMonochromaticSource(self, source):
        kwds = {
            'name': source.label,
            'category': 'sources',
            'type': 'MonochromaticSource',
            'supplier': 'mcni',
            }
        self.onNeutronComponent( **kwds )

        from _utils import e2v
        v = e2v( source.energy )
        self.Ei = source.energy
        self.cmdline_opts[ '%s.velocity' % source.label ] = (0,0,v) 
        return


    def onSample(self):
        self._write(
            "sample = facility( 'sample', default = 'sample' )"
            )
        return


    def onQEMonitor(self, m):
        kwds = {
            'name': m.label,
            'category': 'monitors',
            'type': 'IQE_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            '%s.Ei' % m.label: self.Ei,
            }

        parameters = [
            'Qmin', 'Qmax', 'nQ',
            'Emin', 'Emax', 'nE',
            'max_angle_out_of_plane', 'min_angle_out_of_plane',
            'max_angle_in_plane', 'min_angle_in_plane',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (m.label,param) ] = getattr(m, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onTofMonitor(self, m):
        kwds = {
            'name': m.label,
            'category': 'monitors',
            'type': 'TOF_monitor2',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            ('tmin', 'tmin'),
            ('tmax', 'tmax'),
            ('nchan', 'nchan'),
            ('x_min', 'xmin'),
            ('x_max', 'xmax'),
            ('y_min', 'ymin'),
            ('y_max', 'ymax'),
            ]

        for recordparam, mcparam in parameters:
            opts[ '%s.%s' %  (m.label,mcparam) ] = getattr(m, recordparam)
            continue
        
        self.cmdline_opts.update( opts )
        return


    ### need further work here ###
    def onDetectorSystem_fromXML(self, ds):
        # first we need to get the detector system xml file
        xmlfile_source = os.path.join(
            self._datadir( ds ), self.detectorsystem_xmlfile)
        xmlfile_target = os.path.join( self.path, self.detectorsystem_xmlfile)
        self._link( xmlfile_source, xmlfile_target )

        # then we need to build the options ( odb?)
        kwds = {
            'name': ds.label,
            'category': 'detectors',
            'type': 'DetectorSystemFromXml',
            'supplier': 'mcni',
            }
        self.onNeutronComponent( **kwds )

        #we should use unit to make this automatic
        tofmin = ds.tofmin / 1e6
        tofmax = ds.tofmax / 1e6
        ntofbins = ds.ntofbins
        
        tofparams = '%s,%s,%s' % (
            tofmin, tofmax, (tofmax-tofmin)*1./ntofbins )
        opts = {
            '%s.eventsdat' % ds.label: self.detectorsystem_output_eventfile,
            '%s.instrumentxml' % ds.label: self.detectorsystem_xmlfile,
            '%s.tofparams' % ds.label: tofparams,
            }

        self.cmdline_opts.update( opts )
        return
    detectorsystem_xmlfile = 'detectorsystem.xml'
    detectorsystem_output_eventfile = 'detectorsystem-events.dat'
    ### need further work here ###
    

    def onNeutronComponent(self, **kwds):
        '''
        kwds: name, category, type, supplier
        '''
        self._write( 
            '%(name)s = facility(%(name)r, default = component(%(category)r, %(type)r, supplier = %(supplier)r )(%(name)r ) )' % kwds )
        return
                                    
            
    def _indent(self): self.indent_level += 1
    def _outdent(self): self.indent_level -= 1

    def _write(self, s):
        self.appscript.append( '%s%s' % (self.indent_level * '  ', s) )
        return


    ### need further work here ###
    def _link(self, linked, link):
        cmd = 'ln -s %s %s' % (linked, link )
        from spawn import spawn
        spawn( cmd )
        return
    ### need further work here ###


    def _datadir(self, obj):
        dds = self.dds
        return dds.abspath(obj)


    pass # end of Builder


import os

# version
__id__ = "$Id$"

# End of file 
