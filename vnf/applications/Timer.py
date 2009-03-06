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


from pyre.applications.Script import Script as base


class Timer(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        from pyre.units.time import second
        interval = pyre.inventory.dimensional("interval", default=1.0*second)
        command = pyre.inventory.str('command')


    def main(self, *args, **kwds):
        import threading, time
        
        print "creating event and thread"
        ev = threading.Event()
        t1 = threading.Thread(target=self._repeat, args=(ev, self.interval, self._run))
        
        print "starting thread"
        t1.start()
        
        try:
            while 1: continue
        except KeyboardInterrupt :
            pass
        
        print "setting event to signal the thread to finish"
        ev.set()
        
        print "waiting for thread to finish"
        t1.join()
        
        print "quit"
        return
        

    def _repeat(self, event, every, action):
        while True:
            event.wait(every)
            if event.isSet():
                break
            action()
        return
    

    def _run(self):
        command = self.command
        import os
        os.system(command)
        return


    def __init__(self, name=None):
        if name is None:
            name = "timer"

        super(Timer, self).__init__(name)
        return


    def _configure(self):
        super(Timer, self)._configure()
        self.command = self.inventory.command
        self.interval = self.inventory.interval.value
        return


    def _init(self):
        super(Timer, self)._init()
        return
    


# version
__id__ = "$Id$"

# End of file 
