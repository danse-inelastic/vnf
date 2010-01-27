# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2008  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = sphinx


RECURSE_DIRS = \


#--------------------------------------------------------------------------
#

all: docs
	BLD_ACTION="all" $(MM) recurse

PROJ_CLEAN = \
	_build/* \

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

docs: export-data sphinx-build 


include std-docs.def

SPHINX_BUILD_TMP = _build/html

RSYNC_A = rsync -a
sphinx-build: Makefile $(EXPORT_DOCDIR)
	make html
	$(RSYNC_A) $(SPHINX_BUILD_TMP)/ $(EXPORT_DOCDIR)/


EXPORT_DATADIRS = \
	_static \
	shots \


$(SPHINX_BUILD_TMP):
	mkdir -p $(SPHINX_BUILD_TMP)


export-data: $(EXPORT_DATADIRS) $(SPHINX_BUILD_TMP)
	for x in $(EXPORT_DATADIRS); do { \
	  $(RSYNC_A) $$x/ $(SPHINX_BUILD_TMP)/$$x/; \
	} done

# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
