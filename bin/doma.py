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


from vnfb.components.DOMAccessor import DOMAccessor
basenames = dir(DOMAccessor)
basenames += [
    'aliases',
    'facility',
    'inventory',
    'locator',
    'name',
    ]


from luban.components.Actor import AcceptArbitraryInput
from luban.applications.UIApp import UIApp as base
class DOMAApp(AcceptArbitraryInput, base):

    class Inventory(base.Inventory):

        import pyre.inventory
        name = pyre.inventory.str('name')
        action = pyre.inventory.str('action')
        
        pass # end of Inventory


    def help(self):
        import sys
        cmdname = sys.argv[0]
        print 70*'-'
        print 'Execute methods of domaccessor components using this script'
        print 70*'-'
        print
        print '>>> Usage 1:'
        print ' $ %s -name=<domaccessor>: list methods of the given domaccessor' % cmdname
        print
        print 'E.g.'
        print
        print ' $ %s -name=job' % cmdname
        print
        print '>>> Usage 2:'
        print ' $ %s -name=<domaccessor> -action=<methodname> ...: call the given method of the given domaccessor' % cmdname
        print
        print 'E.g.'
        print
        print ' $ %s -name=job -action=resetJob -id=abcdef' % cmdname
        print
        print 'Calls method resetJob(id="abcdef") of domaccessor "job"'
        print
        return 


    def main(self):
        name = self.inventory.name
        domaccess = self.retrieveDOMAccessor(name)
        if not self.inventory.action:
            return self.printAvailableActions(domaccess)
        kwds = {}
        for attr in self.inventory.__dict__:
            if attr.startswith('_'): 
                continue
            if attr in self.Inventory.__dict__:
                continue
            kwds[attr] = getattr(self.inventory, attr)
            continue
        print getattr(domaccess, self.inventory.action)(**kwds)
        return


    def printAvailableActions(self, domaccess):
        print "domaccessor %r" % domaccess.name
        import inspect
        for p in dir(domaccess):
            if p.startswith('_'):
                continue
            if p in basenames:
                continue
            m = getattr(domaccess, p)
            if not inspect.ismethod(m) and not inspect.isfunction(m): 
                continue
            sig = getmethodsig(m)
            sig = sig[6:]
            print ' -- %s(%s)' % (p, sig)
            continue
        return


    def __init__(self, name=None):
        if name is None:
            name='doma'
        super(DOMAApp, self).__init__( name)
        return


    def _getPrivateDepositoryLocations(self):
        return ['/tmp/luban-services', '../config', '../content/components']




def getmethodsig(f):
    import inspect
    argspec = inspect.getargspec(f)
    args = argspec.args
    defaults = argspec.defaults
    s = ['self']
    s += ['%s=%s' % (a, d) for a,d in zip(args[1:], defaults or [None for a in args[1:]])]
    if argspec.varargs:
        s.append('*'+argspec.varargs)
    if argspec.keywords:
        s.append('**'+argspec.keywords)
    return ', '.join(s)


def main():
    app = DOMAApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
