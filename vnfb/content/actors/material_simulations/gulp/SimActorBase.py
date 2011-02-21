#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.content import load, select, alert
import luban.content as lc


# The action to load the job-editor panel
# select(id='main-display-area').replaceContent(...)
loadjobeditor = lambda id: load(
    actor='job', 
    routine='view',
    id = id,
    )
        


from luban.components.AuthorizedActor import AuthorizedActor as base
class SimActorBase(base):
    
    editor_visual_name = None #  'material_simulations/moldyn/optimization-editor'
    dbtable = None #  from vnfb.dom.material_simulations.GulpOpt import GulpOptTable
    
    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str('id')
        
        formids = pyre.inventory.list('formids')
        viewid = pyre.inventory.str('viewid')


    def createView(self, director):
        id = self.inventory.id
        if not id:
            return alert("simulation id not specified")
        
        # get record
        record = self._getRecord(director)
        
        # job
        clerk = director.clerk
        db = clerk.db
        job = record.getJob(db)

        # 
        if not job:
            return director.retrieveVisual(
                self.editor_visual_name,
                id = id,
                director = director,
                )

        doc = lc.document()
        doc.paragraph(text='not yet implemented')
        return doc


    def createJob(self, director):
        """create job for gulp simulation
        
        The user clicks the "create job" button in the view
        and here we check if the user has filled out all forms
        and move on if ok.
        """
        # check if there are unfilled forms
        actions = self._checkForms(director)
        if actions: return actions
        
        return self._createAndViewJob(director)


    def deleteSimulation(self, director):
        #
        clerk = director.clerk
        clerk.importAllDataObjects()
        
        #
        id = self.inventory.id
        if not id:
            return alert("id of simulation not specified")

        # get record
        record = self._getRecord(director)

        # check ownership
        username = director.sentry.username
        if hasattr(record, 'creator') and record.creator != username:
            return alert("simulation %s not owned by you" % id)

        # make sure it is ok to delete
        from vnfb.utils.db.findreferrals import hasreferral
        orm = clerk.orm
        if hasreferral(record, clerk):
            return alert("simulation %s still in use" % id)

        # delete
        obj = orm.record2object(record)
        orm.destroy(obj)
        
        # 
        return load(actor='materialsimulation')


    def _createAndViewJob(self, director):
        doc = lc.document()
        doc.paragraph(text='not yet implemented')
        return doc


    def _checkForms(self, director):
        actions = []; messages = []
        formids = self.inventory.formids
        actions += [select(id=id).addClass('highlighted') for id in formids]
        n = len(formids)
        if n > 1:
            msg = 'sorry. there are %s forms to submit.' % n
        else:
            msg = 'sorry. there is a form to submit.'
        msg += 'Please look for highlighted sections.'
        messages.append(msg)

        if len(actions):
            actions.append(alert('\n\n'.join(messages)))
            return actions


    def _getRecord(self, director):
        id = self.inventory.id
        clerk = director.clerk
        dbtable = self.dbtable
        return clerk.getRecordByID(dbtable, id)



# version
__id__ = "$Id$"

# End of file 

