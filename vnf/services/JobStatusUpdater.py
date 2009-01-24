#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.services.TCPService import TCPService


class JobStatusUpdater(TCPService):


    class Inventory(TCPService.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        from vnf.components.SSHer import SSHer
        csaccessor = pyre.inventory.facility(
            name='csaccessor', factory = SSHer, args = ['jsu-ssher', 'ssher'])
        csaccessor.meta['tip'] = 'computing server accessor'

        uncompleted = pyre.inventory.str('uncompleted', default = 'uncompleted-job-list')
        uncompleted.meta['tip'] = 'file to contain list of jobs that are not completed'
        
        from vnf.services.Pickler import Pickler
        marshaller = pyre.inventory.facility(
            "marshaller", factory=Pickler, args = ['jsu-pickler'])


    def generateClientConfiguration(self, registry):
        """update the given registry node with sufficient information to grant access to clients"""

        import pyre.parsing.locators
        locator = pyre.parsing.locators.simple('service')

        # get the inherited settings
        TCPService.generateClientConfiguration(self, registry)

        # record the marshaller name
        registry.setProperty('marshaller', self.marshaller.name, locator)

        # get the marshaller to record his configuration
        marshaller = registry.getNode(self.marshaller.name)
        self.marshaller.generateClientConfiguration(marshaller)

        return


    def onTimeout(self, selector):
        import time
        self._info.log("thump")

        self._check()
        return True


    def onReload(self, *unused):
        return self.userManager.onReload()


    def __init__(self, name=None):
        if name is None:
            name = "jsu"

        TCPService.__init__(self, name)

        return


    def _configure(self):
        TCPService._configure(self)
        self.marshaller = self.inventory.marshaller
        self.uncompleted = self.inventory.uncompleted
        self.clerk = self.inventory.clerk
        self.csaccessor = self.inventory.csaccessor

        self.clerk.director = self
        return


    def _init(self):
        TCPService._init(self)
        
        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # set id generator for referenceset
        def _id():
            from vnf.components.misc import new_id
            return new_id(self)
        vnf.dom.set_idgenerator(_id)
        return
    

    def _check(self):
        old_uncompleted = self._read_uncompleted_jobs()
        self._updateJobStatus(old_uncompleted)
        
        new_uncompleted = self._get_new_uncompleted()
        self._debug.log('old list: %s' % (old_uncompleted,) )
        self._debug.log('new list: %s' % (new_uncompleted,) )

        # find jobs that were just completed
        just_completed = filter(lambda j: j not in new_uncompleted, old_uncompleted)
        
        # for each job that just completed, send an email to the user
        from vnf.dom.Job import Job
        for jid in just_completed:
            print jid
            job = self.clerk.db.fetchall(Job, where="id='%s'" % jid)[0]
            self._alert_user(job)
            continue

        # update the 'uncompleted' list
        open(self.uncompleted, 'w').write( '\n'.join(
            [ '%s' % j  for j in new_uncompleted ] ) )
        return


    def _updateJobStatus(self, jobids):
        from vnf.components.Scheduler import check
        for jid in jobids:
            job = self.clerk.getJob(jid)
            check(job, self)
            continue
        return


    def _read_uncompleted_jobs(self):
        if not os.path.exists(self.uncompleted): return []
        return filter(lambda line: len(line.strip()),
                      open(self.uncompleted).read().split('\n') )


    def _alert_user(self, job):
        user = self.clerk.getUser(job.creator)
        email = user.email
        title = 'Your vnf job %s is now %s.' % (job.id, job.state)
        content = [
            'Please log into vnf website and then look for job %s' % job.id,
            'by\n',
            '1. select "Jobs" from main menu\n',
            '2. look for job %s\n' % job.id,
            ]
        content = ''.join(content)
        self._sendemail(email, title, content)
        return


    def _sendemail(self, email, title, content):
        myemail = 'vnfdemo@gmail.com'
        from email.mime.text import MIMEText
        msg = MIMEText(content)
        msg['Subject'] = title
        msg['From'] = myemail
        msg['To'] = email
        
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com')
        server.ehlo()
        server.starttls()
        server.login('vnfdemo', '56tyghbn')
        server.sendmail(
            myemail,
            email,
            msg = msg.as_string())
        return


    def _get_new_uncompleted(self):
        from vnf.dom.Job import Job
        uncompleted_states = [
            'submitted',
            'running',
            'onhold',
            ]
        all = []
        for state in uncompleted_states:
            all += self.clerk.db.fetchall(Job, where = "state='%s'" % state)
            continue
        return [j.id for j in all]

import os

# version
__id__ = "$Id$"

# End of file 
