# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy
import luban.content as lc


from SingleStructureViewFactory import Factory as base
class Factory(base):

    def create(self):
        view = lc.document(id='atomicstructure-details-view')

        #
        titlebar = lc.splitter(Class='atomicstructure-details-view-title-bar')
        view.add(titlebar)

        # view indicator
        view_indicator = self.createViewIndicator()
        titlebar.section().add(view_indicator)

        # view of pdb content
        id = self.id
        htmldoc = lc.htmldocument(id='pdbview-%s'%id)
        view.add(htmldoc)
        # 
        doma = self.domaccess
        pdbfile = doma.hasPDBfile(id)
        if not pdbfile: 
            raise IOError, "no pdb data file: %s" % id
        # 
        pdbcontent = open(pdbfile).read()
        htmldoc.text = "<pre>" + pdbcontent + "</pre>"
        
        return view


# version
__id__ = "$Id$"

# End of file 
