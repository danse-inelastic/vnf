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



# Descriptor of a column
class Column:

    def __init__(self, id='', measure=None, **kwds):
        self.id = id
        self.measure = measure
        if kwds.has_key('label'):
            label = kwds['label']
            del kwds['label']
        else:
            label = measure
        self.label = label
        
        self.options = kwds
        return


def test():
    Column(measure='a')
    return

def main():
    test()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
