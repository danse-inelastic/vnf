# 10/18/10
# Charles O. Goddard

import os
import time
import select
import socket

import modules
from public import Message

class ClientError(RuntimeError):
    def __init__(self, msg):
        super(ClientError, self).__init__(msg)

class Client(object):
    def __init__(self, sock):
        sock.setblocking(False)
        self.sock = sock
        self.buf = []
        self.outbuf = []
        self.last_Message = time.time()
    
    def fileno(self):
        return self.sock.fileno()
    
    def do_write(self):
        # Send as much pending data as possible
        if self.outbuf:
            try:
                sent = self.sock.send(self.outbuf[0])
            except socket.error:
                pass
            else:
                if sent and sent == len(self.outbuf[0]):
                    self.outbuf.pop(0)
                elif sent:
                     self.outbuf[0] = self.outbuf[0][:sent]
    
    def do_read(self):
        # Read whatever we can
        data = self.sock.recv(4096)
        if not data:
            raise ClientError("Connection closed")
        self.buf.append(data)
        
        # Parse a completed message
        if self.buf and '\x01' in self.buf[-1]:
            idx = self.buf[-1].index('\x01')
            last_chunk = self.buf[-1][0:idx+1]
            next_start = self.buf[-1][idx+1:]
            msg = ''.join(self.buf[:-1]+[last_chunk])
            self.buf = [next_start] if next_start else []
            return Message.deserialize(msg)
        return None
    
    def send(self, msg):
        self.outbuf.append(msg.serialize())
    
    def kill(self):
        try:
            self.sock.close()
        except socket.error:
            pass


class Core(object):
    def __init__(self, addr='/tmp/cg_fetchd'):
        try:
            os.unlink(addr)
        except OSError:
            pass
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(5)
        self.clients = []
        self.last_act = time.time()
        
        self.modules = []
        self.services = {}
        for mtype in modules.exposed:
            self.modules.append(mtype(self))
    
    def process(self, client, message):
        if not message[0] in self.services:
            print message
            raise Exception('Invalid service requested')
        self.services[message[0]](client, message[1:])
    
    def think(self):
        map(lambda s: s.maintain(), self.modules)
        (rr, rw, _) = select.select(self.clients+[self.sock], self.clients, [], 10.0)
        if not rr and not [c for c in rw if c.outbuf]:
            time.sleep(0.5)
            return True
        
        if self.sock in rr:
            rr.remove(self.sock)
            (s, _) = self.sock.accept()
            self.clients.append(Client(s))
            
        if rr:
            self.last_act = time.time()
        
        for client in rr:
            try:
                msg = client.do_read()
            except ClientError, e:
                print e
                self.clients.remove(client)
            else:
                self.process(client, msg)
        for client in rw:
            try:
                client.do_write()
            except ClientError, e:
                print e
                self.clients.remove(client)
        if self.last_act + 60 * 5 <= time.time():
            return False
        return True
