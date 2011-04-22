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


computationtype = 'material_simulations.BvKComputation.BvK_GetPhonons'


def compute(modelid, df=0.02, N1=40, credential=None):
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
        type = computationtype,
        id = computationid,
        credential = credential,
        )

    # create plot
    createPlot(computationid, credential)
    return 


def createPlot(computationid, credential):
    """create plot for the computation result (phonons)

    Input:
    - computationid: id of the bvk phonons computation
    - credential: credential object
    """
    from .. import run
    res = run(
        actor = 'computation',
        routine = 'getResults',
        type = computationtype,
        id = computationid,
        credential = credential,
        )
    res = eval(res)
    assert len(res) == 1
    res0 = res[0]
    assert res0[0].lower() == 'phonons'
    phononsid = res0[1]
    run(
        actor='orm/phonons',
        routine='createGraphicalView',
        id = phononsid,
        credential = credential,
        )
    return 

# version
__id__ = "$Id$"

# End of file 
