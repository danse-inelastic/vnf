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


    def execute(self, *args, **kwds):
        options = self._parseOutputOptions()
        kwds['stdout'] = options.outputlog
        kwds['stderr'] = options.errorlog
        super(Launch, self).execute(*args, **kwds)
        return


    def _parseOutputOptions(self):
        import optparse
        parser = optparse.OptionParser()
        parser.add_option('', '--output-log', dest='outputlog', default='/dev/null')
        parser.add_option('', '--error-log', dest='errorlog', default='/dev/null')
        import sys
        args = [sys.argv[0]]
        keys = ['--output-log', '--error-log']
        for arg in sys.argv[1:]:
            for key in keys:
                if arg.startswith(key):
                    args.append(arg)
        (options, args) = parser.parse_args(args)
        return options


    def help(self):
        import sys
        cmd = sys.argv[0]
        print
        print ' $ %s \\' % cmd
        print '   --home=<work-directory-for-the-command> \\'
        print '   --cmd=<command> \\'
        print '   --output-log=<output log file> \\'
        print '   --error-log=<error log file> \\'
        return


    def main(self, *args, **kwds):
        #self.configureJournal(self.logfile)
        cmd = self.inventory.cmd
        self._debug.log( 'cmd=%r' % cmd )
        #print cmd
        import os, shlex
        self._debug.log( 'curdir=%r' % os.path.abspath(os.curdir))
        all = shlex.split(cmd)
        program = all[0]
        os.execvp(program, all)
        return


    def configureJournal(self, path=None):
        if not path: path = self.name + '.log'
        
        # open the logfile
        stream = file(path, "w")

        # attach it as the journal device
        import journal
        journal.logfile(stream)

        return


    def _defaults(self):
        super(Launch, self)._defaults()
        self.inventory.typos = 'relaxed'
        return


    def _configure(self):
        Application._configure(self)
        import os
        self.home = os.path.abspath(self.inventory.home)
        self.cmd = self.inventory.cmd
        return


def main():
    Launch('launch-detached').run()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
