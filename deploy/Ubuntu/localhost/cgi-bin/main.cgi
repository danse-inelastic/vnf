#!/usr/bin/env bash
VNFINSTALL=/home/jbk/dv
EXPORT_ROOT=$VNFINSTALL/tools/pythia-0.8
export PATH=$EXPORT_ROOT/bin:$PATH
export PYTHONPATH=$EXPORT_ROOT/modules:$PYTHONPATH
export LD_LIBRARY_PATH=$EXPORT_ROOT/lib:$LD_LIBRARY_PATH
#cd /home/jbk/dv/tools/pythia-0.8/vnf/cgi && python main.py $@
cd $EXPORT_ROOT/vnf/cgi && python main.py $@