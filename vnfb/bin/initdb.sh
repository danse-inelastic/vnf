#!/usr/bin/env sh

# this script prepares the vnf database to a stage that vnf service
# is usable, and with some example records in the db

# this script is under heavy development


# in the following, each commands initialize some db tables

# create tables that are still in vnf-alpha
./initdb.py  --init-tables \
    --tables=users

# add bvk models
./addbvkmodelstodb.py 

# add instruments
./createInstruments.py

# add a vanadium plate
./createdataobject.py --type=neutron_experiment_simulations.neutron_components.VanadiumPlate.VanadiumPlate 
