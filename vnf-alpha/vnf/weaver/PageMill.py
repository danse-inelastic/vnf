#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from opal.weaver.PageMill import PageMill as base


class PageMill(base):

    
    def onPage(self, page):
        #
        head = page._head

        # render javascripts
        includes, scripts = self.javascriptWeaver.render(page)

        # add includes to head
        for inc in includes:
            head.script(src=inc)

        # add scripts to head
        for script in scripts:
            s = head.script()
            s.script = script
            
        return base.onPage(self, page)


    def __init__(self, configurations):
        base.__init__(self)
        
        from JavaScriptWeaver import JavaScriptWeaver
        self.javascriptWeaver = JavaScriptWeaver(configurations)

        tagger = self.bodyMill.tagger
        from StructuralMill import StructuralMill
        self.bodyMill.structuralMill = StructuralMill(tagger, configurations)
        self.bodyMill.structuralMill.master = self
        return
    


# version
__id__ = "$Id$"

# End of file 
