#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script


class Server:

    def __init__(self, address, port, username):
        self.address = address
        self.port = port
        self.username = username
        return
    


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory
        import vnf.components
        ssher = pyre.inventory.facility('ssher', factory=vnf.components.ssher)
        

    def main(self, *args, **kwds):
        ssher = self.ssher
        ssher.copyfile(
            Server(None, None, None), 'testfile',
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp',
            )
        ssher.copyfile(
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/testfile',
            Server(None, None, None), 'testfile',
            )
        ssher.copyfile(
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/testfile',
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/ssher1.py',
            )
        return


    def __init__(self):
        Script.__init__(self, 'test-ssher')
        return


    def _configure(self):
        Script._configure(self)
        self.ssher = self.inventory.ssher
        return


def main():
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: db.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
