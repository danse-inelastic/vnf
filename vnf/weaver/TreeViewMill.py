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


class TreeViewMill:


    def onTreeView(self, treeview):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']

        # csscode
        csscode = []
        csss = [
            'jquery.treeview.css',
            ]
        for css in csss:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home,css) )

        # now render the tree as <ul>s
        from ActionHrefRenderer import ActionHrefRenderer
        hrefer = ActionHrefRenderer( cgihome )

        htmlcode = []
        htmlcode.append('<ul id="%s" class="filetree">' % _id(treeview))

        theme = 'default'
        styles = styles_dict[theme]
        htmlcode += HtmlMill(hrefer, styles).render(treeview)

        htmlcode.append('</ul>')
        return csscode + htmlcode


styles_dict  = {
    'default': {'container': '',
                'element': '',
                },
    'browser': {'container': 'folder',
                'element': 'file',
                },
    }

class HtmlMill:

    def __init__(self, hrefer, styles):
        self.hrefer = hrefer

        self.styles = styles
        return

    def render(self, treeview):
        self._rep = []
        treeview.identify(self)
        return self._rep


    def onContainer(self, container):
        styles = self.styles
        self.onElement(container, klass=styles['container'])
        
        self._rep.append('<ul>')
        for element in container.children:
            element.identify(self)
            continue
        self._rep.append('</ul>')
        
        return

    
    def onElement(self, element, klass=None):
        styles = self.styles
        if not klass: klass = styles['element']
        
        action = element.action
        if action: href = action.identify(self.hrefer)
        else: href = ''
        self._rep.append(self.li(klass, element.label, href))
        return


    def li(self, klass, label, href):
        s = '<li><span class="%s">' % klass
        if href:
            s+= '<a href="%s">' % href
        s += label
        if href:
            s+= '</a>'
        s += '</span>'
        return s
    
    onTreeView = onBranch = onContainer
    onLeaf = onElement
    pass



class JSMill:

    def onTreeView(self, treeview):
        includes = [
            'jquery/jquery.js',
            'jquery/jquery.cookie.js',
            'jquery/treeview/jquery.treeview.js',
            ]
        self.include(scripts=includes)

        id = _id(treeview);
        self.writemain('$("#%s").treeview();' % id);
        
        return
        


def _id(widget):
    return id(widget)


# version
__id__ = "$Id$"

# End of file 
