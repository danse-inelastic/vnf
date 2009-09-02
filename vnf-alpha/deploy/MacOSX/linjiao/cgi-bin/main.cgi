#!/usr/bin/env bash
EXPORT_ROOT=/Users/linjiao/dv/tools/pythia-0.8
export PYTHONPATH=$EXPORT_ROOT/packages:$PYTHONPATH
export PATH=$EXPORT_ROOT/bin:/usr/local/bin:$PATH
export DYLD_LIBRARY_PATH=$EXPORT_ROOT/lib:$DYLD_LIBRARY_PATH

#source /Users/linjiao/.hdf5-env
#source /Users/linjiao/.jython2.2.1-env

cd $EXPORT_ROOT/vnf/cgi && ./main.py $@
