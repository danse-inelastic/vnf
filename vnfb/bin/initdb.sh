#!/usr/bin/env sh

# this script prepares the vnf database to a stage that vnf service
# is usable, and with some example records in the db

# this script is under heavy development


# in the following, each commands initialize some db tables

./initdb.py \
    --tables=users,roles,privileges,user_has_roles,role_has_roles,role_has_privileges

./initdb.py --tables=snsmoderatormcsimulateddata,bvkmodels,instruments,vanadiumplates,servers

./initdb.py --tables=sqe
