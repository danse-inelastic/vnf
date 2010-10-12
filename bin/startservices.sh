#!/usr/bin/env sh
ipad.py --config=/tmp/luban-services,../config --- --home=../config
spawn-daemon.py  -cmd='./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute' -home=. 
./establish_ssh_tunnels.py
spawn-daemon.py  -cmd='./timer.py --command="./establish_ssh_tunnels.py" -interval=60*minute' -home=. 
