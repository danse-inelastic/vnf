#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Daemon import Daemon as Stager
from pyre.applications.Application import Application

class Launch(Application, Stager):

    class Inventory(Application.Inventory):

        import pyre.inventory
        home = pyre.inventory.str('home', default = '/tmp')
        cmd = pyre.inventory.str('cmd', default = '')
        #logfile = pyre.inventory.str('logfile', default = '')
        

    def main(self, *args, **kwds):
        #self.configureJournal(self.logfile)
        cmd = self.inventory.cmd
        self._debug.log( 'cmd=%r' % cmd )
        #print cmd
        from vnf.utils.spawn import spawn
        import os
        self._debug.log( 'curdir=%r' % os.path.abspath(os.curdir))
        ret, out, err = spawn(cmd, env=os.environ)
        if ret:
            self._debug.log( 'out: %s' % out )
            self._debug.log( 'err: %s' % err )
            raise RuntimeError, '%r failed' % (cmd,)
        return


    def configureJournal(self, path=None):
        if not path: path = self.name + '.log'
        
        # open the logfile
        stream = file(path, "w")

        # attach it as the journal device
        import journal
        journal.logfile(stream)

        return


    def _configure(self):
        Application._configure(self)
        self.home = self.inventory.home
        self.cmd = self.inventory.cmd
        #self.logfile = self.inventory.logfile
        return


def main():
    Launch('launch-detached').run()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
