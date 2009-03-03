

def forceIpadToReload():
    # now need to send HUP signal to ipad so that it will reload the user table
    # this assumes that ipad's pid is written in the pid file
    PIDFILE = '../config/ipa.pid'
    ipapid = open(PIDFILE).read()
    ipapid = eval(ipapid)
    import os
    os.kill( ipapid, 1 )
    return


def askIpadToReload(director):
    sentry = director.sentry
    ipa = sentry.ipa
    ipa.request(command='onReload')
    return
