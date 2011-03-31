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
        # XXX: hack: need this line to support diffraction kernels
        self._write( 'import mccomponents.sample.diffraction.xml')
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
        from vnf.utils.neutron_experiment_simulations.geometry \
            import calculateComponentAbsoluteCoordinates
        calculateComponentAbsoluteCoordinates(components)

        for component in components:
            reference = component.referencename
                        
            position    = component.position
            orientation = component.orientation

            if reference is not None and reference != '' and reference != 'absolute':
                # Relative vectors
                value = 'relative(%s, to="%s"),relative(%s, to="%s")' % (
                                                    list(position),
                                                    reference,
                                                    _formatOrientation(orientation),
                                                    reference)
            else:
                # Absolute vectors
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


    def onSimpleSource(self, s):
        kwds = {
            'name': s.componentname,
            'category': 'sources',
            'type': 'Source_simple',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {
            }


        parameters = {
            'radius':   s.radius,
            'height':   s.height,
            'width':   s.width,
            'dist':   s.dist,
            'xw':   s.xw,
            'yh':   s.yh,
            'E0':   s.E0,
            'dE':   s.dE,
            'Lambda0':   s.Lambda0,
            'dLambda':   s.dLambda,
            'flux':   s.flux,
            'gauss':   s.gauss,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (s.componentname, k)] = v
            continue

        self.cmdline_opts.update( opts )
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


    def onArm(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'Arm',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )


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


    # XXX: No implementation in McVine at this moment!
#    def onQMonitor(self, m):
#        kwds = {
#            'name': m.componentname,
#            'category': 'monitors',
#            'type': 'QMonitor',
#            'supplier': 'mcni', # ?
#            }
#        self.onNeutronComponent( **kwds )
#
#        opts = {
#            }
#
#        parameters = {
#            'filename': outputfilename(m),
#            'Qmin': m.Qmin,
#            'Qmax': m.Qmax,
#            'nQ':   m.nQ
#            }
#        for k,v in parameters.iteritems():
#            opts['%s.%s' % (m.componentname, k)] = v
#            continue
#
#        self.cmdline_opts.update( opts )
#        return


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


    def onDiskChopper(self, m):
        kwds = {
            'name': m.componentname,
            'category': 'optics',
            'type': 'DiskChopper',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'theta_0': m.theta_0,
            'R': m.R,
            'h': m.h,
            'omega': m.omega,
            'n': m.n,
            'j': m.j,
            'theta_1': m.theta_1,
            't_0': m.t_0,
            'IsFirst': m.IsFirst,
            'n_pulse': m.n_pulse,
            'abs_out': m.abs_out,
            'phi_0': m.phi_0,
            'w': m.w,
            'wc': m.wc,
            'compat': m.compat,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (m.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onCollimatorLinear(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'Collimator_linear',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'len': component.len,
            'divergence': component.divergence,
            'transmission': component.transmission,
            'divergenceV': component.divergenceV,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onSlit(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'Slit',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'radius': component.radius,
            'cut': component.cut,
            'width': component.width,
            'height': component.height,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onLMonitor(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'L_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'xwidth': component.x_width,
            'yheight': component.y_height,
            'Lmin': component.Lmin,
            'Lmax': component.Lmax,
            'nchan': component.nchan,
            'filename': outputfilename(component),
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onGuide(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'Guide',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'w1': component.w1,
            'h1': component.h1,
            'w2': component.w2,
            'h2': component.h2,
            'l': component.l,
            'R0': component.R0,
            'Qc': component.Qc,
            'alpha': component.alpha,
            'm': component.m,
            'W': component.W,
            'reflect': component.reflect,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onDiskChopper(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'DiskChopper',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'theta_0': component.theta_0,
            'R': component.R,
            'h': component.h,
            'omega': component.omega,
            'n': component.n,
            'j': component.j,
            'theta_1': component.theta_1,
            't_0': component.t_0,
            'IsFirst': component.IsFirst,
            'n_pulse': component.n_pulse,
            'abs_out': component.abs_out,
            'phi_0': component.phi_0,
            'w': component.w,
            'wc': component.wc,
            'compat': component.compat,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onGuideGravity(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'optics',
            'type': 'Guide_gravity',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'reflect': component.reflect,
            'w1': component.w1,
            'h1': component.h1,
            'w2': component.w2,
            'h2': component.h2,
            'l': component.l,
            'R0': component.R0,
            'Qc': component.Qc,
            'alpha': component.alpha,
            'm': component.m,
            'W': component.W,
            'k': component.k,
            'd': component.d,
            'mleft': component.mleft,
            'mright': component.mright,
            'mtop': component.mtop,
            'mbottom': component.mbottom,
            'kh': component.kh,
            'G': component.G,
            'wavy': component.wavy,
            'wavy_z': component.wavy_z,
            'wavy_tb': component.wavy_tb,
            'wavy_lr': component.wavy_lr,
            'chamfers': component.chamfers,
            'chamfers_z': component.chamfers_z,
            'chamfers_lr': component.chamfers_lr,
            'chamfers_tb': component.chamfers_tb,
            'nelements': component.nelements,
            'nu': component.nu,
            'phase': component.phase,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onPSDMonitor(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'PSD_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'xwidth': component.x_width,
            'yheight': component.y_height,
            'nx': component.nx,
            'ny': component.ny,
            'filename': outputfilename(component),
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onNDMonitor(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'Monitor_nD',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xwidth': component.x_width,
            'yheight': component.y_height,
            'zthick': component.zthick,
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'zmin': component.zmin,
            'zmax': component.zmax,
            'bins': component.bins,
            'min': component.min,
            'max': component.max,
            'options': component.options,
            'filename': outputfilename(component),
            'user1': component.user1,
            'user2': component.user2,
            'username1': component.username1,
            'username2': component.username2,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onVulcanDetectorSystem(self, detectorsystem):
        "Composition of 6 NDMonitor"
        compname = detectorsystem.componentname
        
        # create odb file
        content = """
def neutroncomponent():
    from mcvine.instruments.VULCAN.DetectorSystem import DetectorSystem
    return DetectorSystem('%s')
        """ % compname
        content = content.splitlines()

        filename = '%s.odb' % compname
        self.odbs.append((filename, content))
        
        # 
        kwds = {
            'name':     compname,
            }
        # XXX: name has to be a valid varaible name
        self._write( 
            '%(name)s = facility(%(name)r, default = %(name)r)' % kwds )

        opts = {}

        parameters = {
            'xwidth':   detectorsystem.xwidth,
            'yheight':  detectorsystem.yheight,
            'tmin':     detectorsystem.tmin,
            'tmax':     detectorsystem.tmax,
            'nt':       detectorsystem.nt,
            'wmin':     detectorsystem.wmin,
            'wmax':     detectorsystem.wmax,
            'nw':       detectorsystem.nw
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (detectorsystem.componentname, k)] = v

        self.cmdline_opts.update( opts )
        


    def onVanadiumPlate(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'samples',
            'type': 'V_sample',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'radius_i': component.radius_i,
            'radius_o': component.radius_o,
            'h': component.h,
            'focus_r': component.focus_r,
            'pack': component.pack,
            'frac': component.frac,
            'f_QE': component.f_QE,
            'gamma': component.gamma,
            'target_x': component.target_x,
            'target_y': component.target_y,
            'target_z': component.target_z,
            'focus_xw': component.focus_xw,
            'focus_yh': component.focus_yh,
            'focus_aw': component.focus_aw,
            'focus_ah': component.focus_ah,
            'xwidth': component.x_width,
            'yheight': component.y_height,
            'zthick': component.zthick,
            'sig_a': component.sig_a,
            'sig_i': component.sig_i,
            'V0': component.V0,
            'target_index': component.target_index,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onPSD_TEWMonitor(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'PSD_TEW_monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xwidth': component.x_width,
            'yheight': component.y_height,
            'bmin': component.bmin,
            'bmax': component.bmax,
            'deltab': component.deltab,
            'restore_neutron': component.restore_neutron,
            'nxchan': component.nxchan,
            'nychan': component.nychan,
            'nbchan': component.nbchan,
            'type': component.type,
            'filename': outputfilename(component),
            'format': component.format,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


    def onMonitor(self, component):
        kwds = {
            'name': component.componentname,
            'category': 'monitors',
            'type': 'Monitor',
            'supplier': 'mcstas2',
            }
        self.onNeutronComponent( **kwds )

        opts = {}

        parameters = {
            'xmin': component.x_min,
            'xmax': component.x_max,
            'ymin': component.y_min,
            'ymax': component.y_max,
            'xwidth': component.x_width,
            'yheight': component.y_height,
            }
        for k,v in parameters.iteritems():
            opts['%s.%s' % (component.componentname, k)] = v

        self.cmdline_opts.update( opts )


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
            'PSDMonitor',
            ]:
            f1, ext = os.path.splitext(f)
            f = '.'.join( [f1, 'h5'] )
        elif (klass == "VulcanDetectorSystem"):
            fs      = ['m%s.h5'% i for i in range(1,7)]
            return [os.path.join(self.root, f) for f in fs]
        
        return [os.path.join(self.root, f)]


# version
__id__ = "$Id$"

# End of file 
