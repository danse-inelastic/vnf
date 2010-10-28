# 10/18/10
# Charles O. Goddard

from fetchd.public import Message, request

if __name__=='__main__':
    import os
    import sys
    
    # Unix double-fork magic.
    pid = os.fork()
    if pid > 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    pid = os.fork()
    if pid > 0:
        os._exit(0)
    sys.stdin = open('/dev/null', 'r')
    sys.stdout = open('/dev/null', 'w')
    sys.stderr = open('/dev/null', 'w')
    
    from fetchd.core import Core
    c = Core()
    try:
        while c.think():
            pass
    except:
        print 'stopping'
        os.unlink('/tmp/cg_fetchd')
