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
        from vnf.dom import subclassesOf
        tables = subclassesOf( ScatteringKernel )

        ret = {}
        for table in tables:
            temp = self._index( table, where )
            for id, record in temp.iteritems():
                ret[ (id, table) ] = record
                continue
            continue
        return ret

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
        
        self.db.updateRow(record.__class__, assignments, where)
        return record


    def getRecordByID(self, tablename, id):
        exec 'from vnf.dom.%s import %s as Table' % (tablename, tablename) \
             in locals()
        return self._getRecordByID( Table, id )


    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )

    
    def getJob(self, id):
        '''retrieve job of given id'''
        from vnf.dom.Job import Job
        return self._getRecordByID( Job, id )
    
    
    def getJobs(self, where = None):
        '''retrieve all jobs'''
        from vnf.dom.Job import Job
        return self._getAll( Job, where )
    
    
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
        from vnf.dom.SimulationResult import SimulationResult as table
        simulation = table.simulation = record
        where = "simulation='%s'" % simulation
        records = self.db.fetchall(table, where = where)
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


    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )

    
    def getServer(self, id):
        '''retrieve server of given id'''
        from vnf.dom.Server import Server
        return self._getRecordByID( Server, id )
    

    def getServers(self, where = None):
        '''retrieve all servers'''
        from vnf.dom.Server import Server
        return self._getAll( Server, where )


    def getNeutronExperiment(self, id):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._getRecordByID( NeutronExperiment, id )


    def getSampleEnvironment(self,id):
        from vnf.dom.SampleEnvironment import SampleEnvironment
        return self._getRecordByID( SampleEnvironment, id )


    def deleteRecord(self, record):
        table = record.__class__
        self.db.deleteRow( table, where="id='%s'" % record.id )
        return
    

    def newJob(self, job):
        self.db.insertRow(job)
        return


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
        # a new container. empty
        from vnf.dom.SampleAssembly import SampleAssembly
        sa_copy = self.clerk.new_ownedobject( SampleAssembly )
        
        #first copy all scatterers
        scatterers = sa.scatterers
        self._copyReferenceSet( scatterers, sa_copy.scatterers )

        #then copy attributes
        self._copy_attrs( sa, sa_copy, attrs = ['short_description'] )

        # update record
        self.clerk.updateRecord( sa_copy )
        
        return sa_copy


    def onInstrument(self, instrument):
        # a new container. empty
        from vnf.dom.Instrument import Instrument
        instrument_copy = self.clerk.new_ownedobject( Instrument )

        #first copy all components
        components = sa.components
        self._copyReferenceSet( components, instrument_copy.components )

        #then copy attributes
        attrs = ['short_description', 'componentsequence', 'category']
        self._copy_attrs( sa, sa_copy, attrs = attrs )

        #copy geometer
        geometer = instrument.geometer
        self._copyGeometer( geometer, instrument_copy.geometer )

        #save
        self.clerk.updateRecord( instrument_copy )
        
        return instrument_copy


    def onScatterer(self, scatterer):
        #first make copies of shape and matter
        matter_copy = self._onreference( scatterer.shape )
        shape_copy = self._onreference( scatterer.crystal )
        
        #now make a new record
        from vnf.dom.Scatterer import Scatterer as table
        scatterer_copy = self.clerk.new_ownedobject( table )
        
        #copy some attrs from old record
        attrs = ['short_description']
        self._copy_attrs( scatterer, scatterer_copy, attrs )

        #new record should point to the new matter and shape
        scatterer_copy.shape = shape_copy
        scatterer_copy.matter = matter_copy

        #update record to db
        self.clerk.updateRecord( scatterer_copy )
        return scatterer_copy


    def onBlock(self, block):
        return self._onRecordWithID( block )
    
    
    def onCylinder(self, cylinder):
        return self._onRecordWithID( cylinder )


    def onCrystal(self, crystal):
        return self._onRecordWithID( crystal )


    def onMonochromaticSource(self, source):
        return self._onRecordWithID( source )


    def onIQEMonitor(self, iqem):
        return self._onRecordWithID( iqem )


    def onDetectorSystem_fromXML(self, record):
        return self._onRecordWithID( record )


    def _onreference(self, reference):
        record = reference.dereference()
        copy = self(record)
        newreference = reference.__class__( copy.id, copy.__class__ )
        return newreference


    def _onRecordWithID(self, record):
        # work with normal records with no reference, referenceset, etc
        from copy import copy
        newrecord = copy( record )
        newrecord.id = new_id( self.director )
        self.clerk.updateRecord( newrecord )
        return newrecord


    def _copyReferenceSet(self, referenceset, newreferenceset):
        elements = referenceset.dereference()
        for name, element in elements:
            elementcopy = self(element)
            newreferenceset.add( elementcopy, db, name = name )
            continue
        return


    def _copyGeometer(self, geometer, newgeometer):
        db = self.clerk.db
        registry = geometer.dereference()
        for k,v in registry.iteriterms():
            newgeometer.add( k, v.position, v.orientation, db, reference = v.reference)
            continue
        return 


    def _copy_attrs(self, old, new, attrs):
        for attr in attrs:
            setattr(new, attr, getattr(old, attr) )
            continue
        return

    pass # end of DeepCopier


def _tostr( value ):
    if isinstance( value, list ) or isinstance(value, tuple):
        ret =  '{%s}' % ','.join( [ str(item) for item in value ] )
        return ret
    return str(value)


from misc import new_id, empty_id

# version
__id__ = "$Id$"

# End of file 
