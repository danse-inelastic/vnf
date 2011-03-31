#!/usr/bin/python
# 9/30/10

import socket
import cPickle
import tempfile
import os
import subprocess
import time
import socket
try:
    import json
except ImportError:
    import simplejson as json

import fetchd as fetchd
import fetchd.db as db
import fetchd.data as data

import web
import ftputil

render = web.template.render('templates/')

urls = (
        '/login', 'LoginPage',
        '/browse', 'BrowsePage',
        '/download', 'DownloadPage',
        '/getcif/(.*)', 'GetCif',
        '/dir/(.*)', 'DirPage',
        '/status/(.*)', 'StatusPage',
        )

app = web.application(urls, globals())

# Workaround to make sessions work in debug mode
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

class DownloadPage:
    def GET(self):
        return 'POST only'
    def POST(self):
        i = web.input()
        source = session.source
        path = i.path
        dest = i.dest
        ret = fetchd.request(fetchd.Message(['download', source, path, dest]))
        if ret[0] == 'download':
            return ret[1]
        return '|'.join(ret)

class GetCif:
    def GET(self, fileId):
        fileRepository = '/home/jbk/cod/cif'
        folder = fileId[0]
        filePath = os.path.join(fileRepository, folder, fileId+".cif")
        fileContents = file(filePath).read()
        return json.dumps(fileContents)     

class DirPage:
    def _children(self, path, source):
        ret = fetchd.request(fetchd.Message(['dir', source, path]))
        if ret[0] == 'dir':
            dirs = cPickle.loads(ret[1])
        else:
            return str(ret)
        ret = []
        for p in dirs:
                child = {'data':p[0],
                         'attr':{'id':os.path.join(path,p[0]),
                                 'folder':bool(p[1])}}
                if p[1]:
                    child['state'] = 'closed'
                else:
                    # TODO: proper file icon
                    child['icon'] = '/'
                ret.append(child)
        return ret
    
    def GET(self, path):
        return json.dumps(self._children(path, session.source))

class StatusPage:
    def GET(self, path):
        ret = fetchd.request(fetchd.Message(['status', path]))
        return '|'.join(map(str,ret))

class BrowsePage:
    def GET(self):
        if not hasattr(session, 'source'):
            raise web.seeother("/login")
        source = cPickle.loads(session.source)
        #print source#, path
        #if source.isdir(path):
            #dir = source.listdir(path)
        return render.newbrowse(source[0])
        #elif source.isfile(path):
        #    return render.download(source.name(), path, '')
        #else:
        #    return 'not found'

class LoginPage:
    def GET(self):
        return render.login(data.sources.keys(), '')
    
    def POST(self):
        i = web.input()
        if not i.source in data.sources.keys():
            return render.login(data.sources.keys(), "Invalid data source")
        
        source = data.sources[i.source]
        o = socket.getdefaulttimeout()
        socket.setdefaulttimeout(5.0)
        try:
            s = source(i.username, i.password)
        except data.LoginError:
            return render.login(data.sources.keys(), "Failed to log in")
        except socket.error:
            return render.login(data.sources.keys(), "Failed to connect")
        except:
            raise
            #return render.login(data.sources.keys(), "Unknown error")
        finally:
            socket.setdefaulttimeout(o)
        
        session.source = cPickle.dumps((i.source, i.username, i.password), protocol=0)
        session.downloads = []
        raise web.seeother("/browse")
        
if __name__ == "__main__":
    app.run()