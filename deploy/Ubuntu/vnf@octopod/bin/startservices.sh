#!/usr/bin/env sh
./journald.py
./idd.py
./ipad.py
./updatejobstatus.sh


echo
echo You will also need to make following ssh tunnels
echo  $ ssh -L 50022:octopod:22 login.cacr.caltech.edu

