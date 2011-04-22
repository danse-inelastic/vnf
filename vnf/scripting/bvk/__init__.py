# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def computePhonons(modelid, df=0.02, N1=40, credential=None):
    from .. import run
    # create a new computation
    computationid = run(
        actor='material_simulations/phonon_calculators/bvk',
        routine='createComputation',
        target = 'phonons',
        model_id = modelid, 
        credential = credential,
        )
    # set computation parameters
    run(actor='orm/bvk_getphonons',
        routine='process',
        df = df, N1 = N1,
        id = computationid,
        credential = credential,
        )

    # create a job for the computation and submit it and wait for it
    # to finish and wait for result retrieval to finish
    from ..computation import createAndRunJobFullCycle
    createAndRunJobFullCycle(
        type = 'material_simulations.BvKComputation.BvK_GetPhonons',
        id = computationid,
        credential = credential,
        )
    return 


def test():
    model_id='6P343XN'
    from .. import authenticate
    credential = authenticate(username='xxxx', password='xxxx')
    computePhonons(model_id, credential=credential)
    return


# version
__id__ = "$Id$"

# End of file 
