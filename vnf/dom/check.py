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


import journal
info = journal.info('vnf.dom.check')


def issane(table, db):
    '''check if a table exists in a db'''
    row = table()
    row.id = 'strange_id_for_test'

    try:
        db.insertRow(row)
    except db.ProgrammingError, e:
        msg = 'table %s in db %s is no good: %s' % (table.name, db, e)
        info.log(msg)
        return False
    db.deleteRow(table, where="id='%s'" % row.id)
    return True


import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    prefix = 'strange_id_for_test'
    return prefix + ''.join(random.sample(alphabet, 6))

# version
__id__ = "$Id$"

# End of file 
