#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main():


    from vnf.applications.UpdateJobStatus import UpdateJobStatus


    class App(UpdateJobStatus):


        def _getPrivateDepositoryLocations(self):
            from os.path import join
            root = '..'
            content = join(root, 'content')
            config = join(root, 'config')
            
            from vnf.depositories import depositories
            
            return depositories(content)+[config]


    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: ipad.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
