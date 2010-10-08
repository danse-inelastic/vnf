#!/usr/bin/python
# 9/30/10
# Charles O. Goddard


import socket

import db
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
hardcoded_connection_string_in_plaintext = "dbname=test user=jbk password=chem88"

class BrowsePage:
    def GET(self, path):
        if not session.server:
            raise web.seeother("/login")
        f = ftputil.FTPHost(session.server, session.username, session.password)
        if f.path.isdir(path):
            dir = f.listdir(path)
            return render.browse(session.server, path, dir)
        elif f.path.isfile(path):
            return render.download(session.server, path, '')
        else:
            return 'not found'
    
    def POST(self, path):
        i = web.input()
        if not i.filename:
            return render.download(session.server, path, 'Enter a filename')
        
        f = ftputil.FTPHost(session.server, session.username, session.password)
        if not f.path.isfile(path):
            print 'oh wait, nevermind'
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        try:
            newfile = fs.new(i.filename)
        except:
            return render.download(session.server, path, 'Name already exists')
        else:
            # TODO:
            # Proper ownership and whatnot
            newfile.owner = "root"

            newfile.original_path = session.server + "/" + path
            d = newfile.data()
            d.write(f.file(path, 'r').read())
            fs.commit()
            return 'done'

class LoginPage:
    def GET(self):
        return render.login('')
    
    def POST(self):
        i = web.input()
        if not i.server:
            return render.login('Must specify server')
        
        o = socket.getdefaulttimeout()
        socket.setdefaulttimeout(3.0)
        try:
            f = ftputil.FTPHost(i.server,
                                i.username or 'anonymous',
                                i.password)
        except ftputil.ftp_error.FTPError:
            return render.login("Failed to log in")
        except socket.error:
            return render.login("Failed to connect")
        finally:
            socket.setdefaulttimeout(o)
        
        # This feels really ugly, but I can't think of an easy way to
        # persist an FTP connection across processes off the top of my
        # head -- so in it stays.
        session.username = i.username or 'anonymous'
        session.password = i.password
        session.server = i.server
        raise web.seeother("/browse/")
        
if __name__ == "__main__":
    app.run()