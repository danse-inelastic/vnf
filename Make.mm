# -*- Makefile -*-

PROJECT = vnfb

# directory structure

RECURSE_DIRS = \
	bin \
	cgi-bin \
	vnfb \
	dds \
	log \
	content \
	html \
	config \
	tests \


#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

