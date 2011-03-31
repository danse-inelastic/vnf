# -*- Makefile -*-

PROJECT = vnf

# directory structure

RECURSE_DIRS = \
	bin \
	cgi-bin \
	vnf \
	dds \
	log \
	content \
	html \
	config \
	tests \
	docs \


#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

