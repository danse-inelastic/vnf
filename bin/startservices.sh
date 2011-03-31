#!/usr/bin/env sh

# script to start various vnf services
# should be run as a vnf system administrator
# requirements of vnf sys admin:
#  1. has a ssh key accepted by computing servers 
#  2. has set up a ssh agent and the ssh key in (1) is added
# 

./run-daemons.sh
./cron-daemons.sh

./run-monitors.sh
./cron-monitors.sh

#
./establish_ssh_tunnels.py
spawn-daemon.py  -cmd='./timer.py --command="./establish_ssh_tunnels.py" -interval=60*minute' -home=. 
