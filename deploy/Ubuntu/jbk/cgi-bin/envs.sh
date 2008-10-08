
root=/home/jbk/DANSE/buildInelast/pyre/EXPORT
deps=$root/deps
exportSource=/home/jbk/DANSE/vnf

export PYRE_DIR=$root
export PATH=$root/bin:$deps/bin:$PATH
export LD_LIBRARY_PATH=$root/lib:$deps/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$root/lib:$deps/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$root/modules:$deps/python:$PYTHONPATH

export PYTHONPATH=$exportSource:$PYTHONPATH