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


# Specialized form to directly deal with a db object.


from Form import Form as base, InputProcessingError, formactor_action_prefix


class DBObjectForm( base ):

    class Inventory( base.Inventory ):
        import pyre.inventory
        id = pyre.inventory.str( 'id', default = '' )
        short_description = pyre.inventory.str(
            'short_description', default = '' )
        short_description.meta['label'] = "Name"
        short_description.meta['tip'] = 'Please provide a short description'
        pass # end of Inventory


    DBTable = '' # db table class name
    
    
    def legend(self):
        'return a legend string'
        record = self.getRecord()
        if record is None:
            return 'Edit %s' % self.__class__.__name__.lower()
        
        return 'Edit %s %r' % (
            self.__class__.__name__.lower(),
            record.short_description)


    def expand(self, form, errors = None, properties = None, id = ''):
        '''expand an existing form with fields from this component'''

        if id: self.inventory.id = id
        else: id = self.inventory.id

        if not properties:
            properties = self.parameters
            
        if not empty_id( id ):
            record = self.getRecord()
            values = [record.getColumnValue(name) for name in properties]
        
        id_field = form.hidden(
            name = '%s.id' % prefix, value = id)

        super(DBObjectForm, self).expand(
            form,
            errors=errors,
            properties=properties,
            values = values,
            )
        return


    def processUserInputs(self, commit = True, properties = None):
        '''process user inputs and save them to db
        commit: if true, commit to database record. 
        '''
        # check inputs
        super(DBObjectForm, self).processUserInputs(properties = properties)
        
        # prepare a record to accept user inputs
        if empty_id(self.inventory.id):
            record = self.createRecord()
        else:
            record = self.getRecord( )

        if not properties:
            properties = self.parameters
            
        # transfer user inputs to db record
        for prop in properties:
            value = self.inventory.getTraitValue( prop )
            record._setColumnValue(prop, value)
            continue

        # commit if requested
        if commit:
            director = self.director
            if empty_id(record.id):
                #if record is new, create a new db record
                id = new_id( director )
                record.id = id
                director.clerk.newRecord( record )
            else:
                #otherwise, update the record
                director.clerk.updateRecord( record )
            pass # endif
        return record


    def getRecord(self):
        'get DB record'
        id = self.inventory.id
        if empty_id(id): return
        director = self.director
        clerk = director.clerk
        return clerk.getRecordByID( self.DBTable, id )


    def createRecord(self):
        type = self.DBTable
        module = __import__( 'vnf.dom.%s' % type, {}, {}, [''] )
        table = getattr( module, type )
        record = table()
        return record

    pass # end of DBObjectForm


from misc import new_id, empty_id


# version
__id__ = "$Id$"

# End of file 
