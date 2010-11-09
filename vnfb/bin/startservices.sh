#!/usr/bin/env sh
./run-daemons.sh
./cron-daemons.sh

./run-monitors.sh
./cron-monitors.sh

#
./establish_ssh_tunnels.py
spawn-daemon.py  -cmd='./timer.py --command="./establish_ssh_tunnels.py" -interval=60*minute' -home=. 
