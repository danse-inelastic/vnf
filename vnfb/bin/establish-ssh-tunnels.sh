./establish-ssh-tunnels.py
spawn-daemon.py --cmd="timer.py --command='./establish-ssh-tunnels.py' --interval=1*hour" --home=$PWD
