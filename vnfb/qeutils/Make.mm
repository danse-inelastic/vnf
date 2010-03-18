# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnfb
PACKAGE = qeutils


# directory structure

BUILD_DIRS = \
        qecalcutils \
        qeparser \
        results \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
        qetaskcell.py \
        qetaskinfo.py \
        qetasks.py \
        qeconst.py \
        qegrid.py \
        qeinput.py \
        qeparams.py \
        qerecords.py \
        qeresults.py \
        qescheduler.py \
        qeserver.py \
        qestatus.py \
        qeutils.py \

#include doxygen/default.def

export:: export-package-python-modules 


#docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
