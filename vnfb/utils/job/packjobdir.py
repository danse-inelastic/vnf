

PTRFILEEXT = '.__dir__pack__ptr__'
PACKINGINPROCESS = 'in progress'


import os, tempfile, shutil
temproot = os.path.join('..', 'content', 'data', 'tmp')


def downloadurl(job, director):
    ptr = readPtr(job, director)
    return os.path.join('tmp', ptr)


def ptrFilePath(job, director):
    return '.'.join( [director.dds.abspath(job), PTRFILEEXT] )


def packingIsUpToDate(job, director):
    path = ptrFilePath(job, director)
    if not os.path.exists(path): return
    packtime = os.path.getmtime(path)

    server = director.clerk.dereference(job.server)
    mtime = director.dds.getmtime(job, server=server)
    return packtime > mtime


def removeOldTarBall(job, director):
    path = ptrFilePath(job, director)
    if not os.path.exists(path): return

    oldptr = open(path).read()
    if not oldptr: return
    if oldptr == PACKINGINPROCESS: return
    oldtarballpath = os.path.join(temproot, oldptr)
    oldtarballparentdir = os.path.dirname(oldtarballpath)

    if os.path.exists(oldtarballparentdir):
        shutil.rmtree(oldtarballparentdir)
    return


def establishPtr(job, ptr, director):
    path = ptrFilePath(job, director)
    f = open(path, 'w')
    f.write(ptr)
    return


def readPtr(job, director):
    path = ptrFilePath(job, director)
    f = open(path, 'r')
    return f.read()


def declarePackingInProcess(job, director):
    path = ptrFilePath(job, director)

    f = open(path, 'w')
    f.write(PACKINGINPROCESS)
    return


