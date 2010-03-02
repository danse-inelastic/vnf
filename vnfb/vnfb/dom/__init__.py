# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t as object2table


def importType(name):
    path = name.split('.')
    m = '.'.join(path[:-1])
    m = _import(m)
    return getattr(m, path[-1])


def _import(modulename):
    pkg = 'vnfb.dom'
    m = '%s.%s' % (pkg, modulename)
    return __import__(m, {}, {}, [''])


def qetables():
    "QE Tables"
    ts  = [
            'QESimulation.QESimulation',
            'QETask.QETask',
            'QESimulationTask.QESimulationTask',
            'QEJob.QEJob',
            'QEConfiguration.QEConfiguration',
            'QESetting.QESetting',
            ]

    return map(importType, ts)

def qesimtables():
    "QE Simulations Tables"
    ts  = ['QESimulation.QESimulation',]

    return map(importType, ts)



def tables_without_orm():
    # for compatibility with vnf-alpha. should eventually remove
    from vnf.dom import alltables
    vnfalphatables = alltables()

    ts = [
        'ITask.ITask',
        'Server.Server',
        'Job.Job',
        'User.User',
        'UserHasRole.UserHasRole',
        'Privilege.Privilege',
        ]
    tables = map(importType, ts)
    return vnfalphatables + tables + qetables()


# version
__id__ = "$Id$"

# End of file 
