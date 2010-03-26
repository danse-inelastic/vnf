
PROJECT = vnfb
PACKAGE = config

#--------------------------------------------------------------------------
#

all: export-data-files
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
	addbvkmodelstodb.pml \
	app-extension.odb \
	itaskapp.pml \
	createdataobject.pml \
	clerk.odb \
	createInstruments.pml \
	getuserlist.pml \
	guidfromidddaemon.odb \
	idd-pickler.odb \
	initdb.pml \
	ipa.pml \
	itask-manager.odb \
	journal.pml \
	librarian.pml \
	main.pml \
	postman.pml \
	retrieveresults.pml \
	updatejobstatus.pml \
	usersFromDB.odb \
	web-weaver-library.pml \

#	widget.lib
#	web-weaver.pml \
# 	clerk.pml \
# 	ssher.pml \

#CP_F = rsync -r --copy-unsafe-links

CP_F = cp -f
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-data-files::
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
	} done

