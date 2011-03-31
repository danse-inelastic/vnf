#!/usr/bin/env python


import hmac
import base64
import sha
import time
import string
import urllib

def makeurl(token=None, certificate=None, service=None, expires=None, prefix=None):
    if prefix is None:
        prefix = 'https://nucleus.sns.gov'
    urlT = '%(prefix)s/service/%(service)s/usersOrbiterAccessKeyId=%(token)sExpires=%(expires)s'
    url = urlT % locals()
    # print url
    
    signature = base64.encodestring(hmac.new(certificate, url, sha).digest()).strip()
    signature = urllib.quote(signature)
    # print signature
    urlT = '%(prefix)s/service/%(service)s/users?OrbiterAccessKeyId=%(token)s&Expires=%(expires)s&Signature=%(signature)s'
    url = urlT % locals()
    #url = urllib.quote(url)
    return url

    
def main():
    import sys
    certificatefile = sys.argv[1]
    token = sys.argv[2]
    certificate = open(certificatefile).read()
    service = 'user-group-service.php'
    expires=str(int(time.mktime(time.gmtime()))+60)
    url = makeurl(token=token, certificate=certificate, service=service, expires=expires)
    # print url
    print urllib.urlopen(url).read()
    return

#   ./snsAuthenticate2.py ~/lj7.key bh4mgxjrqwx0m3ba2scvdxdwbkb3ad3bivkoks5yfuqpmppe7rzad2wedw6dxxc7


if __name__ == '__main__': main()
