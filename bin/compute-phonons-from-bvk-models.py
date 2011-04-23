#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main():
    # authenticate
    from vnf.scripting import authenticate
    from realuser import username, password
    credential = authenticate(username=username, password=password)
    
    # find models
    from vnf.scripting import run
    table='material_simulations.BvKModel.BvKModel'
    ids = run(actor='db', routine='getIDs', 
              table=table, credential=credential)
    ids = ids.split(',')
    # ids = ids[:3]
        
    # run computations on models
    from vnf.scripting.bvk.phonons import compute
    failed = []
    for id in ids:
        try:
            compute(id, credential=credential)
        except:
            failed.append(id)
        continue
    
    print "Failed bvk models: %s" % (failed, )
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
