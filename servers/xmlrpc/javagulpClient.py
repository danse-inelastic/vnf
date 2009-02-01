import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8000')
print s.multiply(2,3)  # Returns 2*3 = 6
print s.add(2,3)  # Returns 5
print s.divide(5,2)  # Returns 5//2 = 2

# Print list of available methods
#print s.system.listMethods()
