#!/usr/bin/env sh
ipad.py --home=../config --stop
spawn-daemon.py  -cmd='./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute' -home=.  -stop
spawn-daemon.py  -cmd='./timer.py --command="./establish_ssh_tunnels.py" -interval=60*minute' -home=. -stop
