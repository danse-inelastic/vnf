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

#--------------------------------------------------------------------------
#

all: export-config-files
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


EXPORT_DATAFILES = \
	clerk.pml \
	idd-config.pml \
	idd-harness.pml \
	idd-pickler.odb \
	idd.pml \
	idd-session.pml \
	initdb.pml \
	ipa-harness.pml \
	ipa-pickler.odb \
	ipa.pml \
	ipa-session.pml \
	journald-harness.pml \
	journal.pml \
	remote.pml \
	ssher.pml \
	userdb.md5 \
	weaver.pml \
	

CP_F = cp -f
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-config-files:: 
	mkdir -p $(EXPORT_DATA_PATH); \
	$(CP_F) main.trueblue.pml $(EXPORT_DATA_PATH)/main.pml
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
        } done


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
