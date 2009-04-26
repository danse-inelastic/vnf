#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Jnlp:

    specification = "1.0+"

    def __init__(self, codebase, href, information, security, resources, main_class):
        self.codebase = codebase
        self.href = href
        self.information = information
        self.security = security
        self.resources = resources
        self.main_class = main_class
        return

    def identify(self, visitor): return visitor.onJnlp(self)


class Information:

    def __init__(self, title, vendor, homepage, descriptions, icons, options={}):
        self.title = title
        self.vendor = vendor
        self.homepage = homepage
        self.descriptions = descriptions
        self.icons = icons
        self.options = options
        return

    def identify(self, visitor): return visitor.onInformation(self)
    

class Security:

    def identify(self, visitor): return visitor.onSecurity(self)

    pass # end of Security



class ResourceBase:

    pass # end of ResourceBase


class J2SE(ResourceBase):

    version = '1.5+'

    def identify(self, visitor): return visitor.onJ2SE(self)
    

class Jar(ResourceBase):

    def __init__(self, href, main):
        self.href = href
        self.main = main
        return

    def identify(self, visitor): return visitor.onJar(self)
    

class Extension(ResourceBase):

    def __init__(self, href):
        self.href = href
        return

    def identify(self, visitor): return visitor.onExtension(self)


__id__ = "$Id"

# End of file 
