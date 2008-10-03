# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class DbAddressResolver:
    
    def resolve(self, address):
        tmp = address.split('@')
        if len(tmp)==1:
            svr = tmp[0]
            up = ''
        elif len(tmp)==2:
            up,svr = tmp
        else:
            raise ValueError, 'Invalid db address: %r' % address

        host,port,database = self._resolve_svr(svr)
        user, pw = self._resolve_up(up)
        ret = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            }
        if pw: ret['password'] = pw
        return ret
    

    def _resolve_up(self, up):
        separator = ':'
        tmp = up.split(separator)
        if len(tmp) == 1:
            user = tmp[0]
            pw = None
        elif len(tmp) == 2:
            user, pw = tmp
        else:
            raise ValueError, 'Invalid user, password: %r' % up
        return user, pw
    

    def _resolve_svr(self, svr):
        separator = ':'
        
        if svr.find(separator) == -1:
            return 'localhost', 5432, svr
        splits = svr.split(separator)
        if len(splits)==2:
            host, database = splits
            return host, 5432, database
        elif len(splits)==3:
            host, port, database = splits
            return host, port, database
        raise ValueError, 'Invalid db svr: %r' % (svr,)
    


# version
__id__ = "$Id$"

# End of file 
