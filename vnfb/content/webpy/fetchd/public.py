# 10/18/10
# Charles O. Goddard

import socket
import time
import os

class Message(list):
    @classmethod
    def deserialize(cls, data):
        assert(data[-1] == '\x01')
        chunks = data[:-1].split('\x00')
        for i,c in enumerate(chunks):
            if c.isdigit():
                chunks[i] = int(c)
        return Message(chunks)
    
    def serialize(self):
        return '\x00'.join(map(str,self)) + '\x01'

def _conn():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect('/tmp/cg_fetchd')
    except socket.error:
        try: os.unlink('/tmp/cg_fetchd')
        except OSError: pass
        
        os.spawnlp(os.P_NOWAIT, 'python', 'python', '-m', 'fetchd')
        while not os.path.exists('/tmp/cg_fetchd'):
            time.sleep(0.2)
        sock.connect('/tmp/cg_fetchd')
    return sock

def request(msg):
    data = msg.serialize()
    s = _conn()
    s.send(data)
    buf = []
    while True:
        data = s.recv(1024)
        if not data:
            raise Exception('socket broken')
        buf.append(data)
        if buf and buf[-1] and buf[-1][-1] == '\x01':
            break
    return Message.deserialize(''.join(buf))

(DS_STARTING, DS_WORKING, DS_DONE,
 DS_FAILED, DS_LOADING) = range(5)