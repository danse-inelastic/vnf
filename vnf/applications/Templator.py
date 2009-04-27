# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base


class Templator(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="test")
        name.meta['tip'] = 'the name of the application to generate'

        filename = pyre.inventory.str('filename', default='')
        ext = pyre.inventory.str('ext', default='odb')

        import vnf.inventory
        template = vnf.inventory.template('template', default='actor')

        language = pyre.inventory.str('language', default='python')
        

    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        name = self.inventory.name
        ext = self.inventory.ext
        filename = self.inventory.filename
        if not filename:
            filename = self.inventory.name + '.' + ext
        print "creating '%s' in '%s'" % (name, filename)

        stream = file(filename, "w")
        for line in self.weaver.document():
            print >> stream, line
        stream.close()
        
        return


    def __init__(self):
        super(Templator, self).__init__("templator")
        return


    def _init(self):
        super(Templator, self)._init()
        self.weaver.language = self.inventory.language
        return


    def _template(self):
        name = self.inventory.name
        template = self.inventory.template
        text = template.create(name=name)
        return text



# version
__id__ = "$Id$"

# End of file
