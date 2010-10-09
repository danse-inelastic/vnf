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


from _ import JobBuilder as base
class Builder(base):


    def __init__(self, path):
        'path: path in which data files are generated'
        base.__init__(self, 'instrumentsimulationappbuilder', path)
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
        components = [c for n, c in components]
        
        self._write( 'import mcvine' )
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

        sequence = []
        for component in components:
            self.dispatch( component )
            name = component.componentname
            # for sample, the name is alwasy "sample"
            if component.__class__.__name__ == 'SampleComponent':
                name = 'sample'
            sequence.append(name)
            continue

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

        # calculate absolute coordinates of scatterers
        from vnfb.utils.neutron_experiment_simulations.geometry \
            import calculateComponentAbsoluteCoordinates
        calculateComponentAbsoluteCoordinates(components)

        for component in components:
            reference = component.referencename
            if reference is not None and reference != '' and reference != 'absolute':
                raise NotImplementedError, 'reference=%r' % reference
            
            position = component.position
            orientation = component.orientation

            value = '%s,%s' % (list(position), _formatOrientation(orientation))

            name = component.componentname
            # for sample, the name is alwasy "sample"
            if component.__class__.__name__ == 'SampleComponent':
                name = 'sample'
            self.cmdline_opts[ 'geometer.%s' % name ] = value

            continue

        self._outdent()
        self._write('')

        self._write( 'if __name__ == "__main__":' )
        self._indent()
        self._write( 'app = Instrument( "Instr%s" )' % configuration.id )
        self._write( 'app.run()' )
        self._outdent()
        self._write( '' )
        return


    def onMonochromaticSource(self, source):
        kwds = {
            'name': source.componentname,
            'category': 'sources',
            'type': 'MonochromaticSource',
            'supplier': 'mcni',
            }
        self.onNeutronComponent( **kwds )

        from _utils import e2v
        v = e2v( source.energy )
        self.Ei = source.energy
        self.cmdline_opts[ '%s.velocity' % source.componentname ] = (0,0,v) 
        return


    def onSNSModerator(self, component):
        kwds = {
            'name': component.componentname,
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
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
            continue

        neutronprofile = component.neutronprofile.dereference(self.db)
        self.registerDependency(neutronprofile)
        
        opts[ '%s.S_filename' % component.componentname ] = os.path.join(
            '..', '..', self.dds.path(neutronprofile, 'profile.dat'))

        self.cmdline_opts.update( opts )
        return


    def onChanneledGuide(self, component):
        kwds = {
            'name': component.componentname,
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
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onT0Chopper(self, component):
        kwds = {
            'name': component.componentname,
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
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onFermiChopper(self, component):
        kwds = {
            'name': component.componentname,
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
            'nchan',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
            continue

        self.cmdline_opts.update( opts )
        return


    def onNeutronRecorder(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'NeutronToStorage',
            'supplier': 'mcni',
            }
        self.onNeutronComponent(**kwds)

        opts = {
            '%s.path' % component.componentname: outputfilename(component),
            }

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onNeutronPlayer(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'sources',
            'type': 'NeutronFromStorage',
            'supplier': 'mcni',
            }
        self.onNeutronComponent(**kwds)

        # neutronstorage db record
        storage = component.neutrons.dereference(self.db)
        self.registerDependency(storage)
        neutrondatapath = os.path.join('..', '..', self.dds.path(storage, 'data.idf'))
        
        opts = {
            '%s.path' % component.componentname: neutrondatapath,
            }

        # map database record parameter names to parameters used in monte carlo components
        parameters = [
            ]

        for param in parameters:
            opts[ '%s.%s' %  (component.componentname,param) ] = getattr(component, param)
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
            'name': m.componentname,
            'category': 'monitors',
            'type': 'IQE_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        if hasattr(self, 'Ei'):
            Ei = self.Ei
        else:
            Ei = m.Ei
        opts = {
            '%s.Ei' % m.componentname: Ei,
            '%s.filename' % m.componentname: outputfilename(m),
            }

        parameters = [
            'Qmin', 'Qmax', 'nQ',
            'Emin', 'Emax', 'nE',
            'max_angle_out_of_plane', 'min_angle_out_of_plane',
            'max_angle_in_plane', 'min_angle_in_plane',
            ]

        for param in parameters:
            opts[ '%s.%s' %  (m.componentname,param) ] = getattr(m, param)
            continue
        
        self.cmdline_opts.update( opts )
        return




    def onSphericalPSD(self, m):
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'PSD_monitor_4PI',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            '%s.filename' % m.componentname: outputfilename(m),
            }

        parameters = {
            'radius': m.radius,
            'nx': m.ncolumns,
            'ny': m.nrows,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onEMonitor(self, m):
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'E_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
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
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue
        
        self.cmdline_opts.update( opts )
        return


    def onLMonitor(self, m):
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'L_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }

        parameters = {
            'filename': outputfilename(m),
            'xmin': m.x_min,
            'xmax': m.x_max,
            'ymin': m.y_min,
            'ymax': m.y_max,
            'xwidth': m.x_width,
            'yheight': m.y_height,
            'Lmin': m.Lmin,
            'Lmax': m.Lmax,
            'nchan': m.nchan,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
        return


    def onMonitor(self, m):
        # Monitor
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'Monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }

        parameters = {
            'xmin': m.x_min,
            'xmax': m.x_max,
            'ymin': m.y_min,
            'ymax': m.y_max,
            'xwidth': m.xwidth,
            'yheight': m.yheight,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
        return


    def onNDMonitor(self, m):
        # NDMonitor
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'Monitor_nD',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }

        parameters = {
            'filename': outputfilename(m),
            'xmin': m.x_min,
            'xmax': m.x_max,
            'ymin': m.y_min,
            'ymax': m.y_max,
            'xwidth': m.xwidth,
            'yheight': m.yheight,
            'options': m.options,
            'user1': m.user1,
            'user2': m.user2,
            'username1': m.username1,
            'username2': m.username2,
            'zthick': m.zthick,
            'zmin': m.zmin,
            'zmax': m.zmax,
            'bins': m.bins,
            'min': m.min,
            'max': m.max,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
        return


    def onPSDMonitor(self, m):
        # PSDMonitor
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'PSD_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }

        parameters = {
            'filename': outputfilename(m),
            'xmin': m.x_min,
            'xmax': m.x_max,
            'ymin': m.y_min,
            'ymax': m.y_max,
            'xwidth': m.xwidth,
            'yheight': m.yheight,
            'nx': m.nx,
            'ny': m.ny,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
        return


    def onPSD_TEWMonitor(self, m):
        # PSD_TEWMonitor
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'PSD_TEW_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }

        parameters = {
            'filename': outputfilename(m),
            'xwidth': m.xwidth,
            'yheight': m.yheight,
            'nxchan': m.nxchan,
            'nychan': m.nychan,
            'nbchan': m.nbchan,
            'type': m.type,
            'format': m.format,
            'bmin': m.bmin,
            'bmax': m.bmax,
            'deltab': m.deltab,
            'restore_neutron': m.restore_neutron,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
        return


    def onTofMonitor(self, m):
        kwds = {
            'name': m.componentname,
            'category': 'monitors',
            'type': 'TOF_monitor2',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            '%s.filename' % m.componentname: outputfilename(m),
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
            opts[ '%s.%s' %  (m.componentname,mcparam) ] = getattr(m, recordparam)
            continue
        
        self.cmdline_opts.update( opts )
        return


    ### need further work here ###
    def onDetectorSystem_fromXML(self, ds):
        # first we need to get the detector system xml file
        hierarchy = ds.hierarchy.dereference(self.db)
        xmlfilepath = self.dds.path(hierarchy, hierarchy.xmlfilename)
        # suppose that .. works
        import os
        xmlfilepath = os.path.join('..', '..', xmlfilepath)

        # declare the hierarchy a dependency
        self.registerDependency(hierarchy)
        
        # then we need to build the options ( odb?)
        kwds = {
            'name': ds.componentname,
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
            '%s.eventsdat' % ds.componentname: outputfilename(ds),
            '%s.instrumentxml' % ds.componentname: xmlfilepath,
            '%s.tofparams' % ds.componentname: tofparams,
            }
        
        self.cmdline_opts.update( opts )
        return
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


    def _datadir(self, obj):
        dds = self.dds
        return dds.abspath(obj)


    pass # end of Builder



def _formatOrientation(matrix):
    from mcni.neutron_coordinates_transformers.mcstasRotations import toAngles
    return list(toAngles(matrix))



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
            'LMonitor',
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
