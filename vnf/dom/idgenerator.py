
generator = None


import time
def idFromTime():
    x=time.ctime()
    return x.replace(' ','-') 
