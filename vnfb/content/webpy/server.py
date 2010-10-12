#!/usr/bin/python
# 9/30/10
# Charles O. Goddard


import socket
import cPickle
import tempfile

import db
import data

import web
import ftputil

render = web.template.render('templates/')

urls = (
        '/login', 'LoginPage',
        '/browse/(.*)', 'BrowsePage'
        )

app = web.application(urls, globals())

# Workaround to make sessions work in debug mode
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

# This ranks pretty high on my list of favorite variable names.
# TODO: Make this less appalling.
hardcoded_connection_string_in_plaintext = "dbname=test user=postgres password=TzjUvh"

class BrowsePage:
    def GET(self, path):
        if not session.source:
            raise web.seeother("/login")
        source = cPickle.loads(session.source)
        if source.isdir(path):
            dir = source.listdir(path)
            return render.browse(source.name(), path, dir)
        elif source.isfile(path):
            return render.download(source.name(), path, '')
        else:
            return 'not found'
    
    def POST(self, path):
        i = web.input()
        if not i.filename:
            return render.download(session.server, path, 'Enter a filename')
        
        source = cPickle.loads(session.source)
        if not source.isfile(path):
            print 'oh wait, nevermind'
        
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        if fs.name_exists(i.filename):
            return render.download(session.server, path, 'Name already exists')
        
        tf = tempfile.NamedTemporaryFile()
        source.download(path, tf.name)
        
        newfile = fs.new(i.filename, tf.name)
        # TODO:
        # Proper ownership and whatnot
        newfile.owner = "root"

        newfile.original_path = source.name() + "/" + path
        fs.commit()
        tf.close()
        return 'done'

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
        
        session.source = cPickle.dumps(s, protocol=2)
        raise web.seeother("/browse/")
        
if __name__ == "__main__":
    app.run()