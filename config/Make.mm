# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = config

PROJ_TESTS = \

PROJ_CLEAN += \
    idd-config.pml \
    idd-session.pml \
    ipa-session.pml \
    remote.pml \


PROJ_LIBRARIES = 

#--------------------------------------------------------------------------
#

all: tidy

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:15 aivazis Exp $

# End of file
