#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main():


    from vnf.applications.ApproveUser import ApproveUser as base


    class App(base):


        def _getPrivateDepositoryLocations(self):
            from os.path import join
            root = '..'
            content = join(root, 'content')
            config = join(root, 'config')

            from vnf.depositories import depositories
            
            return depositories(content)+[config]


    app = App()
    app.run()

    # now need to send HUP signal to ipad so that the new user table is used
    ipapid = open('../config/ipa.pid').read()
    ipapid = eval(ipapid)
    import os
    os.kill( ipapid, 1 )
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
