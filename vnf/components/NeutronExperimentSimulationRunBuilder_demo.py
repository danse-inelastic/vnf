#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Builder:


    shscriptname = 'run.sh'


    def __init__(self, path):
        self.path = path
        return
    

    def render(self, experiment):
        #copy files directory from template
        template = 'content/jobs/SQEtemplate'
        for item in os.listdir( template ):
            source = os.path.join( template, item )
            #skip directories
            if os.path.isdir( source ): continue
            shutil.copy( source, self.path )
            continue
        experiment.expected_results = [ 'Eresolution.png', 'IQE.png' ]
        return
        
    pass # end of Builder


import os, shutil


# version
__id__ = "$Id$"

# End of file 
