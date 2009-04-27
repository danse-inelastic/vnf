#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao  Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main():


    from vnf.applications.Templator import Templator as base


    class App(base):

        def _getPrivateDepositoryLocations(self):
            from os.path import join
            import os
            export_root = os.environ['EXPORT_ROOT']
            root = os.path.join(export_root, 'vnf')
            content = join(root, 'content')
            config = join(root, 'config')

            from vnf.depositories import depositories

            return depositories(content)+[config]

        pass # end of App


    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
