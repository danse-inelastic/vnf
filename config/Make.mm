# -*- Makefile -*-

PROJECT = vnfb
PACKAGE = config

#--------------------------------------------------------------------------
#

all: export-data-files init-data-files init-guid-dat
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_DATAFILES = \
	SimpleHttpServer.pml \
	activateserver.pml \
	addbvkmodelstodb.pml \
	app-extension.odb \
	approveUser.pml \
	itaskapp.pml \
	checkservers.pml \
	createdataobject.pml \
	clerk.odb \
	createInstruments.pml \
	doma.pml \
	getuserlist.pml \
	guidfromidddaemon.odb \
	idd-pickler.odb \
	initdb.pml \
	ipa.pml \
	itask-manager.odb \
	librarian.pml \
	listservers.pml \
	main.pml \
	retrieveresults.pml \
	updatejobstatus.pml \
	usersFromDB.odb \
	web-weaver-library.pml \


INIT_DATAFILES = \
	atomicstructure-cod.pml \
	clerk.pml \
	journal.pml \
	postman.pml \
	ssher.pml \
	web-weaver.pml \


#CP_F = rsync -r --copy-unsafe-links

CP_F = cp -f
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-data-files::
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
	} done


# copy the data files over only if they do not exist
init-data-files:
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(INIT_DATAFILES); do { \
            if [ -e $$x -a ! -e $(EXPORT_DATA_PATH)/$$x ]; then { \
	        $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
            } fi; \
        } done


# init guid.dat
GUID_DAT = guid.dat
# HTTP_SERVER_USER = www-data
# HTTP_SERVER_GROUP = www-data
init-guid-dat:
	if [ ! -e $(EXPORT_DATA_PATH)/$(GUID_DAT) ]; then { \
	  $(CP_F) $(GUID_DAT) $(EXPORT_DATA_PATH)/ ; \
	  sudo chown $(HTTP_SERVER_USER) $(EXPORT_DATA_PATH)/$(GUID_DAT) ; \
	  sudo chgrp $(HTTP_SERVER_GROUP) $(EXPORT_DATA_PATH)/$(GUID_DAT) ; \
	} fi;
