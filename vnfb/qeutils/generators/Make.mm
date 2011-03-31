# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = qeutils/generators


#--------------------------------------------------------------------------
#

EXPORT_PYTHON_MODULES = \
    bandsgenerator.py \
    cpgenerator.py \
    dosgenerator.py \
    dynmatgenerator.py \
    __init__.py \
    matdyngenerator.py \
    phgenerator.py \
    plotbandgenerator.py \
    pwgenerator.py \
    q2rgenerator.py \
    emgenerator.py \
    imgenerator.py \
    irgenerator.py \
    qugenerator.py \
    dygenerator.py \
    thgenerator.py \
    trgenerator.py \


BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id$

# End of file