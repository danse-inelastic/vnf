# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component

class Clerk(Component):


    def __init__(self, *args, **kwds):
        Component.__init__(self, *args, **kwds)
        self.getHierarchy = HierarchyRetriever(self)
        return


    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
        from vnf.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user
            continue
        return index

    def indexActiveUsers(self):
        """create an index of all active users"""
        return self.indexUsers()
        return self.indexUsers(where="status='a'")

    def indexJobs(self, where = None):
        '''create and index all jobs'''
        from vnf.dom.Job import Job
        return self._index( Job, where )

    def indexInstruments(self, where = None):
        """create an index of all instruments
        that meet the specified criteria"""
        from vnf.dom.Instrument import Instrument
        return self._index( Instrument, where )

    def indexSampleAssemblies(self, where = None):
        """create an index of all sample assemblies
        that meet the specified criteria"""
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._index( SampleAssembly, where )

    def indexScatterers(self, where = None):
        '''create and index of all scatterers
        that meet the specified criteria'''
        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )

    def indexScatteringKernels(self, where = None):
        '''create and index of all scatterers
        that meet the specified criteria'''
        from vnf.dom.ScatteringKernel import ScatteringKernel
        return self._index( ScatteringKernel, where )

    def indexServers(self, where = None):
        '''create and index of all servers
        that meet the specified criteria'''

        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )


    def indexNeutronExperiments(self, where = None):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._index( NeutronExperiment, where )


    def updateRecord(self, record):
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        for column in record.getColumnNames():
            value = getattr( record, column )
            #value = _tostr( value )
            assignments.append( (column, value) )
            continue
        
        self.db.updateRow(record, assignments, where)
        return record


    def getRecordByID(self, tablename, id):
        exec 'from vnf.dom.%s import %s as Table' % (tablename, tablename) \
             in locals()
        return self._getRecordByID( Table, id )


    def findParentSampleAssembly(self, scatterer_id ):
        from vnf.dom.SampleAssembly import SampleAssembly
        table = SampleAssembly.Scatterers
        all = self.db.fetchall( table, where = "remotekey='%s'" % scatterer_id )
        if len(all) != 1:
            raise RuntimeError, "Every scatterer should have only one parent sample assembly"
        record = all[0]
        id = record.localkey
        return self.getSampleAssembly( id )
        

    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )

    
    def getMatter(self, id):
        '''retrieve matter of given id'''
        from vnf.dom.Matter import Matter
        return self._getRecordByID( Matter, id )

    
    def getJob(self, id):
        '''retrieve job of given id'''
        from vnf.dom.Job import Job
        return self._getRecordByID( Job, id )
    
    
    def getJobs(self, where = None):
        '''retrieve all jobs'''
        from vnf.dom.Job import Job
        return self._getAll( Job, where )
    
    
    def getRealMatter(self, id):
        '''given id in the matter table, retrieve the real
        matter's record.
        The matter table contains type and reference_id
        info of the matter.
        To look up the real matter, we have to
        go to the table of the given matter type
        and find the record of given id.
        '''
        from vnf.dom.Matter import Matter
        return self._getRealObject( id, Matter )


    def getRealScatterer(self, id):
        '''given id in the scatter table, retrieve the real
        scatterer's record.
        The scatter table contains type and reference_id
        info of the scatterer.
        To look up the real scatterer, we have to
        go to the table of the given scatterer type
        and find the record of given id.
        '''
        from vnf.dom.Scatterer import Scatterer
        return self._getRealObject( id, Scatterer )


    def getRealComponent(self, id):
        '''given id in the component table, retrieve the real
        component's record.
        The component table contains type and reference_id
        info of the component.
        To look up the real component, we have to
        go to the table of the given component type
        and find the record of given id.
        '''
        from vnf.dom.Component import Component
        return self._getRealObject( id, Component )


    def getSample(self, id):
        '''retrieve sample of given id'''
        from vnf.dom.Sample import Sample
        return self._getRecordByID( Sample, id )
    
    def getSamples(self, where = None):
        '''retrieve all samples'''
        from vnf.dom.Matter import Matter
        return self._getAll( Matter, where )

    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._getRecordByID( SampleAssembly, id )
    
#    def getScatteringKernels(self, where = None):
#        '''retrieve all scattering kernels'''
#        from vnf.dom.ScatteringKernel2 import ScatteringKernel2
#        return self._getAll( ScatteringKernel2, where )


    def getSimulationResults(self, record):
        type = record.__class__.__name__
        id = record.id
        from vnf.dom.SimulationResult import SimulationResult as table
        records = self.db.fetchall(
            table, where = "simulation_type='%s' and simulation_id='%s'" % (
            type, id) )
        return records
    

    def getUser(self, username):
        '''retrieve user of given username'''
        from vnf.dom.User import User
        all = self.db.fetchall( User, where = "username='%s'" % username )
        assert len(all) == 1
        return all[0]
        
    def getInstrument(self, id):
        '''retrieve instrument of given id'''
        from vnf.dom.Instrument import Instrument
        return self._getRecordByID( Instrument, id )


    def getConfiguredScatterer(self, id):
        from vnf.dom.ConfiguredScatterer import ConfiguredScatterer
        return self._getRecordByID( ConfiguredScatterer, id )


    def getConfiguredInstrument(self, id):
        '''retrieve configured instrument of given id'''
        from vnf.dom.ConfiguredInstrument import ConfiguredInstrument as table
        return self._getRecordByID( table, id )


    def getInstrumentConfiguration(self, name, id):
        '''retrieve instrument configuration
        name: name of instrument
        id: id of configuration for the given instrument
        '''
        table = self._instrument_configuration_table( name )
        if table is None:
            from vnf.dom.Instrument import Instrument as table
        return self._getRecordByID( table, id )


    def makeShape(self, type):
        '''create a shape pointer db record and a solid shape instance
        shape pointer --> solid shape instance
        type is the type of the solid shape instance
        return the shape pointer
        '''
        #create the solid shape instance
        module = __import__( 'vnf.dom.%s' % type, {}, {}, [''] )
        table = getattr( module, type )
        shape = self.new_dbobject( table )

        #create the pointer
        from vnf.dom.Shape import Shape
        shapeptr = self.new_dbobject( Shape )
        shapeptr.type = type
        shapeptr.reference = shape.id
        self.updateRecord( shapeptr )
        
        return shapeptr


    def destroyShape(self, shape):
        '''destroy a shape pointer

        It not only delete the pointer record, but also the
        db record of the solid shape that this pointer points to.
        '''
        shape = self.getHierarchy( shape )
        self.deleteRecord( shape.realshape )
        self.deleteRecord( shape )
        return


    def newInstrumentConfiguration(self, name):
        '''create new instrument configuration
        name: name of instrument
        '''
        table = self._instrument_configuration_table( name )
        return self.new_dbobject( table )
    

    def getComponent(self, id):
        '''retrieve component of given id'''
        from vnf.dom.Component import Component
        return self._getRecordByID( Component, id )
    
    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )
    
    def getConfiguredScatterers(self, id):
        '''retrieve configured scatterers in the sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        from vnf.dom.ConfiguredScatterer import ConfiguredScatterer

        referencetable = SampleAssembly.Scatterers
        
        records = self.db.fetchall(
            referencetable, where = "localkey='%s'" % id )

        ret = []
        
        for record in records:
            scattererID = record.remotekey
            scattererrecord = self._getRecordByID(
                ConfiguredScatterer, scattererID )
            # set "label" - sample, sample_holder, furnace
            # label is an attribute of a scatterer in a sample assembly
            # it is not an attribute of a scatterer itself (you can
            # do a scattering experiment using a furnace as a sample,
            # for example). so the label attribute is saved in
            # the reference table. here we transfer it to the
            # abstract scatterer record.
            scattererrecord.label = record.label
            ret.append( scattererrecord )
            continue

        return ret
    

    def getComponents(self, id):
        '''retrieve components in the instrument of given id'''
        from vnf.dom.Instrument import Instrument
        referencetable = Instrument.Components
        
        records = self.db.fetchall(
            referencetable, where = "localkey='%s'" % id )

        from vnf.dom.Component import Component
        ret = []
        
        for record in records:
            componentID = record.remotekey
            componentrecord = self._getRecordByID( Component, componentID )
            componentrecord.label = record.label
            ret.append( componentrecord )
            continue

        return ret

    def getInstrumentGeometer(self, instrument):
        id = instrument.id
        from vnf.dom.Instrument import Instrument
        records = self.db.fetchall(
            Instrument.Geometer, where = 'container_id=%r' % id )
        geometer = {}
        for record in records:
            geometer[ record.element_label ] = record
            continue
        return geometer

    def getScatteringKernels(self, id):
        '''retrieve kernels in the scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        from vnf.dom.ScatteringKernel import ScatteringKernel
        return self._getElements(
            id, Scatterer.Kernels, ScatteringKernel)


    def getServer(self, id):
        '''retrieve server of given id'''
        from vnf.dom.Server import Server
        return self._getRecordByID( Server, id )
    
    def getServers(self, where = None):
        '''retrieve all servers'''
        from vnf.dom.Server import Server
        return self._getAll( Server, where )


    def getShape(self, id):
        '''retrieve shape of given id'''
        from vnf.dom.Shape import Shape
        return self._getRecordByID( Shape, id )


    def getRealShape(self, id):
        '''given id in the shape table, retrieve the real
        shape's record.
        The shape table contains type and reference_id
        info of the shape.
        To look up the real shape, we have to
        go to the table of the given shape type
        and find the record of given id.
        '''
        from vnf.dom.Shape import Shape
        return self._getRealObject( id, Shape )


    def getRealScatteringKernel(self, id):
        from vnf.dom.ScatteringKernel import ScatteringKernel
        return self._getRealObject( id, ScatteringKernel)


    def getPhononDispersion(self, id):
        from vnf.dom.PhononDispersion import PhononDispersion
        return self._getRecordByID( PhononDispersion, id )


    def getRealPhononDispersion(self, id):
        from vnf.dom.PhononDispersion import PhononDispersion
        return self._getRealObject( id, PhononDispersion )


    def getNeutronExperiment(self, id):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._getRecordByID( NeutronExperiment, id )


    def getSampleEnvironment(self,id):
        from vnf.dom.SampleEnvironment import SampleEnvironment
        return self._getRecordByID( SampleEnvironment, id )


    def getAbstractScatterer(self, impltablename, id ):
        '''obtain record in the abstract scatterer table given the
        implementation table and id'''
        
        from vnf.dom.Scatterer import Scatterer
        all = self.db.fetchall(
            Scatterer, where = "type='%s' and reference='%s'" % (
            impltablename, id) )
        assert len(all) == 1
        return all[0]


    def deleteScattererFromSampleAssembly(
        self, scatterer_id, sampleassembly_id ):

        # mark scatterer as deleted
        record = self.getScatterer( scatterer_id )
        assignments = [ ('status', 'd'), ]
        self.db.updateRow(
            record, assignments, where = "id='%s'" % scatterer_id)

        # detach scatterer from sampleassembly
        from vnf.dom.SampleAssembly import SampleAssembly
        table = SampleAssembly.Scatterers
        records = self.db.fetchall(
            table,
            where = "localkey='%s' and remotekey='%s'" % (
            sampleassembly_id, scatterer_id )
            )
        assert len(records) == 1
        reference = records[0]

        self.db.deleteRow(table, where="id='%s'" % reference.id)
        return


    def deleteRecord(self, record):
        table = record.__class__
        self.db.deleteRow( table, where="id='%s'" % record.id )
        return
    

    def newJob(self, job):
        self.db.insertRow(job)
        return


    def newReference(self, table, localkey, remotekey):
        '''create a new reference record.

        The new record will not be inserted to the db.
        So you have to do that some time in the future.
        '''
        record = table()
        id = new_id( self.director )
        record.id = id
        record.localkey = localkey
        record.remotekey = remotekey
        return record
    

    def new_ownedobject(self, table):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        director = self.director
        
        record = table()
        
        id = new_id( director )
        record.id = id

        record.creator = director.sentry.username
        
        self.newRecord( record )
        return record


    def new_dbobject(self, table):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
        '''
        director = self.director
        
        record = table()
        
        id = new_id( director )
        record.id = id

        self.newRecord( record )
        return record


    def newRecord(self, record):
        'insert a new record into db'
        try:
            self.db.insertRow( record )
        except:
            columns = record.getColumnNames()
            values = [ record.getColumnValue( column ) for column in columns ]
            s = ','.join(
                [ '%s=%s' % (column, value)
                  for column, value in zip(columns, values)
                  ] )
            self._debug.log( 'failed to insert record: %s' % s)
            raise
        return record


    def _instrument_configuration_table(self, name):
        tablename = '%sconfiguration' % name
        try:
            exec 'from vnf.dom.%s import %s as table' % (
                tablename, tablename )
        except ImportError:
            return
        return table


    def _getElementIDs(self, id, referencetable):
        '''retrieve ids of elements in the container of the given id'''
        records = self.db.fetchall(
            referencetable, where = "localkey='%s'" % id )
        elementIDs = [
            record.remotekey for record in records]
        return elementIDs

    
    def _getElements(self, id, referencetable, elementtable):
        '''retrieve elements in the container of given id'''
        ids = self._getElementIDs( id, referencetable )
        records = [
            self._getRecordByID( elementtable, id )
            for id in ids]
        return records


    def _getRealObject(self, id, table):
        '''given id in a virtual table, retrieve the real
        object's record.
        A virtual table contains type and reference_id
        info of the real object.
        To look up the real object, we have to
        go to the table of the given object type
        and find the record of given id.
        '''
        record = self._getRecordByID( table, id )
        type = record.type
        id1 = record.reference
        #import vnf.dom.PolyCrystal
        module = __import__( 'vnf.dom.%s' % type, {}, {}, [''] )
        # "from vnf.dom.%s import %s as RealObj" % (type, type)
        temp=getattr(module, type)
        obj = self._getRecordByID( temp, id1 )
        return obj


    def _index(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        for item in all:
            index[item.id] = item
        return index
    
    def _getAll(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        return all

    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)


    def _init(self):
        Component._init(self)
        self.deepcopy = DeepCopier( self )
        return



class DeepCopier:

    def __init__(self, clerk):
        self.clerk = clerk
        self.director = clerk.director
        return


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onSampleAssembly(self, sa):
        #first copy all scatterers
        scatterers = sa.scatterers
        scatterer_copies = [ self( scatterer ) for scatterer in scatterers ]
        from vnf.dom.SampleAssembly import SampleAssembly
        sa_copy = self.clerk.new_ownedobject( SampleAssembly )

        self._copy_attrs( sa, sa_copy, attrs = ['short_description'] )

        #fill the one-many relation table of SampleAssembly.Scatterers
        from vnf.dom.SampleAssembly import SampleAssembly
        for scatterer in scatterer_copies:
            label = scatterer.label
            ref = self.clerk.newReference(
                SampleAssembly.Scatterers,
                sa_copy.id, scatterer.id )
            #transfer label
            ref.label = label
            #new record to db
            self.clerk.newRecord( ref )
            continue
        
        sa_copy.scatterers = scatterer_copies

        # update record
        self.clerk.updateRecord( sa_copy )
        
        return sa_copy


    def onShape(self, shape):
        #first copy the real shape
        realshape = shape.realshape
        realshape_copy = self(realshape)

        #now make a new record
        from vnf.dom.Shape import Shape
        shape_copy = self.clerk.new_ownedobject( Shape )
        
        #copy some attrs from old record
        attrs = ['type', 'short_description']
        self._copy_attrs( shape, shape_copy, attrs )

        #new record should point to the new real shape
        shape_copy.reference = realshape_copy.id

        #update record to db
        self.clerk.updateRecord( shape_copy )
        return shape_copy


    def onScatterer(self, scatterer):
        #first copy the real scatterer
        realscatterer = scatterer.realscatterer
        realscatterer_copy = self(realscatterer)

        #now make a new record
        from vnf.dom.Scatterer import Scatterer
        scatterer_copy = self.clerk.new_ownedobject( Scatterer )
        
        #copy some attrs from old record
        attrs = ['type', 'short_description']
        self._copy_attrs( scatterer, scatterer_copy, attrs )

        #new record should point to the new real scatterer
        scatterer_copy.reference = realscatterer_copy.id
        #attach real scatterer copy to the scatterer copy
        scatterer_copy.realscatterer = realscatterer_copy

        #update record to db
        self.clerk.updateRecord( scatterer_copy )
        
        #remember my label in my sampleassembly
        try: scatterer_copy.label = scatterer.label
        except: scatterer_copy.label = None
        
        return scatterer_copy


    def onPolyXtalScatterer(self, scatterer):
        #first make copies of shape and crystal
        shape_copy = self( scatterer.shape )
        crystal_copy = self( scatterer.crystal )
        
        #now make a new record
        from vnf.dom.PolyXtalScatterer import PolyXtalScatterer as table
        scatterer_copy = self.clerk.new_ownedobject( table )
        
        #copy some attrs from old record
        attrs = ['short_description']
        self._copy_attrs( scatterer, scatterer_copy, attrs )

        #new record should point to the new crystal and shape
        scatterer_copy.shape_id = shape_copy.id
        scatterer_copy.crystal_id = crystal_copy.id

        #update record to db
        self.clerk.updateRecord( scatterer_copy )
        return scatterer_copy


    def onBlock(self, block):
        #now make a new record
        from vnf.dom.Block import Block as table
        block_copy = self.clerk.new_ownedobject( table )
        
        #copy some attrs from old record
        attrs = ['height', 'width', 'thickness', 'short_description']
        self._copy_attrs( block, block_copy, attrs )

        #update record to db
        self.clerk.updateRecord( block_copy )
        return block_copy
    
    def onCylinder(self, cylinder):
        #now make a new record
        from vnf.dom.Cylinder import Cylinder as table
        cylinder_copy = self.clerk.new_ownedobject( table )
        
        #copy some attrs from old record
        attrs = ['height', 'radius', 'short_description']
        self._copy_attrs( cylinder, cylinder_copy, attrs )

        #update record to db
        self.clerk.updateRecord( cylinder_copy )
        return cylinder_copy


    def onCrystal(self, crystal):
        #now make a new record
        from vnf.dom.Crystal import Crystal as table
        crystal_copy = self.clerk.new_ownedobject( table )
        
        #copy some attrs from old record
        attrs = ['datafile', 'chemical_formula', 'short_description']
        self._copy_attrs( crystal, crystal_copy, attrs )

        #update record to db
        self.clerk.updateRecord( crystal_copy )
        return crystal_copy


    def onInstrument(self, instrument):
        components = instrument.components
        component_copies = [ self( component ) for component in components ]
        from vnf.dom.Instrument import Instrument
        instrument_copy = self.clerk.new_ownedobject( Instrument )

        for prop in ['short_description', 'componentsequence', 'category']:
            setattr( instrument_copy, prop,
                     getattr( instrument, prop ) )
            continue
        
        from vnf.dom.Instrument import Instrument
        for component in component_copies:
            label = component.label
            ref = self.clerk.newReference(
                Instrument.Components,
                instrument_copy.id, component.id )
            #transfer label
            ref.label = label
            self.clerk.newRecord( ref )
            #made individual component available in instrument's name space
            setattr( instrument_copy, label, component )
            continue
        
        instrument_copy.components = component_copies

        geometer = instrument.geometer
        #geometer is a dictionary of label: record
        geometer_copy = {}
        for name, record in geometer.iteritems():
            recordcopy = self.onInstrumentGeometer( record )
            recordcopy.container_id = instrument_copy.id
            self.clerk.updateRecord( recordcopy )
            geometer_copy[ name ] = recordcopy
            continue
        instrument_copy.geometer = geometer_copy

        self.clerk.updateRecord( instrument_copy )
        
        return instrument_copy


    def onInstrumentGeometer(self, record):
        from vnf.dom.Instrument import Instrument
        new = self.clerk.new_ownedobject( Instrument.Geometer )
        attrs = ['element_label', 'position', 'orientation', 'reference_label']
        for attr in attrs:
            setattr(new, attr, getattr(record, attr) )
            continue
        self.clerk.updateRecord( new )
        return new
    

    def onComponent(self, component):
        realcomponent = component.realcomponent
        realcomponent_copy = self(realcomponent)

        from vnf.dom.Component import Component
        component_copy = self.clerk.new_ownedobject( Component )
        component_copy.type = realcomponent.__class__.__name__
        component_copy.reference = realcomponent_copy.id
        self.clerk.updateRecord( component_copy )

        #remember my label in my instrument
        component_copy.label = component.label
        return component_copy


    def onMonochromaticSource(self, source):
        from vnf.dom.MonochromaticSource import MonochromaticSource
        copy = self.clerk.new_ownedobject( MonochromaticSource )
        copy.energy = source.energy
        self.clerk.updateRecord(copy)
        return copy


    def onIQEMonitor(self, iqem):
        from vnf.dom.IQEMonitor import IQEMonitor
        copy = self.clerk.new_ownedobject( IQEMonitor )
        attrs = [
            'Emin', 'Emax', 'nE',
            'Qmin', 'Qmax', 'nQ',
            'max_angle_in_plane', 'min_angle_in_plane',
            'max_angle_out_of_plane', 'min_angle_out_of_plane',
            'short_description',
            ]
        for attr in attrs:
            setattr( copy, attr, getattr( iqem, attr) )
            continue
        self.clerk.updateRecord(copy)
        return copy


    def onDetectorSystem_fromXML(self, record):
        from vnf.dom.DetectorSystem_fromXML import DetectorSystem_fromXML \
             as table
        copy = self.clerk.new_ownedobject( table )
        attrs = [
            'tofmin', 'tofmax', 'ntofbins',
            ]
        for attr in attrs:
            setattr( copy, attr, getattr( record, attr) )
            continue
        self.clerk.updateRecord(copy)
        return copy


    def _copy_attrs(self, old, new, attrs):
        for attr in attrs:
            setattr(new, attr, getattr(old, attr) )
            continue
        return

    pass # end of DeepCopier


class HierarchyRetriever:

    def __init__(self, clerk):
        self.clerk = clerk
        return
    

    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onNeutronExperiment(self, experiment):
        instrument_id = experiment.instrument_id
        if empty_id( instrument_id ):
            instrument = None
        else:
            configured_instrument = self.clerk.getConfiguredInstrument(
                instrument_id )
            configure_instrument = self(configured_instrument)
            instrument = configured_instrument
        experiment.instrument = instrument

        sampleassembly_id = experiment.sampleassembly_id
        if empty_id(sampleassembly_id):
            sampleassembly = None
        else:        
            sampleassembly = self.clerk.getSampleAssembly( sampleassembly_id )
            sampleassembly = self(sampleassembly)
        experiment.sampleassembly = sampleassembly

        job_id = experiment.job_id
        if empty_id(job_id):
            job = None
        else:
            job = self.clerk.getJob( job_id )
            job = self(job)

        experiment.job = job
        return experiment


    def onJob(self, job):
        server = job.server
        if empty_id(server):
            computation_server= None
        else:
            computation_server = self.clerk.getServer( server )
            computation_server = self(computation_server)
        job.computation_server = computation_server
        job.short_description = job.jobName
        return job


    def onServer(self, server):
        server.short_description = '%s@%s' % (server.server, server.location)
        return server


    def onConfiguredInstrument(self, configured):
        instrument_id = configured.instrument_id
        if empty_id(instrument_id):
            # if instrument is not specified, configuration is not
            # meaningful
            configured.instrument = None
            configured.configuration = None
            return configured

        instrument = self.clerk.getInstrument( instrument_id )
        instrument = self(instrument)

        configuration_id = configured.configuration_id
        if empty_id(configuration_id):
            # if configuration is not explicit,
            # it will be explicitly stored in the instrument table.
            # be sure that this 'instrument' (actually configuration)
            # could contain
            # less components than the original template instrument.
            # it could contain no component too.
            configuration = None
            # create a new instrument record
            #from vnf.dom.Instrument import Instrument
            #instrument = self.clerk.new_ownedobject( Instrument )
            #configuration_id = configured.configuration_id = instrument.id
            #self.clerk.updateRecord( configured )
        else:
            configuration = self.clerk.getInstrumentConfiguration(
                instrument_id, configuration_id )
            configuration = self(configuration)

        configured.instrument = instrument
        configured.configuration = configuration
        return configured


    def onInstrument(self, instrument):
        self.clerk._debug.line(  str(instrument.__class__) )
        self.clerk._debug.log( '%s' % instrument.id )
        components = self.clerk.getComponents( instrument.id )
        components = [ self( component ) for component in components ]
        instrument.components = components
        self.clerk._debug.line( str(dir(instrument)) )
        self.clerk._debug.log( '%s' % instrument.id )
        # make individual component available in instrument's namespace
        for component in components:
            setattr(instrument, component.label, component)
            continue

        self.clerk._debug.line(  str(dir(instrument)) )
        self.clerk._debug.log( '%s' % instrument.id )
        try:
            geometer = self.clerk.getInstrumentGeometer( instrument )
            instrument.geometer = geometer
        except:
            # does not have geometer records
            import traceback
            self.clerk._debug.log( traceback.format_exc() )
            pass
        
        return instrument


    def onARCSconfiguration(self, configuration):
        return configuration


    def onComponent(self, component):
        realcomponent = self.clerk.getRealComponent( component.id )
        component.realcomponent = self(realcomponent)
        return component


    def onMonochromaticSource(self, source):
        return source


    def onIQEMonitor(self, iqem):
        return iqem


    def onDetectorSystem_fromXML(self, ds):
        return ds


    def onSampleAssembly(self, sampleassembly):
        scatterers = self.clerk.getConfiguredScatterers( sampleassembly.id )
        scatterers = [ self( scatterer ) for scatterer in scatterers ]
        sampleassembly.scatterers = scatterers
        return sampleassembly


    def onConfiguredScatterer(self, configured):
        scatterer_id = configured.scatterer_id
        if empty_id(scatterer_id):
            scatterer = None
        else:
            scatterer = self.clerk.getScatterer( scatterer_id )
            scatterer = self(scatterer)
        configured.scatterer = scatterer

        configuration_id = configured.configuration_id
        if empty_id( configuration_id ): configuration = None
        else:
            configuration = self.clerk.getScatterer( configuration_id )
            configuration = self(configuration)
            pass # endif
        configured.configuration = configuration
        return configured


#    def onScatterer(self, scatterer):
#        try:
#            realscatterer = self.clerk.getRealScatterer( scatterer.id )
#        except Exception, error:
#            import traceback
#            self.clerk._debug.log(traceback.format_exc() )
#            return scatterer
#        scatterer.realscatterer = self(realscatterer)
#        return scatterer

    def onScatterer(self, scatterer):
        matter_id =  scatterer.matter_id
        if empty_id( matter_id ):
            matter = None
        else:
            matter = self.clerk.getMatter(matter_id )
            matter = self(matter)

        shape_id = scatterer.shape_id
        if empty_id(shape_id):
            shape = None
        else:
            shape = self.clerk.getShape(shape_id)
            shape = self(shape)
        
        scatterer.shape = shape
        scatterer.matter = matter
    
        try:
            kernels = self.clerk.getScatteringKernels( scatterer.id )
        except:
            import traceback
            self.clerk._debug.log(traceback.format_exc())
            kernels = []
        kernels = [ self(kernel) for kernel in kernels ]
        scatterer.kernels = kernels
        return scatterer
    
    
    def onMatter(self, matter):
        realmatter = self.clerk.getRealMatter( matter.id )
        realmatter = self(realmatter)
        matter.realmatter = realmatter
        return matter
    
    
    def onGulpScatteringKernel(self, gulpScatteringKernel):
        return gulpScatteringKernel
    
    
    def onPolyCrystal(self, record):
        return record
    
    
    def onDisordered(self, record):
        return record
    

    def onScatteringKernel(self, kernel):
        realkernel = self.clerk.getRealScatteringKernel( kernel.id )
        kernel.realscatteringkernel = self(realkernel)
        return kernel
    

    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        dispersion_id = kernel.dispersion_id
        dispersion = self.clerk.getPhononDispersion( dispersion_id )
        dispersion = self(dispersion)
        kernel.dispersion = dispersion
        return kernel


    def onPhononDispersion(self, dispersion):
        realdispersion = self.clerk.getRealPhononDispersion( dispersion.id )
        realdispersion = self(realdispersion)
        dispersion.realphonondispersion = realdispersion
        return dispersion


    def onIDFPhononDispersion(self, dispersion):
        return dispersion


    def onCrystal(self, crystal):
        return crystal


    def onShape(self, shape):
        try:
            realshape = self.clerk.getRealShape( shape.id )
        except Exception, error:
            import traceback
            self.clerk._debug.log(traceback.format_exc() )
            return shape
        shape.realshape = self(realshape)
        return shape


    def onBlock(self, block):
        return block
    
    def onCylinder(self, cylinder):
        return cylinder


    def onCylinder(self, cylinder):
        return cylinder


    pass # end of Clerk



def _tostr( value ):
    if isinstance( value, list ) or isinstance(value, tuple):
        ret =  '{%s}' % ','.join( [ str(item) for item in value ] )
        return ret
    return str(value)


from misc import new_id, empty_id

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 
