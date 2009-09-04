
PROJECT = vnf-migrational

# directory structure

RECURSE_DIRS = \
	vnf-alpha \
	vnfb \


#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

