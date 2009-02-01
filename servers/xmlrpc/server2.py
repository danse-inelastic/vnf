from SimpleXMLRPCServer import SimpleXMLRPCServer

def retrieveStructure(id):
    from vnf.components.Clerk import Clerk
    clerk = Clerk()
    
    polycrystal=getRecordByID(self, 'polycrystal', id)
    

# A simple server with simple arithmetic functions
server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(retrieveStructure, 'retrieveStructure')
server.serve_forever()
