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


from JobBuilder import JobBuilder as base
class Builder(base):


    def __init__(self, path):
        'path: path in which data files are generated'
        base.__init__(self, path)
        return
    

    def render(self, instrument, db=None, dds=None):
        self.db = db
        self.dds = dds
        
        self.appscript = []
        from NeutronExperiment import outputdir
        self.cmdline_opts = {
            'output-dir': outputdir,
            'overwrite-datafiles': True,
            }
        self.odbs = []
        
        self.indent_level = 0
        self.dispatch( instrument )

        self.db = self.dds = None
        return self.appscript, self.cmdline_opts, self.odbs


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
        
        #if 'sample' in sequence:
        #    self.onSample( )
        #    pass # end if

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
            if reference is not None and reference != '' and reference != 'absolute':
                raise NotImplementedError, 'reference=%r' % reference
            
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


    def onSNSModerator(self, component):
        kwds = {
            'name': component.label,
            'category': 'sources',
            'type': 'SNS_source',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent(**kwds)

        opts = {}

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            'width',
            'height',
            'dist',
            'xw',
            'yh',
            'Emin',
            'Emax',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.label,param) ] = getattr(component, param)
            continue

        neutronprofile = component.neutronprofile.dereference(self.db)
        self.registerDependency(neutronprofile)
        
        opts[ '%s.S_filename' % component.label ] = os.path.join(
            '..', '..', self.dds.path(neutronprofile, 'profile.dat'))

        self.cmdline_opts.update( opts )
        return


    def onChanneledGuide(self, component):
        kwds = {
            'name': component.label,
            'category': 'optics',
            'type': 'Guide_channeled',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent(**kwds)

        opts = {}

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            'w1', 'h1',
            'w2', 'h2',
            'l',
            'R0',
            'mx', 'my',
            'Qcx', 'Qcy',
            'alphax', 'alphay',
            'W',
            'k',
            'd',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.label,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onT0Chopper(self, component):
        kwds = {
            'name': component.label,
            'category': 'optics',
            'type': 'Vertical_T0',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent(**kwds)

        opts = {}

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            'w1', 'w2',
            'len',
            'ymin', 'ymax',
            'nu',
            'delta',
            'tc'
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.label,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onFermiChopper(self, component):
        kwds = {
            'name': component.label,
            'category': 'optics',
            'type': 'Fermi_chop2',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent(**kwds)

        opts = {}

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            'w',
            'len',
            'ymin', 'ymax',
            'nu',
            'delta',
            'tc',
            'bw',
            'blader',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.label,param) ] = getattr(component, param)
            continue

        opts[ '%s.nchan' % (component.label,)] = component.nchans
        
        self.cmdline_opts.update( opts )
        return


    def onNeutronRecorder(self, component):
        kwds = {
            'name': component.label,
            'category': 'monitors',
            'type': 'NeutronToStorage',
            'supplier': 'mcni',
            }
        self.onNeutronComponent(**kwds)

        opts = {
            '%s.path' % component.label: outputfilename(component),
            }

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            'packetsize',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.label,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onSampleComponent(self, component):
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

        # need a odb file to enhance the monitor
        odbname = 'enhanced_%s' % m.label
        odbcode = """
def %(name)s():
    from mcni.pyre_support import componentfactory as component
    f = component('monitors', 'IQE_monitor', supplier = 'mcstas2')
    ret =  f('%(odbname)s')
    from mcstas2.pyre_support.monitor_exts import extend
    extend( ret )
    return ret
    """ % {
            'name': m.label,
            'odbname': odbname,
        }
        odbcode = odbcode.split('\n')
        self.odbs.append( ('%s.odb' % odbname, odbcode) )
        
        opts = {
            m.label: odbname,
            '%s.Ei' % odbname: self.Ei,
            '%s.filename' % odbname: outputfilename(m),
            }

        parameters = [
            'Qmin', 'Qmax', 'nQ',
            'Emin', 'Emax', 'nE',
            'max_angle_out_of_plane', 'min_angle_out_of_plane',
            'max_angle_in_plane', 'min_angle_in_plane',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (odbname,param) ] = getattr(m, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onSphericalPSD(self, m):
        kwds = {
            'name': m.label,
            'category': 'monitors',
            'type': 'PSD_monitor_4PI',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        # need a odb file to enhance the monitor
        odbname = 'enhanced_%s' % m.label
        odbcodes = [
            'def %(name)s():',
            '    from mcni.pyre_support import componentfactory as component',
            "    f = component('monitors', 'PSD_monitor_4PI', supplier = 'mcstas2')",
            "    ret =  f('%(odbname)s')",
            "    from mcstas2.pyre_support.monitor_exts import extend",
            "    extend( ret )",
            "    return ret",
            ]
        odbcode = '\n'.join(odbcodes)
        odbcode = odbcode % {
            'name': m.label,
            'odbname': odbname,
            }
        odbcode = odbcode.split('\n')
        self.odbs.append( ('%s.odb' % odbname, odbcode) )
        
        opts = {
            m.label: odbname,
            '%s.filename' % odbname: outputfilename(m),
            }

        parameters = {
            'radius': m.radius,
            'nx': m.ncolumns,
            'ny': m.nrows,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (odbname, k)] = v
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onEMonitor(self, m):
        kwds = {
            'name': m.label,
            'category': 'monitors',
            'type': 'E_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        # need a odb file to enhance the monitor
        odbname = 'enhanced_%s' % m.label
        odbcodes = [
            'def %(name)s():',
            '    from mcni.pyre_support import componentfactory as component',
            "    f = component('monitors', 'E_monitor', supplier = 'mcstas2')",
            "    ret =  f('%(odbname)s')",
            "    from mcstas2.pyre_support.monitor_exts import extend",
            "    extend( ret )",
            "    return ret",
            ]
        odbcode = '\n'.join(odbcodes)
        odbcode = odbcode % {
            'name': m.label,
            'odbname': odbname,
            }
        odbcode = odbcode.split('\n')
        self.odbs.append( ('%s.odb' % odbname, odbcode) )
        
        opts = {
            m.label: odbname,
            }

        parameters = {
            'filename': outputfilename(m),
            'xmin': m.x_min,
            'xmax': m.x_max,
            'ymin': m.y_min,
            'ymax': m.y_max,
            'Emin': m.Emin,
            'Emax': m.Emax,
            'nchan': m.nchan,
            'xwidth': 0,
            'yheight': 0,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (odbname, k)] = v
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

        # need a odb file to enhance the monitor
        odbname = 'enhanced_%s' % m.label
        odbcode = """
def %(name)s():
    from mcni.pyre_support import componentfactory as component
    f = component('monitors', 'TOF_monitor2', supplier = 'mcstas2')
    ret =  f('%(odbname)s')
    from mcstas2.pyre_support.monitor_exts import extend
    extend( ret )
    return ret
    """ % {
            'name': m.label,
            'odbname': odbname,
        }
        odbcode = odbcode.split('\n')
        self.odbs.append( ('%s.odb' % odbname, odbcode) )
        
        opts = {
            m.label: odbname,
            '%s.filename' % odbname: outputfilename(m),
            }

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
            opts[ '%s.%s' %  (odbname,mcparam) ] = getattr(m, recordparam)
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
            '%s.eventsdat' % ds.label: outputfilename(ds),
            '%s.instrumentxml' % ds.label: self.detectorsystem_xmlfile,
            '%s.tofparams' % ds.label: tofparams,
            }

        self.cmdline_opts.update( opts )
        return
    detectorsystem_xmlfile = 'detectorsystem.xml'
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

#!!! need a more structured way to handle this !!!
from NeutronExperiment import outputfilename
class _ComponentOutputfiles:
    '''Each component generates some output files. This class
    figures out what those output files are. This actually depends
    on which mcvine components are used.
    
    Developer: Keep this class in sync with the main class here: Builder
    '''

    def __init__(self, root):
        self.root = root
        return

    def dispatch(self, component):
        f = outputfilename(component)
        
        klass = component.__class__.__name__
        if klass in [
            'EMonitor',
            'QEMonitor',
            'TofMonitor',
            'SphericalPSD',
            ]:
            f1, ext = os.path.splitext(f)
            f = '.'.join( [f1, 'h5'] )
        
        return [os.path.join(self.root, f)]


# version
__id__ = "$Id$"

# End of file 
