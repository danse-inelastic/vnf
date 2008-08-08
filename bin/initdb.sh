#!/usr/bin/env bash

#use pgsql command to create database
#what if we use different sql backend?
dropdb vnf
createdb vnf

#create tables in the db
./initdb.py