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


    def __eq__(self, rhs):
        return self.address == rhs.address and self.port == rhs.port and self.username == rhs.username
    


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
        ssher.copyfile(
            Server(None, None, None), 'testfile',
            Server('login.cacr.caltech.edu', None, 'linjiao'), '/tmp',
            )
        ssher.copyfile(
            Server('login.cacr.caltech.edu', None, 'linjiao'), '/tmp/testfile',
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/ssher1.py',
            )
        
        ssher.pushdir( 'testdir',
                       Server('login.cacr.caltech.edu', None, 'linjiao'),
                       '/tmp')
        
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
    import journal
    journal.info('ssher').activate()
    # invoke the application shell
    main()


# version
__id__ = "$Id: db.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
