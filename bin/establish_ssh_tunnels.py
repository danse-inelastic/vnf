#!/usr/bin/env python


# establish tunnels

tunnels = [
    # 50022 -- octopod:22
    ('octopod.danse.us:22', 50022, 'danse-vnf-admin@foxtrot.danse.us'),
    #('octopod.danse.us:22', 50022, 'upgrayedd.danse.us'),
    # 55432 -- octopod 5432
    # ('localhost:5432', 55432, 'localhost:50022'),
    ]


import os
def connect(tunnel):
    remote, localport, thru = tunnel
    cmd = 'sshtunnel.py -remote="%s" -localport=%s -through="%s"' % (
        remote, localport, thru)
    os.system(cmd)
    return


def main():
    for tunnel in tunnels:
        connect(tunnel)
    return


if __name__ == '__main__': main()
