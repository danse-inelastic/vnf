#!/usr/bin/env bash
EXPORT_ROOT=/Users/linjiao/dv/tools/pythia-0.8
export PYTHONPATH=$EXPORT_ROOT/modules:$PYTHONPATH
export PATH=$EXPORT_ROOT/bin:/usr/local/bin:$PATH
export LD_LIBRARY_PATH=$EXPORT_ROOT/lib:$LD_LIBRARY_PATH

cd $EXPORT_ROOT/vnf/cgi && ./main.py $@
