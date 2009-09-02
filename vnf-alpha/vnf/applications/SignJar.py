#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class SignJar(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        keyalias = pyre.inventory.str('keyalias')
        keystore = pyre.inventory.str('keystore')
        storepassword = pyre.inventory.str('storepassword')
        keypassword = pyre.inventory.str('keypassword')
        jar = pyre.inventory.str('jar')
        pass # end of Inventory
        

    def main(self):
        from vnf.utils.spawn import spawn
        cmd = 'jarsigner -keystore %(keystore)s -storepass %(storepassword)s -keypass %(keypassword)s %(jar)s %(keyalias)s' % self.__dict__
        ret, out, err  = spawn(cmd)
        if ret:
            raise RuntimeError, "Command %r failed. \n Out: %s\n Error: %s\n" % (
                cmd, out, err)
        return


    def __init__(self, name='signJar'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self.keyalias = self.inventory.keyalias
        self.keystore = self.inventory.keystore
        self.storepassword = self.inventory.storepassword
        self.keypassword = self.inventory.keypassword
        self.jar = self.inventory.jar
        return


    def _init(self):
        base._init(self)
        if self._showHelpOnly: return

        import os
        if not os.path.exists(self.keystore):
            raise RuntimeError, "key store %r does not exist" % self.keystore

        if not os.path.exists(self.jar):
            raise RuntimeError, "Jar %r does not exist" % self.jar

        return



# version
__id__ = "$Id$"

# End of file 
