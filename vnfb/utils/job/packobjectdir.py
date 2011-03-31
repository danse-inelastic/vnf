

PTRFILEEXT = '.__dir__pack__ptr__'
PACKINGINPROCESS = 'in progress'


import os, shutil
temproot = os.path.join('..', 'content', 'data', 'tmp')


def downloadurl(object, director):
    ptr = readObject(object, director)
    return os.path.join('tmp', ptr)

def readObject(object, director):
    path = objectFilePath(object, director)
    f = open(path, 'r')
    return f.read()

def objectFilePath(object, director):
    return director.dds.abspath(object)

#def downloadurl(object, director):
#    ptr = readPtr(object, director)
#    return os.path.join('tmp', ptr)

def ptrFilePath(object, director):
    return '.'.join( [director.dds.abspath(object), PTRFILEEXT] )


def packingIsUpToDate(object, director):
    path = ptrFilePath(object, director)
    if not os.path.exists(path): return
    packtime = os.path.getmtime(path)

    server = director.clerk.dereference(object.server)
    mtime = director.dds.getmtime(object, server=server)
    return packtime > mtime


def removeOldTarBall(object, director):
    path = ptrFilePath(object, director)
    if not os.path.exists(path): return

    oldptr = open(path).read()
    if not oldptr: return
    if oldptr == PACKINGINPROCESS: return
    oldtarballpath = os.path.join(temproot, oldptr)
    oldtarballparentdir = os.path.dirname(oldtarballpath)

    if os.path.exists(oldtarballparentdir):
        shutil.rmtree(oldtarballparentdir)
    return


def establishPtr(object, ptr, director):
    path = ptrFilePath(object, director)
    f = open(path, 'w')
    f.write(ptr)
    return


def readPtr(object, director):
    path = ptrFilePath(object, director)
    f = open(path, 'r')
    return f.read()


def declarePackingInProcess(object, director):
    path = ptrFilePath(object, director)

    f = open(path, 'w')
    f.write(PACKINGINPROCESS)
    return


