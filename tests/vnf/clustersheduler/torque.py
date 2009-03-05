#!/usr/bin/env python
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


from pyre.applications.Script import Script as Base


class TestApp(Base):


    class Inventory(Base.Inventory):
        
        import pyre.inventory

        # components
        from vnf.components import ssher
        csaccessor = pyre.inventory.facility( name='csaccessor', factory = ssher)
        csaccessor.meta['tip'] = 'computing server accessor'


    def main(self, *args, **kwds):
        from vnf.clusterscheduler import scheduler as factory
        scheduler = factory('torque')

        class server:
            address = 'localhost'
            port = 50022
            username = 'linjiao'
            workdir = '/home/linjiao/vnfjobs'

        torqueid = '231'
        jobremotedir = '/home/linjiao/vnfjobs/jobs/MCDFU'
        launch = lambda cmd: self.csaccessor.execute(
            cmd, server, jobremotedir, suppressException=True)

        scheduler = scheduler(launch, prefix = 'source ~/.vnf' )

        print scheduler.status(torqueid)
        return
    

    def __init__(self, name):
        Base.__init__(self, name)
        return


    def _configure(self):
        super(TestApp, self)._configure()
        
        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        super(TestApp, self)._init()
        return



if __name__=='__main__':
    w=TestApp(name='test-torque')
    w.run()
    

# version
__id__ = "$Id$"

# End of file 
