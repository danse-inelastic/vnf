# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def subclassOf(classes):
    for i, C in enumerate(classes): exec 'C%d=C' % i in locals()
    code = 'class N(%s): pass' % ', '.join([ 'C%d' % i for i in range(len(classes)) ])
    exec code in locals()
    return N


def test():
    class A1:
        def a1(self): print 'a1'
    class A2: 
        def a2(self): print 'a2'
    N = subclassOf([A1,A2])
    N().a1(); N().a2()
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
