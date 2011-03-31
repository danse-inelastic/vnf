#!/usr/bin/python
import base64
import hmac
import sha
import sys

import time

def main():

    EXPIRES=str(int(time.mktime(time.gmtime()))+60)

#    idfile = open("securityToken.id") #security token in a file
#    ACCESS_KEY = idfile.read()
#    idfile.close()

    keyfile = open("jbrkeith.key") #private key (certificates page down at bottom)
    PRIVATE_KEY = keyfile.read()
    keyfile.close()

    #if len(sys.argv) < 2:
    #    print 'Usage: testOrbiterREST.py [URI]'
    #    sys.exit()

    #[URI] = sys.argv[1:]

    URI =  'https://nucleus.sns.gov/service/user-group-service.php/users'

    ACCESS_KEY='shj4ajfhxm5kjgnuvjstrdcanmfysp48uf0tn7y8hshpzvbj5t4nu4m5grtw4otn'

    #EXPIRES='1241116263'

    string = URI + 'OrbiterAccessKeyId=' + ACCESS_KEY + 'Expires=' + EXPIRES

    SIGNATURE = base64.encodestring(hmac.new(PRIVATE_KEY, string, sha).digest()).strip()
    
    #print 'signature', SIGNATURE

    #print 'Test generation of Orbiter VFS SOA URI\n'

    #print URI + '?OrbiterAccessKeyId=' + ACCESS_KEY + '&Expires=' + EXPIRES + '&Signature=' + SIGNATURE + '\n'

    from urllib import urlopen, quote
    print urlopen(URI + '?OrbiterAccessKeyId=' + ACCESS_KEY + '&Expires=' + EXPIRES + '&Signature=' + quote(SIGNATURE)).read()


if __name__=='__main__':
	main()
	
#17rp6DPaYn640uOmMRdzbFkx890

