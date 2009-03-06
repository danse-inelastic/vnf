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


depository = '../../../../content/base'

from pyre.applications.Script import Script as Base


class TestApp(Base):


    class Inventory(Base.Inventory):
        
        import pyre.inventory


    def main(self, *args, **kwds):
        import os
        directory = os.path.join(depository, 'announcements')
        entries = os.listdir(directory)

        for entry in entries:
            root, ext = os.path.splitext(entry)
            if ext != '.odb': continue
            testodb = root + '.odb'
            if not os.path.exists( testodb ):
                print '*'*60
                print 'test of announcement ' + entry + 'does not exist'
                continue
            code = open(testodb).read()
            env = {}; exec code in env
            test = env['test']
            try:
                test(self)
            except:
                print '*'*60
                print 'test of announcement ' + entry + ' failed'
                import traceback
                traceback.print_exc()
            continue
        return


    def __init__(self, name):
        super(TestApp, self).__init__(name)
        return


    def _configure(self):
        super(TestApp, self)._configure()
        return


    def _init(self):
        super(TestApp, self)._init()
        return


    def _getPrivateDepositoryLocations(self):
        return [depository]
    

if __name__=='__main__':
    w=TestApp(name='test-announcements')
    w.run()
    

# version
__id__ = "$Id$"

# End of file 
