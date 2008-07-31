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


    def __init__(self, configurations):
        self.imagepath = configurations['imagepath']
        self.javascriptpath = configurations['javascriptpath']
        
        cgihome = configurations['cgihome']
        from ActionHrefRenderer import ActionHrefRenderer
        self.hrefer = ActionHrefRenderer( cgihome )
        return

    def render(self, treeview):
        return treeview.identify(self)


    def onTreeView(self, treeview):
        # go through the tree and render action_href from action
        hrefer = self.hrefer
        class _:
            def onContainer(self, container):
                self.onElement( container )
                for element in container.children:
                    element.identify(self) # assume the mill knows how to convert action to action href
                    continue
                return
            def onElement(self, element):
                action = element.action
                if action: href = action.identify(hrefer)
                else: href = ''
                element.action_href = href
                return
            onTreeView = onBranch = onContainer
            onLeaf = onElement
            pass

        _().onTreeView( treeview )

        # now render js codes.
        # this weaver makes use of TreeView js @ http://treeview.net/
        #
        imagepath = self.imagepath
        javascriptpath = self.javascriptpath

        prefix = [
            #license requirement
            '<TABLE border=0><TR><TD><FONT size=-2><A style="font-size:7pt;text-decoration:none;color:silver" href="http://www.treemenu.net/" target=_blank>Javascript Tree Menu</A></FONT></TD></TR></TABLE>',
            #
            '<SPAN class=TreeviewSpanArea>',
            '<SCRIPT src="%s/TreeView/ua.js"></SCRIPT>' % javascriptpath,
            '<SCRIPT src="%s/TreeView/ftiens4.js"></SCRIPT>' % javascriptpath,
            ]
        postfix = [
            '</SPAN>'
            ]
        configurations = [
            'USETEXTLINKS = 1',
            'STARTALLOPEN = 0',
            'USEFRAMES = 0',
            'USEICONS = 0',
            'WRAPTEXT = 1',
            'PRESERVESTATE = 1',
            'ICONPATH = "%s/TreeView/"' % imagepath,  #/vnfLJ/images
            ]

        codes = JSCodeRenderer().render( treeview )

        codes = configurations + codes

        codes.append( 'initializeDocument()' )
        
        codes = prefix + ['<script>'] + codes + ['</script>'] + postfix
        return codes




class JSCodeRenderer:

    def render(self, tree):
        self.generate_id = IdGenerator()
        self.codes = []
        tree.identify(self)
        return self.codes


    def onTreeView(self, treeview):
        self._makeBranchNode( treeview )
        self.codes.append( 'foldersTree = aux%d' % treeview.id )

        # prepare to descend
        self.id = treeview.id
        # descend to children
        for child in treeview.children:
            child.identify(self)
            continue

        # back up
        self.id = id
        return


    def onBranch(self, branch):
        #parent's id
        id = self.id

        # js code to create the node
        self._makeBranchNode( branch )
        
        # js code to add node to its parent
        code = 'insFld( aux%d, aux%d )' % (
            id, branch.id )
        self.codes.append( code )

        # prepare to descend
        self.id = branch.id
        # descend to children
        for child in branch.children:
            child.identify(self)
            continue

        # back up
        self.id = id
        return
    

    def onLeaf(self, leaf):
        # parent's id
        parentid = self.id
        
        # js code to create the leaf and add to its parent
        code = 'insDoc(aux%d, gLnk("S", "%s", "%s"))' % (
            parentid, leaf.label, leaf.action_href )
        self.codes.append( code )
        
        return


    def _makeBranchNode(self, branch):
        branch.id = id = self.generate_id()
        code = 'aux%d = gFld("%s", "%s")' % (
            id, branch.label, branch.action_href )
        self.codes.append(code)
        return




class IdGenerator:

    def __init__(self):
        self._id = 0
        return

    def __call__(self):
        ret = self._id
        self._id += 1
        return ret
    

# version
__id__ = "$Id$"

# End of file 
