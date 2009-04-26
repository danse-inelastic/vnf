#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnf.weaver.JnlpMill import Renderer as JnlpMill

import unittest

from unittest import TestCase
class TestCase(TestCase):


    def test1(self):
        'Jnlp weaver'
        jnlp = _jnlp(
            codebase = 'http://vnf.caltech.edu',
            icon = 'icons/theicon.png',
            description = ['Description of the jnlp'],
            jnlpurl = 'jars/thejar.jnlp',
            jarurl = 'jars/thejar.jar',
            main_class = 'mainclass',
            )
        mill = JnlpMill()
        mill.options = _options()
        texts = mill.render(jnlp)
        print '\n'.join(texts)
        return
    
    
    pass # end of TestCase


def _jnlp(**kwds):
    from vnf.weaver.Jnlp import Jnlp, Information, Security, J2SE, Jar, Extension
    title = '3D view'
    vendor = 'DANSE'
    homepage = 'http://vnf.caltech.edu'
    descriptions = {'': kwds['description']}
    icons = {'': kwds['icon']}
    options = ['offline-allowed']
    info = Information(title, vendor, homepage, descriptions, icons, options)
    
    security = Security()

    j2se = J2SE()

    jarhref = kwds['jarurl']
    jar = Jar(jarhref, main='true')

    extension = Extension('http://download.java.net/media/java3d/webstart/release/java3d-latest.jnlp')

    resources = [
        j2se,
        jar,
        extension,
        ]

    codebase = kwds['codebase']
    jnlpurl = kwds['jnlpurl']
    main_class = kwds['main_class']
    jnlp = Jnlp(codebase, jnlpurl, info, security, resources, main_class)
    return jnlp


def _options():
    class _:
        author = 'author'
        organization = 'organization'
        copyright = 'copyright'

        bannerWidth = 78
        bannerCharacter = '~'

        creator = 'creator'
        timestamp = True

        lastLine = 'End of file'
        copyrightLine = '(C) %s All rights reserved'
        licenseText = ['{LicenseText}']

        timestampLine = " Generated automatically by %s on %s"
        versionId = '$Id$'
    return _

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
