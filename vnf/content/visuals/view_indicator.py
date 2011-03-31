# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import luban.content as lc

def visual_step(path):
    # path is a list of (label, action) and one label as the last item

    doc = lc.document(id='view-indicator')

    doc1 = doc
    for (label, action) in path[:-1]:
        doc1.add(lc.link(label=label, onclick=action))
        doc1.paragraph(text=['/ '], Class='splitter')
        doc1 = doc1.document()
        continue

    last = path[-1]
    if isinstance(last, basestring):
        doc1.paragraph(text=path[-1])
    else:
        label, action = last
        doc1.add(lc.link(label=label, onclick=action))
    
    return doc

def visual_inline(path):
    # path is a list of (label, action) and one label as the last item

    doc = lc.document(id='view-indicator')

    doc1 = doc
    for (label, action) in path[:-1]:
        doc1.add(lc.link(label=label, onclick=action))
        doc1.paragraph(text=['/ '], Class='splitter')
        continue

    last = path[-1]
    if isinstance(last, basestring):
        doc1.paragraph(text=path[-1])
    else:
        label, action = last
        doc1.add(lc.link(label=label, onclick=action))

    return doc


def visual(path):
    return visual_inline(path)


# version
__id__ = "$Id$"

# End of file 
