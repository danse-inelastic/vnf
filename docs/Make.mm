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


# data dirs containing images, videos etc that will be exported to 
# sphinx export directory
EXPORT_DATADIRS = \
	_static \
	shots \


# vars for sphinx build command 
# build cmd for sphinx
SPHINX_BUILD   = sphinx-build
# additional options for sphinx command
SPHINX_OPTS    =
# paper type: a4 or letter
PAPER         =                         


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

RSYNC_A = rsync -a

# tmp dir for this package
PACKAGE_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)


# to build up the sphinx cmd
SPHINX_BUILDDIR = $(EXPORT_DOCDIR)
SPHINX_BUILDDIR_HTML = $(SPHINX_BUILDDIR)
SPHINX_BUILDDIR_DOCTREES = $(PACKAGE_TMPDIR)/doctrees
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALL_SPHINX_OPTS   = -d $(SPHINX_BUILDDIR_DOCTREES) $(PAPEROPT_$(PAPER)) $(SPHINX_OPTS) .


sphinx-build: $(EXPORT_DOCDIR)
	mkdir -p $(SPHINX_BUILDDIR_HTML)
	mkdir -p $(SPHINX_BUILDDIR_DOCTREES)
	$(SPHINX_BUILD) -b html $(ALL_SPHINX_OPTS) $(SPHINX_BUILDDIR_HTML)
	@echo
	@echo "Build finished. The HTML pages are in $(SPHINX_BUILDDIR_HTML)."


export-data: $(EXPORT_DATADIRS) $(SPHINX_BUILDDIR_HTML)
	for x in $(EXPORT_DATADIRS); do { \
	  $(RSYNC_A) $$x/ $(SPHINX_BUILDDIR_HTML)/$$x/; \
	} done


# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
