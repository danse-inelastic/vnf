#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Contains little but useful itils!
"""

def parseFile(filename):
    e = []
    x = []
    y = []
    z = []
    f = open(filename,  "r")
    line = f.readline() # Skip the first line with header
    line = f.readline()
    while line:
        list = line.split()

        #Convert strings to float and append to the list
        e.append(float(list[0]))
        x.append(float(list[1]))
        y.append(float(list[2]))
        z.append(float(list[3]))
        line = f.readline()
    f.close()
    return (e,  x,  y,  z)

def parsePHFile(filename):
    e = []
    x = []
    f = open(filename,  "r")
    line = f.readline()
    while line:
        list = line.split()
        #print list
        e.append(float(list[0]))
        x.append(float(list[1]))
        line = f.readline()
    f.close()
    return (e,  x)


def newid(director):
    "Id generator "
    id  = ''
    if director:
        id = director.getGUID()     # Changed from idd.token().locator

    return id


def timestamp():
    """Returns time stamp"""
    import time
    return int(time.time())

"""Replaces ternary operator in C: '?:' (e.g. a ? a: 4) """
ifelse  = lambda a,b,c: (b,c)[not a]

"""
Sets attribute 'name' of object 'obj' from params dictionary
Used mostly on database classes (vini.dom)
"""
setname = lambda params, obj, name: ifelse(params.has_key(name), params.get(name), getattr(obj, name))


def stamp2date(stamp):
    """Converts stamp to date"""
    # TODO: Change to: Month Day, Hours:Minutes:Seconds
    # Check is stamp is
    import time
    import re
    p   = re.compile("[\d.]+")
    m   = p.match(str(stamp))
    from datetime import date
    if m:
        s   = time.strptime(date.fromtimestamp(float(stamp)).ctime())
        return str(time.strftime("%Y-%m-%d", s))     # Format: Year-Month-Day

    return ""


def makedirs(path):
    """Recursively creates directory specified by path"""
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def writefile(filename, content):
    open(filename, 'w').write(content)


def packname(id, name):
    """Packs name by appending name to id.
    E.g.
        id   = "3YEQ8PNV"
        name = "ni.scf.in"
    =>  3YEQ8PNVni.scf.in
    """
    return "%s%s" % (id, name)

def unpackname(string, id):
    """
    Unpacks string: returns tupple (id, name) by trancating id from string
    """
    parts   = string.split("id")
    
    # raise error if id is not in string
    assert len(parts) == 2  # breaks into two parts
    assert parts[0] == ''
    name    = parts[1]

    return (id, name)


def testStamp():
    import time
    print stamp2date(time.time())

if __name__ == "__main__":
    testStamp()

__date__ = "$Jul 30, 2009 12:08:31 PM$"


